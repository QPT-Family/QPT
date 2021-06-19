import sys

import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from qpt.kernel.qt_ui import GUIML
from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.terminal import QTCondaVenv, QTerminal
from qpt.kernel.tools.os_op import SysInfo

"""
GUI界面以及变量名命名规范：用途_动作_控件
例：发送shell的按钮为shell_send_button
"""


class GUIModuleLauncher(GUIML.Ui_Launcher):
    COLOR_GREEN = [170, 255, 0]
    COLOR_ORANGE = [255, 170, 0]
    COLOR_ORANGE_RED = [255, 85, 0]

    def __init__(self, q_windows):
        self.q_windows = q_windows
        # 终端对象
        self.main_terminal = QTerminal()
        self.main_terminal.start()

        # 初始化GUI界面
        self.setupUi(q_windows)

        # 初始化GUI终端
        self.shell_init()

        # 初始化系统信息模块
        self.sys_info = SysInfo()
        self.device_info_apply()
        # 初始化信息 ！此处后续需要进一步封装为自动选择设备
        self.memory_info_apply(0)

        # 初始化当前虚拟环境信息
        self.qt_conda_venv = QTCondaVenv(self.shell_send)
        self.venv_info_apply()

    def setupUi(self, q_windows):

        super(GUIModuleLauncher, self).setupUi(q_windows)
        # 固定终端框游标初始化
        self.shell_window_text.ensureCursorVisible()
        # 终端框文本界面绑定
        self.main_terminal.set_text_browser(self.shell_window_text)
        # 终端框按钮绑定
        self.shell_send_button.clicked.connect(self.shell_send_with_shell_text)
        self.shell_reset_button.clicked.connect(self.shell_reset)
        self.shell_clear_button.clicked.connect(self.shell_clear)
        # 设备选择框绑定
        self.select_device_comboBox.highlighted.connect(self.memory_info_apply)
        # 环境下拉列表框绑
        self.select_env_comboBox.activated.connect(self.venv_activate)

    def shell_send(self, shell, yes_opt=None, no_opt=None):
        """
        向终端发送指令
        :param shell: 指令
        :param yes_opt: 运行成功则执行yes_opt()
        :param no_opt: 运行失败则执行no_opt()
        """
        Logging.debug("send_shell: " + shell)
        self.main_terminal.send_shell(shell, yes_opt, no_opt)

    def shell_send_with_shell_text(self):
        """
        在界面中向终端发送指令
        """
        shell = self.shell_text.text()
        self.shell_text.clear()
        self.shell_send(shell)

    def shell_init(self):
        """
        启动窗口内嵌入的终端
        """
        self.main_terminal.shell_init_func()
        Logging.info("终端已启动")

    def shell_reset(self):
        """
        重启终端
        """
        self.main_terminal.shell_reset_func()
        Logging.info("终端已重启")

    def shell_clear(self):
        """
        清空终端里的输出
        """
        self.main_terminal.shell_clear_func()

    def memory_info_apply(self, index):
        """
        获取并设置系统硬件信息到GUI
        :param index: 设备索引
        """
        if index == 0:
            memory = self.sys_info.req_memory()
            if memory >= 8:
                self.memory_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_GREEN))
                self.memory_mdiArea.setStatusTip("当前环境未使用GPU，执行速度可能极慢")
                self.memory_label.setText(str(memory) + " GB")
                Logging.warning("当前环境无GPU，执行速度可能极慢")
                self.rate_label.setText("一般")
                self.rate_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_ORANGE))
            elif memory >= 4:
                self.memory_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_ORANGE_RED))
                self.memory_mdiArea.setStatusTip("当前用户CPU模式下内存竟然也紧张，可能造成系统崩溃！")
                Logging.warning("当前用户CPU模式下内存竟然也紧张，可能造成系统崩溃！")
                self.memory_label.setText(str(memory) + " GB")
                self.rate_label.setText("非常慢")
                self.rate_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_ORANGE))
            else:
                self.memory_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_ORANGE_RED))
                self.memory_mdiArea.setStatusTip("环境资源紧张，不推荐运行！")
                Logging.warning("当前用户CPU模式下内存竟然也紧张，可能造成系统崩溃！")
                self.memory_label.setText(str(memory) + " GB")
                self.rate_label.setText("<font color=\"#FF0000\">有概率死机</font>")
                self.rate_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_ORANGE_RED))

            self.rate_mdiArea.setStatusTip("当前环境未使用GPU，执行速度可能极慢")

        else:
            gpu_level = self.sys_info.req_gpu_level(idx=index - 1)
            if gpu_level == 2:
                self.memory_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_GREEN))
                self.memory_mdiArea.setStatusTip("显存较为充足，可运行一般模型")
                self.memory_label.setText("一般")
                self.rate_label.setText("很快")
                Logging.info("显存较为充足，可运行一般模型")
            elif gpu_level == 1:
                self.memory_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_ORANGE))
                self.memory_mdiArea.setStatusTip("显存较低，启动模型可能会出现显存不足情况")
                self.memory_label.setText("较低")
                self.rate_label.setText("较快")
                Logging.warning("显存较低，启动模型可能会出现显存不足情况")
            elif gpu_level == 0:
                self.memory_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_ORANGE_RED))
                self.memory_mdiArea.setStatusTip("当前GPU难以满足运行，建议升级GPU设备")
                self.memory_label.setText("极低")
                self.rate_label.setText("略快")
                Logging.warning("当前GPU难以满足运行，建议升级GPU设备。")
            self.rate_mdiArea.setBackground(PyQt5.QtGui.QColor(*self.COLOR_GREEN))
            self.rate_mdiArea.setStatusTip("当前环境使用GPU，执行速度较快")

    def device_info_apply(self):
        """
        获取设备信息并加载到下拉列表中
        """
        gpus_info = self.sys_info.req_all_gpu_info()
        self.select_device_comboBox.addItems(gpus_info)

    def venv_info_apply(self):
        self.select_env_comboBox.clear()
        venvs_info = self.qt_conda_venv.req_venv_info()
        venvs_info = ["->点击此处新建一个环境<-"] + venvs_info
        self.select_env_comboBox.addItems(venvs_info)

    def venv_create(self):
        venv_name = "paddle20-cpu-1"
        signal = QMessageBox.question(self.q_windows,
                                      "创建新环境",
                                      f"是否需要立即创建一个名为{venv_name}全新的环境？\n若需要创建请点击“是(Yes)”",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if signal == QMessageBox.Yes:
            self.qt_conda_venv.set_opt(
                lambda: QMessageBox.information(self.q_windows,
                                                "创建新环境",
                                                f"新环境创建成功！(概率较大)",
                                                QMessageBox.Close,
                                                QMessageBox.Close),
                lambda: QMessageBox.warning(self.q_windows,
                                            "创建新环境",
                                            f"新环境创建失败！(概率较大)",
                                            QMessageBox.Close,
                                            QMessageBox.Close))
            self.qt_conda_venv.create_venv(venv_name=venv_name)

    def venv_activate(self, index):
        """
        进入到当前环境
        """
        if index == 0:
            self.venv_create()
        self.qt_conda_venv.set_opt(
            lambda: QMessageBox.information(self.q_windows,
                                            "加载Python环境",
                                            f"新环境加载成功！(概率较大)",
                                            QMessageBox.Close,
                                            QMessageBox.Close),
            lambda: QMessageBox.warning(self.q_windows,
                                        "加载Python环境",
                                        f"新环境加载失败！(概率较大)",
                                        QMessageBox.Close,
                                        QMessageBox.Close))
        venv_name = self.qt_conda_venv.activate_env(index - 1)
        self.select_env_comboBox.clear()

        self.main_terminal.write_text(f"<font color=\"#00aa00\">{venv_name}环境激活成功  "
                                      f"<font color=\"#000000\"></font>")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    gui_module_launcher = GUIModuleLauncher(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
