from qpt import sys_info
from qpt import executor
from qpt import modules
from qpt.kernel.tools.qlog import Logging

try:
    import ctypes
except Exception as e:
    Logging.error(f"当前操作系统存在运行库组件漏洞，请下载国内主流杀毒软件并修复所有Windows漏洞，完整报错信息如下：\n"
                  f"{e}")
