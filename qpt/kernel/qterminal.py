import subprocess
import os
import zipfile

from qpt.kernel.qlog import Logging
from qpt.kernel.qos import download, TMP_BASE_PATH
from qpt.memory import QPT_MEMORY, QPT_MODE

TERMINAL_NAME = "powershell"


# TERMINAL_NAME = "pwsh"


class TerminalCallback:
    def __init__(self):
        self.cache = ""
        self.error_fitter = list()
        self.normal_fitter = list()

    def handle(self, terminal=None):
        """
        该函数将获取终端输出，并且需要显式调用执行成功与失败的func
        """
        raise NotImplementedError(f"{self.__class__.__name__}中未定义handle方法")

    def normal_func(self):
        """
        终端执行成功后需要执行的Method
        """
        raise NotImplementedError(f"{self.__class__.__name__}中未定义normal_func方法")

    def error_func(self):
        """
        终端执行失败后需要执行的Method
        """
        raise NotImplementedError(f"{self.__class__.__name__}中未定义error_func方法")


class MessageBoxTerminalCallback(TerminalCallback):
    def handle(self, terminal=None):
        pass

    def normal_func(self):
        pass

    def error_func(self):
        pass


class LoggingTerminalCallback(TerminalCallback):
    def handle(self, terminal=None):
        assert terminal, "此处需要terminal"
        line = True
        end = False
        while line:
            line = terminal.stdout.readline()
            msg = line.decode('gbk', errors="ignore").strip("b'").strip("\n").strip("\r")
            if msg:
                if msg == '---QPT OUTPUT STATUS CODE---':
                    end = True
                    continue
                if msg == "\r" or msg == "\n":
                    continue
                if end:
                    fitter_flag = False
                    for normal_fitter in self.normal_fitter:
                        if normal_fitter in self.cache:
                            self.normal_func()
                            fitter_flag = True
                    for error_fitter in self.error_fitter:
                        if error_fitter in self.cache:
                            self.error_func()
                            fitter_flag = True
                    if fitter_flag:
                        break
                    if msg == "True":
                        self.normal_func()
                        break
                    elif msg == "False":
                        self.error_func()
                        break
                self.cache += msg + "\n"
                self.print_func(msg)

    @staticmethod
    def print_func(msg):
        Logging.debug(msg)

    def normal_func(self):
        self.cache = ""
        Logging.debug("终端命令执行成功！")

    def error_func(self):
        Logging.error(f"在执行终端命令时检测到了失败，完整信息如下：\n{self.cache}")
        self.cache = ""


class RunTerminalCallback(LoggingTerminalCallback):
    @staticmethod
    def print_func(msg):
        print(msg)


class Terminal:
    """
    Terminal基类，定义Terminal基本方法
    """

    def __init__(self, cwd="./"):
        self.main_terminal = None
        self.cwd = cwd
        self.init_terminal()
        Logging.debug(f"正在连接{self.__class__.__name__}")

    def init_terminal(self):
        raise NotImplementedError(f"{self.__class__.__name__}中未定义init_terminal方法")

    @staticmethod
    def _get_env_vars():
        """
        为Terminal设置环境变量
        """
        # ToDO 需考虑增加兼容性支持 - 当前只考虑Windows和完整Python环境
        # ToDO 貌似没考虑打包时候的环境变量
        path_vars = QPT_MEMORY.get_env_vars()
        return path_vars

    def reset_terminal(self):
        """
        重启Terminal
        """
        raise NotImplementedError(f"{self.__class__.__name__}中未定义reset_terminal方法")

    def close_terminal(self):
        """
        关闭Terminal
        """
        raise NotImplementedError(f"{self.__class__.__name__}中未定义close_terminal方法")

    def shell(self, shell, callback: TerminalCallback = None):
        """
        执行shell语句
        :param shell: shell语句
        :param callback:
        """
        raise NotImplementedError(f"{self.__class__.__name__}中未定义shell方法")

    def shell_func(self, callback: TerminalCallback = None):
        """
        获取shell函数
        :param callback:
        :return: shell函数
        """
        raise NotImplementedError(f"{self.__class__.__name__}中未定义shell_func方法")


