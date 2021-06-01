import shutil
import ctypes
import os
import sys
import tempfile
import io
from importlib import util

from qpt.kernel.tools.log_op import Logging


def dynamic_load_package(packages_name, lib_packages_path):
    """
    动态加载Python包
    :param packages_name: 包名
    :param lib_packages_path: site-packages路径/包所在的目录
    :return: Python包
    """
    module_spec = util.find_spec(packages_name, lib_packages_path)
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


def download(url, file_name, path=None, clean=False):
    import wget
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, file_name)
    if not os.path.exists(file_path) or clean:
        try:
            wget.download(url, file_path)
        except Exception as e:
            Logging.error(f"无法下载文件，请检查网络是否可以连接以下链接\n"
                          f"{url}\n"
                          f"若该文件由QPT提供，请升级QPT版本，若版本升级后仍未解决可在以下地址提交issue反馈该情况\n"
                          f"https://github.com/GT-ZhangAcer/QPT/issues")
            raise Exception("文件下载失败，报错如下：" + str(e))


def get_qpt_tmp_path(dir_name="Cache", clean=False):
    """
    获取一个临时目录
    :param dir_name: 临时目录名
    :param clean: 是否强制清空目录
    :return: 目录路径
    """
    base_path = tempfile.gettempdir()
    dir_path = os.path.join(base_path, "QPT_Cache", dir_name)
    if os.path.exists(dir_path) and clean:
        shutil.rmtree(dir_path)
    else:
        os.makedirs(dir_path, exist_ok=True)
    return dir_path


def clean_qpt_cache():
    base_path = tempfile.gettempdir()
    dir_path = os.path.join(base_path, "QPT_Cache")
    shutil.rmtree(dir_path)


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
        if self.container is not None:
            self.container.append(output_stream)

    def flush(self):
        self.buff = ''


class FileSerialize:
    def __init__(self, file_path):
        with open(file_path, "rb")as file:
            self._data = file.read()

    def get_data(self):
        return self._data

    @staticmethod
    def serialize2file(data):
        tmp_path = get_qpt_tmp_path()
        file_path = os.path.join(tmp_path, "FileSerialize.tmp")
        with open(file_path, "wb") as file:
            file.write(data)
        return file_path
