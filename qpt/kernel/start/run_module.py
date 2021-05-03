import os
import sys

sys.path.append("/")
os.chdir("/")
os.environ["PYTHONPATH"] = "D:/Python_Projects/QPT/venv/Lib/site-packages:D:/Python_Projects/QPT"

from PyQt5.QtWidgets import QApplication, QMainWindow

from qpt.gui import GUI_module_launcher, GUI_unzip

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 初始化Module读取窗口
    zip_window = QMainWindow()
    GUI_unzip.GUIUnzip(zip_window, "//tmp.qpt")
    zip_window.show()
    # 设置窗口不可用
    # zip_window.setEnabled(False)
    # 销毁窗口
    zip_window.close()
    # 启动Launcher窗口
    launcher_window = QMainWindow()
    gui_module_launcher = GUI_module_launcher.GUIModuleLauncher(launcher_window)
    launcher_window.show()
    sys.exit(app.exec_())
