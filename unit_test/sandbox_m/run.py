import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

app = QApplication(sys.argv)
widget = QWidget()
msg = QMessageBox.information(widget, '测试结果', '测试成功',
                              QMessageBox.Yes)
widget.close()
