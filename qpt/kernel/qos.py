import shutil
import os
import sys
import tempfile
import io
from importlib import util

from qpt.kernel.qlog import Logging, TProgressBar
from qpt.memory import QPT_MEMORY
from qpt.version import version


def check_chinese_char(text):
    """
    判断是否包含中文，避免来自部分内鬼C++底层的Python包无缘无故报错
    :param text: 字符串
    :return: 是否包含
    """
    return not all(ord(char) < 128 for char in text)


TMP_BASE_PATH = os.path.join(tempfile.gettempdir(), f"QPT_Cache_V/{version}")
# Check User name is chinese
if check_chinese_char(TMP_BASE_PATH) or " " in TMP_BASE_PATH:
    TMP_BASE_PATH = "C:/q_tmp"
    Logging.warning(f"当前系统的用户名中包含中文/空格等可能会对程序造成异常的字符，现已默认QPT临时目录为{TMP_BASE_PATH}")
    os.makedirs(TMP_BASE_PATH, exist_ok=True)


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
    import ctypes
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
    """
    下载指定文件至目录
    :param url: 下载的URL
    :param file_name: 保存的文件名
    :param path: 保存路径
    :param clean: 是否情况旧的下载数据
    :return: 1代表全新数据，0代表使用缓存
    """
    import wget
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, file_name)
    if not os.path.exists(file_path) or clean:
        try:
            wget.download(url, file_path)
            return 1
        except Exception as e:
            Logging.error(f"无法下载文件，请检查网络是否可以连接以下链接\n"
                          f"{url}\n"
                          f"若该文件由QPT提供，请升级QPT版本，若版本升级后仍未解决可在以下地址提交issue反馈该情况\n"
                          f"https://github.com/GT-ZhangAcer/QPT/issues")
            raise Exception("文件下载失败，报错如下：" + str(e))
    else:
        return 0


def get_qpt_tmp_path(dir_name="Cache", clean=False):
    """
    获取一个临时目录
    :param dir_name: 临时目录名
    :param clean: 是否强制清空目录
    :return: 目录路径
    """
    dir_path = os.path.join(TMP_BASE_PATH, dir_name)
    if os.path.exists(dir_path) and clean:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)
    else:
        os.makedirs(dir_path, exist_ok=True)
    return dir_path


def clean_qpt_cache():
    dir_path = TMP_BASE_PATH
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
        rel_ignore_dirs = list()
        for d in ignore_dirs:
            try:
                rel_ignore_dirs.append(os.path.relpath(os.path.abspath(d), src))
            except ValueError:
                continue
    if ignore_files is None:
        ignore_files = list()
    else:
        ignore_files = [os.path.abspath(os.path.join(src, f)) for f in ignore_files]
    if not os.path.exists(dst):
        os.makedirs(dst)

    copy_info = dict()
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
                copy_info[src_file] = dst_file

        progressbar = TProgressBar(msg="正在拷贝文件", max_len=len(copy_info) + 1)
        for k_id, k in enumerate(copy_info):
            shutil.copy(k, copy_info[k])
            progressbar.step()


class FileSerialize:
    def __init__(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
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


def warning_msg_box(title="Warning - GitHub: QPT-Family/QPT", text="", force=False):
    """
    发出警告框
    :param title: 标题
    :param text: 文本
    :param force: 是否强制只有确定按钮
    :return: 用户反馈
    """
    win32api = QPT_MEMORY.get_win32api
    win32con = QPT_MEMORY.get_win32con
    if force:
        flag = win32con.MB_OK | win32con.MB_ICONEXCLAMATION
    else:
        flag = win32con.MB_OKCANCEL | win32con.MB_ICONEXCLAMATION
    msg = win32api.MessageBox(0, text, title, flag)
    if not force and msg == 2:
        return False
    else:
        return True