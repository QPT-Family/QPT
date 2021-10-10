# Author: Acer Zhang
# Datetime:2021/6/24 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# 设置镜像源
import os

from qpt import Logging
from qpt.kernel.qinterpreter import PIPTerminal, PipTools
from qpt.memory import QPT_MEMORY


def set_default_pip_source(source: str):
    QPT_MEMORY.pip_tool.source = source
    Logging.debug(f"已设置PIP镜像源为：{source}")


def set_default_pip_lib(interpreter_path: str):
    if not os.path.splitext(interpreter_path)[1]:
        interpreter_path = os.path.join(interpreter_path, "python.exe")
    QPT_MEMORY.pip_tool.pip_main = PIPTerminal(interpreter_path).shell_func()
    Logging.debug(f"已设置PIP跨版本编译模式，目标解释器路径为：{interpreter_path}")


def set_pip_configs(lib_package_path=None,
                    source: str = None):
    """
    设置全局pip工具组件
    :param lib_package_path: pip所在位置
    :param source: 镜像源地址
    """
    QPT_MEMORY.set_mem("pip_tool", PipTools(pip_path=lib_package_path, source=source))
