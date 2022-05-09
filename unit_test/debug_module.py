# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

M_PATH = r"M:\QPT_UT_OUT_CACHE\test_module_m_gui_python37\Debug"
os.chdir(M_PATH)
from qpt.executor import RunExecutableModule

if __name__ == '__main__':
    module = RunExecutableModule(M_PATH)
    module.run()
