import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

from qpt.kernel.qt_ui.welcome import Ui_welcome
from qpt.gui.qpt_about import MiniAbout
from qpt.gui.qpt_msg import write_path_with_msg
from qpt.kernel.tools.os_op import add_ua, set_qpt_env_var


# ToDo: 首次使用
class Welcome(QWidget, Ui_welcome):
    def __init__(self):
        super().__init__()
        # About占位
        self.about = None
        self.path_auto = "C:/QPT_HOME"
        self.path_select = "C:/QPT_HOME/QPT.exe"

        self.setupUi(self)

    def setupUi(self, unzip_file_dialog):
        super().setupUi(unzip_file_dialog)
        self.button_about.clicked.connect(self.open_about)
        self.button_next.clicked.connect(self.next_event)
        self.button_choose_folder.clicked.connect(self.select_dir_event)
        self.tab_mode.currentChanged.connect(self.select_tab_event)

    def open_about(self):
        self.about = MiniAbout()
        self.about.show()

    def next_event(self):
        """
        点击下一步时产生的事件
        """
        mode = self.tab_mode.currentIndex()
        if mode == 0:
            self.auto_create_act()
        else:
            self.select_base_env_act()

    def auto_create_act(self):
        """
        自动创建环境
        """
        base_path = self.text_input_path.text()
        act = write_path_with_msg(self, base_path)

        # 加上环境变量
        if act:
            add_ua()
            set_qpt_env_var(base_path)
            # ToDO 复制启动器至该目录，并修改注册表注册QPT文件

    def select_base_env_act(self):
        """
        手动选择环境
        """
        base_path = os.path.split(self.text_input_path.text())[0]
        act = write_path_with_msg(self, base_path)

        # 加上环境变量
        if act:
            add_ua()
            set_qpt_env_var(base_path)

    def select_dir_event(self):
        mode = self.tab_mode.currentIndex()
        if mode == 0:
            out = QFileDialog.getExistingDirectory(self, "选择文件夹")
            path = os.path.join(out, "QPT_HOME")
            self.path_auto = path
        else:
            out = QFileDialog.getOpenFileName(self, "选择QPT.exe文件", "./", filter="QPT EXE(QPT.exe)")
            path = out[0]
            self.path_select = path
        self.text_input_path.setText(path)

    def select_tab_event(self):
        mode = self.tab_mode.currentIndex()
        if mode == 0:
            self.button_choose_folder.setText("选择文件夹")
            self.text_input_path.setText(self.path_auto)
        else:
            self.button_choose_folder.setText("选择QPT程序")
            self.text_input_path.setText(self.path_select)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = Welcome()
    welcome.show()
    sys.exit(app.exec_())
