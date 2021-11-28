import subprocess
from qpt.kernel.qlog import Logging
from qpt.memory import get_env_vars, QPT_MODE

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

    def __init__(self):
        self.main_terminal = None
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
        path_vars = get_env_vars()
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
    def __init__(self, shell_mode=True):
        self.shell_mode = shell_mode
        super(PTerminal, self).__init__()

    def init_terminal(self):
        if self.shell_mode:
            self.main_terminal = subprocess.Popen(TERMINAL_NAME,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT,
                                                  stdin=subprocess.PIPE,
                                                  shell=True,
                                                  env=self._get_env_vars())
        else:
            self.main_terminal = subprocess.Popen(TERMINAL_NAME,
                                                  shell=False,
                                                  env=self._get_env_vars())
        # ToDo 加个自动判断
        Logging.info("\n如在本信息之后停留时间较长，请升级Windows Powershell至版本5即可解决该问题，下载地址：\n"
                     "官方地址：https://www.microsoft.com/en-us/download/details.aspx?id=54616\n"
                     "团子云镜像：https://s.dango.cloud/s/ZyDSn 下载码：egl95d")
        prepare = "chcp 65001"
        self._shell_func()(prepare)
        if QPT_MODE == "Debug":
            # 打印环境变量
            self._shell_func()("dir env:")
        # prepare = "$env:PATH='" + self._get_env_vars() + "'"
        # self._shell_func()(prepare)

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
            self.main_terminal.stdin.write(final_shell)
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
