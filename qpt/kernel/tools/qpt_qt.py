import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from qpt.kernel.tools.log_op import Logging

TERMINAL_NAME = "cmd.exe"


class TerminalCallback:
    def __init__(self):
        pass

    def normal_func(self):
        pass

    def error_func(self):
        pass

    @staticmethod
    def _req_qt_process_normal_info(terminal):
        result = terminal.readAllStandardOutput().data().decode("gbk")
        return result

    @staticmethod
    def _req_qt_process_error_info(terminal):
        result = terminal.readAllStandardError().data().decode("gbk")
        return result


class MessageBoxTerminalCallback(TerminalCallback):
    pass


class QTerminal:
    def __init__(self):
        # 终端占位
        self.main_terminal = None
        # 信息输出绑定函数占位
        self.terminal_normal_info_func = None
        self.terminal_error_info_func = None

        self.init_terminal()

    def init_terminal(self):
        self.main_terminal = QtCore.QProcess()
        self.main_terminal.start(TERMINAL_NAME)

    def reset_terminal(self):
        self.main_terminal.close()
        self.init_terminal()

    def close_terminal(self):
        self.main_terminal.close()

    def shell(self, shell, callback: TerminalCallback):
        self.shell_func(callback)(shell)

    def shell_func(self, callback: TerminalCallback):
        if callback:
            self.main_terminal.readyReadStandardOutput.connect(callback.normal_func)
            self.main_terminal.readyReadStandardError.connect(callback.error_func)

        def closure(closure_shell):
            closure_shell += "&&echo GACT:DONE!||echo GACT:ERROR!\n"
            # 发送指令
            self.main_terminal.write(closure_shell.encode("gbk"))

        return closure

