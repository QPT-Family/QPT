import os
import shutil

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


def check_path_with_msg(window, path):
    if not os.path.exists(path):
        abs_path = os.path.abspath(path)
        QMessageBox.warning(window,
                            "路径检查",
                            f"当前路径{abs_path}不存在，请检查/修改该路径",
                            QMessageBox.Reset)
        return False
    else:
        return True


def write_path_with_msg(window, path):
    if os.path.exists(path):
        abs_path = os.path.abspath(path)
        out = QMessageBox.warning(window,
                                  "写入检查",
                                  f"当前路径{abs_path}已有文件，是否重置该目录",
                                  QMessageBox.Yes | QMessageBox.No,
                                  QMessageBox.Yes)
        if out == QMessageBox.Yes:
            shutil.rmtree(abs_path)
            os.mkdir(abs_path)
            return True
        elif out == QMessageBox.No:
            return True
        else:
            return False
    else:
        os.mkdir(path)
        return True
