# Author: Acer Zhang
# Datetime: 2021/6/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore

from qpt.kernel.qt_ui.unzip import Ui_unzip_file_dialog


class Unzip(QWidget, Ui_unzip_file_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def update_value(self, value):
        if not isinstance(value, int):
            value = int(value)
        self.progressBar.setValue(value)

    def update_title(self, text: str):
        self.setWindowTitle(text)


if __name__ == '__main__':
    import time

    app = QApplication(sys.argv)
    unz = Unzip()
    unz.show()
    for i in range(15):
        time.sleep(1)
        unz.update_value(i)
        app.processEvents()

    sys.exit(app.exec_())