# class TerminalO(PyQt5.QtCore.QThread):
#     """
#     QT的Terminal管理类，收到指令后会获取输出结果，返回正确与异常结果并给出状态
#     """
#     # 初始化信号
#     # shell_final_signal = pyqtSignal(str)
#     shell_done_signal = pyqtSignal(str)
#     shell_error_signal = pyqtSignal(str)
#
#     def __init__(self, q_process=None, text_browser=None):
#         """
#         :param text_browser: 可供输出的text_browser、label等QT组件，若为None则直接返回结果
#         :param q_process:
#         """
#         super().__init__()
#         self.terminal_text_browser = text_browser
#
#         # 初始化状态
#         self.init_act = False
#         # 初始化执行后决策函数
#         self.done_opt = None
#         self.error_opt = None
#         # 当有ERROR时控制只弹出ERROR消息框, False为没有ERROR
#         self.policy_flag = False
#
#         if q_process is None:
#             self.shell_init_func()
#         else:
#             self.main_terminal = q_process
#
#     def set_act_opt(self, done_opt=None, no_opt=None):
#         """
#         设置send_shell中opt操作
#         """
#         if self.done_opt is not None:
#             self.shell_done_signal.disconnect(self.done_opt)
#         if self.error_opt is not None:
#             self.shell_error_signal.disconnect(self.error_opt)
#         if done_opt:
#             self.done_opt = done_opt
#             self.shell_done_signal.connect(self.done_opt)
#         if no_opt:
#             self.error_opt = no_opt
#             self.shell_error_signal.connect(self.error_opt)
#
#     def send_shell(self, shell, done_opt=None, no_opt=None):
#         """
#         发送shell指令
#         :param shell:shell指令
#         :param done_opt: 运行成功则执行yes_opt()
#         :param no_opt: 运行失败则执行no_opt()
#         """
#         # ！待完善 可以采用信号+序列来依次执行（或许在set时候直接组队列？），避免多个指令同事传输导致执行反馈为最后一次设置
#         self.set_act_opt(done_opt, no_opt)
#         # 当有ERROR时控制只弹出ERROR消息框, False为没有ERROR
#         self.policy_flag = False
#         # 模拟按下回车并通过&&echo GACT:DONE!||echo GACT:ERROR!来判断执行是否正常，暂时还没想出更好的方案
#         shell += "&&echo GACT:DONE!||echo GACT:ERROR!\n"
#
#         # 在GUI展示发送的命令
#         if self.terminal_text_browser is not None:
#             self.write_text(f"{'-' * 50}")
#             self.write_text(
#                 f"<font color=\"#FF0000\">[Input]>>> {shell}  <font color=\"#000000\"></font>")
#             self.write_text(f"{'-' * 50}")
#
#         # 发送指令
#         self.main_terminal.write(shell.encode("gbk"))
#
#     def shell_init_func(self):
#         """
#         初始化终端进程
#         """
#         if self.init_act is False:
#             self.main_terminal = QtCore.QProcess()
#             # 绑定输出
#             self.main_terminal.readyReadStandardOutput.connect(self.req_terminal_txt)
#             self.main_terminal.readyReadStandardError.connect(self.req_terminal_error_txt)
#             # !需完善-兼容性仅Windows
#             self.main_terminal.start(TERMINAL_NAME)
#             self.write_text("<font color=\"#FF0000\">-----控制台链接成功！-----</font>  "
#                             "<font color=\"#000000\"></font>")
#             self.init_act = True
#         else:
#             self.main_terminal.start(TERMINAL_NAME)
#
#     def shell_reset_func(self):
#         """
#         重新启动终端
#         """
#         self.main_terminal.close()
#         self.shell_init_func()
#         self.write_text("终端已重启")
#
#     def shell_clear_func(self):
#         self.terminal_text_browser.clear()
#         self.write_text("<font color=\"#FF0000\">-----控制台信息清空成功！-----</font>  "
#                         "<font color=\"#000000\"></font>")
#
#     def set_text_browser(self, text_browser):
#         """
#         设置输出容器
#         """
#         self.terminal_text_browser = text_browser
#
#     def write_text(self, text: str, in_error=False):
#         """
#         向GUI的终端界面中添加文本
#         :param text: 需要添加的文本
#         :param in_error:来自ERROR的数据
#         """
#         if self.terminal_text_browser is None:
#             return None
#         text = text.strip("\n").replace("&&echo GACT:DONE!||echo GACT:ERROR!", "")
#         self.terminal_text_browser.append("<font color=\"#000000\"></font>" + text)
#         # 对执行结果进行评估，进行决策
#         if self.done_opt and not self.policy_flag:
#             if "GACT:DONE!" in text and self.done_opt and not in_error:
#                 self.shell_done_signal.emit("执行完毕")
#         if ("GACT:ERROR!" in text and self.error_opt) or in_error:
#             self.policy_flag = True
#             self.shell_error_signal.emit("部分报错信息：" + text)
#
#         # 持续滚动，保证显示是最新一行
#         cursor = self.terminal_text_browser.textCursor()
#         pos = len(self.terminal_text_browser.toPlainText())
#         cursor.setPosition(pos)
#         self.terminal_text_browser.setTextCursor(cursor)
#
#     def req_terminal_error_txt(self):
#         """
#         获取终端报错输出并添加到GUI界面中
#         """
#         result = self.main_terminal.readAllStandardError().data().decode("gbk")
#         # 不是很清楚为什么我的电脑在打开cmd时候会出现这个，先屏蔽掉好了
#         if "系统找不到指定的路径。" in result:
#             return "系统找不到指定的路径。"
#         if result:
#             Logging.debug(result)
#             # 返回消息
#             if self.terminal_text_browser is None:
#                 return result
#             else:
#                 self.write_text(f"<font color=\"#FF0000\">[Input]>>>[可能发生了异常]{result}  "
#                                 f"<font color=\"#000000\"></font>",
#                                 in_error=True)
#
#     def req_terminal_txt(self):
#         """
#         获取终端输出并添加到GUI界面中
#         """
#         result = self.main_terminal.readAllStandardOutput().data().decode("gbk")
#         if result:
#             # 返回消息
#             Logging.debug(result)
#             if self.terminal_text_browser is None:
#                 return result
#             self.write_text(result)
#
#     def req_terminal(self):
#         return self.main_terminal
