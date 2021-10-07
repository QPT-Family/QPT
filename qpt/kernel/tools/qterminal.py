import subprocess
from qpt.kernel.tools.qlog import Logging
from qpt.sys_info import get_env_vars

TERMINAL_NAME = "powershell"


# TERMINAL_MSG_FITTER_TAG = ["Microsoft Windows [版本", "(c) Microsoft Corporation。保留所有权利。"]


# try:
#     import PyQt5
#     from PyQt5 import QtCore
#     from PyQt5.QtCore import pyqtSignal
#
#     TERMINAL_TYPE = "QTerminal"
# except ModuleNotFoundError:
#     TERMINAL_TYPE = "PTerminal"
#     Logging.debug("当前环境不存在PyQT")


class TerminalCallback:
    def __init__(self):
        self.cache = ""

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
                    if msg == "True":
                        self.normal_func()
                        break
                    elif msg == "False":
                        self.error_func()
                        break

                #             for tag_id, tag in enumerate(TERMINAL_MSG_FITTER_TAG):
                #                 if tag in msg:
                #                     break
                #                 if tag_id == len(TERMINAL_MSG_FITTER_TAG) - 1:
                #                     self.cache += msg
                #                     Logging.debug(msg)
                self.cache += msg
                Logging.debug(msg)

    def normal_func(self):
        self.cache = ""
        Logging.debug("终端命令执行成功！")

    def error_func(self):
        Logging.error(f"在执行终端命令时检测到了失败，完整信息如下：\n{self.cache}")
        self.cache = ""


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
        path_vars = get_env_vars()["PATH"]
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
    def __init__(self):
        super(PTerminal, self).__init__()

    def init_terminal(self):
        self.main_terminal = subprocess.Popen(TERMINAL_NAME,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              stdin=subprocess.PIPE,
                                              shell=True,
                                              close_fds=True)
        prepare = "chcp 65001"
        self._shell_func()(prepare)
        prepare = "set PATH='" + self._get_env_vars() + "'"
        self._shell_func()(prepare)

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


# class QTerminal(Terminal):
#     def __init__(self):
#         super(QTerminal, self).__init__()
#         # 信息输出绑定函数占位
#         self.terminal_normal_info_func = None
#         self.terminal_error_info_func = None
#
#     def init_terminal(self):
#         self.main_terminal = QtCore.QProcess()
#         self.main_terminal.start(TERMINAL_NAME)
#
#     def reset_terminal(self):
#         self.close_terminal()
#         self.init_terminal()
#
#     def close_terminal(self):
#         self.main_terminal.close()
#
#     def shell(self, shell, callback: TerminalCallback = MessageBoxTerminalCallback()):
#         self.shell_func(callback)(shell)
#
#     def shell_func(self, callback: TerminalCallback = MessageBoxTerminalCallback()):
#         self.main_terminal.readyReadStandardOutput.connect(callback.normal_func)
#         self.main_terminal.readyReadStandardError.connect(callback.error_func)
#
#         def closure(closure_shell):
#             Logging.debug(f"SHELL: {closure_shell}")
#             closure_shell += "&&echo GACT:DONE!||echo GACT:ERROR!\n"
#             # 发送指令
#             self.main_terminal.write(closure_shell.encode("gbk"))
#             callback.handle()
#
#         return closure


# 实现自动Terminal类型
# AutoTerminal = PTerminal if TERMINAL_TYPE == "PTerminal" else QTerminal

AutoTerminal = PTerminal  # 当前正在测试QTerminal，暂时只使用PTerminal
if __name__ == '__main__':
    t = AutoTerminal()
    t.shell("ping 192.168.1.1")
