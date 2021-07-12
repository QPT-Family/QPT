import subprocess
from qpt.kernel.tools.log_op import Logging

TERMINAL_NAME = "cmd.exe"
TERMINAL_MSG_FITTER_TAG = ["Microsoft Windows [版本", "(c) Microsoft Corporation。保留所有权利。"]
SHELL_ACT = "&&echo GACT:DONE!||echo GACT:ERROR!\n"

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
        pass

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
        while line:
            line = terminal.stdout.readline()
            if line == b'GACT:DONE!\r\n':
                self.normal_func()
                break
            elif line == b'GACT:ERROR!\r\n':
                self.error_func()
                break
            msg = line.decode('gbk').strip("b'").strip("\n").strip(SHELL_ACT)
            if msg == "\r":
                continue

            for tag_id, tag in enumerate(TERMINAL_MSG_FITTER_TAG):
                if tag in msg:
                    break
                if tag_id == len(TERMINAL_MSG_FITTER_TAG) - 1:
                    Logging.debug(msg)

    def normal_func(self):
        Logging.debug("终端命令执行成功！")

    def error_func(self):
        Logging.error("终端命令执行失败！")


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

    def reset_terminal(self):
        raise NotImplementedError(f"{self.__class__.__name__}中未定义reset_terminal方法")

    def close_terminal(self):
        raise NotImplementedError(f"{self.__class__.__name__}中未定义close_terminal方法")

    def shell(self, shell, callback: TerminalCallback = None):
        raise NotImplementedError(f"{self.__class__.__name__}中未定义shell方法")

    def shell_func(self, callback: TerminalCallback = None):
        raise NotImplementedError(f"{self.__class__.__name__}中未定义shell_func方法")


class PTerminal(Terminal):
    def __init__(self):
        super(PTerminal, self).__init__()

    def init_terminal(self):
        self.main_terminal = subprocess.Popen(TERMINAL_NAME,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              stdin=subprocess.PIPE,
                                              shell=True)

    def reset_terminal(self):
        self.close_terminal()
        self.init_terminal()

    def close_terminal(self):
        self.main_terminal.terminate()

    def shell(self, shell, callback: TerminalCallback = LoggingTerminalCallback()):
        self.shell_func(callback)(shell)

    def shell_func(self, callback: TerminalCallback = LoggingTerminalCallback()):
        # ToDo 实现Callback
        def closure(closure_shell):
            Logging.debug(f"SHELL: {closure_shell}")
            closure_shell += "&&echo GACT:DONE!||echo GACT:ERROR!\n"
            # 发送指令
            self.main_terminal.stdin.write(closure_shell.encode("gbk"))
            self.main_terminal.stdin.flush()
            callback.handle(self.main_terminal)

        return closure


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
