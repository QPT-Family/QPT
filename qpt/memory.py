# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import platform
import os
from distutils.sysconfig import get_python_lib

from qpt.kernel.qlog import Logging


def init_wrapper(func):
    @property
    def render(self):
        if func.__name__ in self.memory:
            out = self.memory[func.__name__]
        else:
            out = func(self)
            self.memory[func.__name__] = out
        return out

    return render


class QPTMemory:
    def __init__(self):
        self.memory = dict()

    def set_mem(self, name, variable):
        self.memory[name] = variable
        return variable

    def free_mem(self, name):
        self.memory.pop(name)

    @init_wrapper
    def platform_bit(self):
        arc = platform.machine()
        Logging.debug(f"操作系统位数：{arc}")
        return arc

    @init_wrapper
    def platform_os(self):
        p_os = platform.system()
        Logging.debug(f"操作系统类型：{p_os}")
        return p_os

    @init_wrapper
    def site_packages_path(self):
        site_package_path = os.path.abspath(get_python_lib())
        return site_package_path

    @init_wrapper
    def pip_tool(self):
        from qpt.kernel.qinterpreter import PipTools
        pip_tools = PipTools()
        return pip_tools

    @init_wrapper
    def get_win32con(self):
        import win32con
        return win32con

    @init_wrapper
    def get_win32api(self):
        import win32api
        return win32api


QPT_MEMORY = QPTMemory()


def check_bit():
    arc = QPT_MEMORY.platform_bit
    assert "64" in arc, "当前QPT不支持32位操作系统"


def check_os():
    p_os = QPT_MEMORY.platform_os
    assert "Windows" in p_os, "当前QPT只支持Windows系统"


IGNORE_ENV_FIELD = ["conda", "Conda", "Python", "python"]


def get_env_vars(work_dir="."):
    """
    获取当前待设置的环境变量字典
    :param work_dir:
    :return: dict
    """
    env_vars = dict()
    # Set PATH ENV
    path_env = os.environ.get("PATH").split(";")
    pre_add_env = os.path.abspath("./Python/Lib/site-packages") + ";" + \
                  os.path.abspath("./Python/Lib") + ";" + \
                  os.path.abspath("./Python/Lib/ext") + ";" + \
                  os.path.abspath("./Python") + ";" + \
                  os.path.abspath("./Python/Scripts") + ";"

    for pe in path_env:
        if pe:
            add_flag = True
            for ief in IGNORE_ENV_FIELD:
                if ief in pe:
                    add_flag = False
                    break
            if add_flag:
                pre_add_env += pe + ";"
    env_vars["PATH"] = pre_add_env

    # Set PYTHON PATH ENV
    env_vars["PYTHONPATH"] = os.path.abspath("./Python/Lib/site-packages") + ";" + \
                             work_dir + ";" + \
                             os.path.abspath("./Python")
    os_env = os.environ.copy()
    os_env.update(env_vars)

    return os_env


PYTHON_IGNORE_DIRS = [".idea", ".git", ".github", "venv"]

# 被忽略的Python包
IGNORE_PACKAGES = ["virtualenv", "pip", "setuptools", "cpython"]

# QPT运行状态 Run/Debug
QPT_MODE = os.getenv("QPT_MODE")

# QPT检测到的运行状态 Run/本地Run
QPT_RUN_MODE = None


class CheckRun:
    @staticmethod
    def make_run_file(configs_path):
        with open(os.path.join(configs_path, "run_act.lock"), "w") as f:
            f.write("Run Done")

    @staticmethod
    def check_run_file(configs_path):
        global QPT_RUN_MODE
        if QPT_RUN_MODE is None:
            QPT_RUN_MODE = os.path.exists(os.path.join(configs_path, "run_act.lock"))
        return QPT_RUN_MODE


def check_all():
    # 检查系统
    check_os()
    # 检查arc
    check_bit()


check_all()
