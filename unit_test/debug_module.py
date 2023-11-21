# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

if __name__ == '__main__':
    M_PATH = r"J:\QPT_UT_OUT_CACHE\test_module_m\Debug"
    os.chdir(M_PATH)
    from qpt.run_wrapper import wrapper

    wrapper()
    from qpt.executor import RunExecutableModule

    RunExecutableModule().run()
