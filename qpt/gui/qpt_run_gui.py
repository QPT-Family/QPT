import sys

from PyQt5.QtWidgets import QApplication


def run_gui(gui_class):
    app = QApplication(sys.argv)
    gui_class = gui_class()
    gui_class.show()
    sys.exit(app.exec_())
