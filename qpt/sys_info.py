# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import platform
import os
from qpt.kernel.tools.qlog import Logging


def check_bit():
    arc = platform.machine()
    Logging.debug(f"操作系统位数：{arc}")
    assert "64" in arc, "当前QPT不支持32位操作系统"


def check_os():
    p_os = platform.system()
    if p_os is None:
        return 0
    Logging.debug(f"操作系统类型：{p_os}")
    assert "Windows" in p_os, "当前QPT只支持Windows系统"


def req_site_packages_path():
    import pip
    site_package_path = os.path.dirname(os.path.dirname(pip.__file__))
    return site_package_path


def get_env_vars(work_dir="."):
    """
    获取当前待设置的环境变量字典
    :param work_dir:
    :return: dict
    """
    env_vars = dict()
    # Set PATH ENV
    path_env = os.environ.get("path").split(";")
    ignore_env_field = ["conda", "Conda", "Python", "python"]
    pre_add_env = os.path.abspath("./Python/Lib/site-packages") + ";" + \
                  os.path.abspath("./Python/Lib") + ";" + \
                  os.path.abspath("./Python/Lib/ext") + ";" + \
                  os.path.abspath("./Python") + ";" + \
                  os.path.abspath("./Python/Scripts") + ";"

    for pe in path_env:
        if pe:
            add_flag = True
            for ief in ignore_env_field:
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
    return env_vars


SITE_PACKAGE_PATH = req_site_packages_path()

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


# 需考虑Run避免无法记录进日志的情况
if QPT_MODE == "Run":
    check_all()
elif QPT_MODE == "Debug":
    check_all()
