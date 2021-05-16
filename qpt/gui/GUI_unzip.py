import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from qpt.kernel.tools.qpt_model import GModule
from qpt.kernel.qt_ui.unzip import Ui_unzip_file_dialog

__all__ = ["GUIUnzip"]


def cancel():
    MainWindow.close()


class GUIUnzip(Ui_unzip_file_dialog):
    def __init__(self, q_windows, gdm_file_path):
        self.setupUi(q_windows)
        self.unzip(gdm_file_path)

    def setupUi(self, unzip_file_dialog):
        super(GUIUnzip, self).setupUi(unzip_file_dialog)
        self.exit_button.clicked.connect(cancel)

    def unzip(self, gdm_file_path):
        module = GModule(gdm_file_path)
        self.progressBar.setValue(0)
        module.load_module(self.progressBar, self.act_label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = GUIUnzip(MainWindow, "tmp.qpt")
    MainWindow.show()
    sys.exit(app.exec_())
