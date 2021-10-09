import sys

from PyQt5.QtWidgets import QApplication, QWidget

from qpt.kernel.qt_ui.mini_about import Ui_mini_about


class MiniAbout(QWidget, Ui_mini_about):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, unzip_file_dialog):
        super().setupUi(unzip_file_dialog)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = MiniAbout()
    welcome.show()
    sys.exit(app.exec_())