class PTerminal(Terminal):
    def __init__(self, shell_mode=True, cwd="./"):
        self.shell_mode = shell_mode
        self.first_flag = True
        super(PTerminal, self).__init__(cwd=cwd)

    def init_terminal(self):
        if self.shell_mode:
            self.main_terminal = subprocess.Popen(TERMINAL_NAME,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT,
                                                  stdin=subprocess.PIPE,
                                                  shell=True,
                                                  env=self._get_env_vars(),
                                                  cwd=self.cwd)
        else:
            self.main_terminal = subprocess.Popen(TERMINAL_NAME,
                                                  shell=False,
                                                  env=self._get_env_vars(),
                                                  cwd=self.cwd)
        # ToDo 加个自动判断
        Logging.info("\n如在本信息之后停留时间较长，请升级Windows Powershell至版本5即可解决该问题，下载地址：\n"
                     "官方地址：https://www.microsoft.com/en-us/download/details.aspx?id=54616\n"
                     "团子云镜像：https://s.dango.cloud/s/GVbhB 下载码：zAkjpradJA2eHiC")
        prepare = "chcp 65001"
        self._shell_func()(prepare)
        Logging.info("检测结束，当前Powershell满足使用需求。")
        # if QPT_MODE == "Debug":
        #     self._shell_func()("dir env:")

    def reset_terminal(self):
        self.close_terminal()
        self.init_terminal()

    def close_terminal(self):
        self.main_terminal.terminate()

    def _shell_func(self, callback: TerminalCallback = LoggingTerminalCallback()):
        # ToDo 实现Callback
        def closure(closure_shell):
            Logging.debug(f"SHELL: {closure_shell}")
            if closure_shell[1:3] == ":\\":
                closure_shell += f"cd {closure_shell[:2]} ;"
            closure_shell = f'{closure_shell} ; echo "---QPT OUTPUT STATUS CODE---" $? \n'
            try:
                final_shell = closure_shell.encode("utf-8")
            except Exception as e:
                Logging.error("执行该指令时遇到解码问题，目前将采用兼容模式进行，原始报错如下：\n" + str(e))
                final_shell = closure_shell.encode("utf-8", errors="ignore")

            try:
                self.main_terminal.stdin.write(final_shell)
            except OSError as e:
                if self.first_flag:
                    Logging.warning("当前操作系统可能无法正常调起Powershell，如您正在使用盗版/已被破坏的Windows操作系统，"
                                    f"强烈建议您进行更新！\n当前正在尝试在线补充Powershell，原始报错信息如下\n{e}")
                    Logging.info("正在下载Powershell 5")
                    download(url="https://bj.bcebos.com/v1/ai-studio-online/1c4c1b9fd52c49f3b88697e60f"
                                 "771d1e1181711684b84c7bb830cb589d1689ee?responseContentDisposition=at"
                                 "tachment%3B%20filename%3Dpwsh.zip",
                             file_name="pwsh.zip",
                             path=TMP_BASE_PATH)
                    zip_path = os.path.join(TMP_BASE_PATH, "pwsh.zip")

                    pwsh_dir = os.path.join(TMP_BASE_PATH, "pwsh_ext")
                    with zipfile.ZipFile(zip_path) as zip_obj:
                        zip_obj.extractall(pwsh_dir)

                    os_env = QPT_MEMORY.get_env_vars().copy()
                    os_env["PATH"] += f"{pwsh_dir};"
                    QPT_MEMORY.set_mem(name="get_env_vars", variable=os_env)
                    self.reset_terminal()

                    self.first_flag = False
                else:
                    Logging.error("当前操作系统仍无法正常调起Powershell，程序已终止！")
                    exit(-200)
            try:
                self.main_terminal.stdin.flush()
            except Exception as e:
                Logging.error(str(e))
            callback.handle(self.main_terminal)

        return closure

    def shell_func(self, callback: TerminalCallback = None):
        return self._shell_func(callback)

    def shell(self, shell, callback: TerminalCallback = LoggingTerminalCallback()):
        self.shell_func(callback)(shell)


if __name__ == '__main__':
    t = PTerminal()
    t.shell("ping 192.168.1.1")
    t.shell("dir")
    t.shell("ping 192.168.1.1")
