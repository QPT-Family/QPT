# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

M_PATH = r"D:\Python_Projects\QPT\unit_test\unit_out\test_module_paddle\Debug"
os.chdir(M_PATH)
from qpt.executor import RunExecutableModule

if __name__ == '__main__':
    module = RunExecutableModule(M_PATH)
    module.run()
