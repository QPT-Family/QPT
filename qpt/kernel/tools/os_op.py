import shutil
import subprocess
import ctypes
import os
import sys
import tempfile

import wget

from qpt.kernel.tools.log_op import Logging


def add_ua():
    """
    获取UA权限
    """
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


def set_qpt_env_var(path):
    # ToDO:可考虑用Win32代替
    out = os.system(f'setx "QPT_BASE" {path} /m')
    if out == 0:
        return True
    else:
        return False


def download(url, path, file_name, clean=False):
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, file_name)
    if not os.path.exists(file_path) or clean:
        wget.download(url, out=file_path)


def get_qpt_tmp_path(dir_name, clean=False):
    base_path = tempfile.gettempdir()
    dir_path = os.path.join(base_path, "QPT_Cache", dir_name)
    if os.path.exists(dir_path) and clean:
        shutil.rmtree(dir_path)
    return dir_path


