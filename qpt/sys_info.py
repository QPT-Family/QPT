# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import platform
import os
from qpt.kernel.tools.log_op import Logging


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


# QPT运行状态 Run/Debug
QPT_MODE = os.getenv("QPT_MODE")


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
