import shutil
import ctypes
import os
import sys
import tempfile
import io
from importlib import util

import wget

from qpt.kernel.tools.log_op import Logging


def dynamic_load_package(packages_name, lib_packages_path):
    """
    动态加载Python包
    :param packages_name: 包名
    :param lib_packages_path: site-packages路径/包所在的目录
    :return: Python包
    """
    module_spec = util.find_spec("pip", lib_packages_path)
    module = util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


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
    else:
        os.makedirs(dir_path, exist_ok=True)
    return dir_path


class StdOutWrapper(io.TextIOWrapper):
    def __init__(self, container: list = None, do_print=True):
        super().__init__(io.BytesIO(), encoding="utf-8")
        self.buff = ''
        self.ori_stout = sys.stdout
        self.container = container
        self.do_print = do_print

    def write(self, output_stream):
        if self.do_print:
            self.buff += output_stream
        self.container.append(output_stream)

    def flush(self):
        self.buff = ''
