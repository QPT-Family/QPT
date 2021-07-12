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
    Logging.info("UA请求完毕")


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


class StdOutLoggerWrapper:
    def __init__(self, log_file_path):
        self.ori_stout = sys.stdout
        self.log_file = open(log_file_path, "w", encoding="utf-8", buffering=1)

    def write(self, output_stream):
        self.ori_stout.write(output_stream)
        self.log_file.write(output_stream)

    def flush(self):
        self.ori_stout.flush()

    def close_file(self):
        self.log_file.close()

    def isatty(self):
        return True


def copytree(src, dst, ignore_dirs: list = None, ignore_files: list = None):
    """
    复制整个目录树
    最开始是用shutil.copytree()，但奈何Python3.7和3.8差别挺大，算了忽略这点效率吧，反正是在打包过程中，不影响用户
    :param src: 源路径
    :param dst: 目标路径
    :param ignore_dirs: 忽略的文件夹名
    :param ignore_files: 忽略的文件名
    """
    if ignore_dirs is None:
        rel_ignore_dirs = list()
    else:
        rel_ignore_dirs = [os.path.relpath(os.path.abspath(d), src) for d in ignore_dirs]
    if ignore_files is None:
        ignore_files = list()
    else:
        ignore_files = [os.path.abspath(os.path.join(src, f)) for f in ignore_files]
    if not os.path.exists(dst):
        os.makedirs(dst)

    if os.path.exists(src):
        dir_cache = "-%NONE-FLAG%-"
        for root, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root, src)
            if rel_path in rel_ignore_dirs:
                dir_cache = os.path.relpath(root, src)
                continue
            if dir_cache in rel_path and rel_path.index(dir_cache) == 0:
                continue
            dst_root = os.path.join(os.path.abspath(dst),
                                    os.path.abspath(root).replace(os.path.abspath(src), "").strip("\\"))
            for file in files:
                src_file = os.path.join(root, file)
                if os.path.abspath(src_file) in ignore_files:
                    continue
                dst_file = os.path.join(dst_root, file)
                if not os.path.exists(dst_root):
                    os.makedirs(dst_root, exist_ok=True)
                shutil.copy(src_file, dst_file)


def check_chinese_char(text):
    for t in text:
        if u'\u4e00' <= t <= u'\u9fff':
            return True
    return False


class FileSerialize:
    def __init__(self, file_path):
        with open(file_path, "r", encoding="utf-8")as file:
            self._data = file.read()

    def get_serialize_data(self):
        return self._data

    @staticmethod
    def serialize2file(data):
        tmp_path = get_qpt_tmp_path()
        file_path = os.path.join(tmp_path, "FileSerialize.tmp")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)
        return file_path
