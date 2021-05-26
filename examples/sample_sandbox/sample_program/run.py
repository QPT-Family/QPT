import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


class Example(QWidget):
    def __init__(self):
        super().__init__()
        QMessageBox.information(self, '测试结果', '测试成功',
                                QMessageBox.Yes)


app = QApplication(sys.argv)
ex = Example()
ex.close()
sys.exit(app.exec_())
