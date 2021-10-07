# Author: Acer Zhang
# Datetime:2021/10/7 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import unittest
import sys
import os

from qpt.executor import CreateExecutableModule
from qpt.modules.package import ONLINE_DEPLOY_MODE
from qpt.modules.python_env import Python37, Python38, Python39

OUT_DIR_ROOT = r"M:\QPT_UT_OUT_CACHE"

os.makedirs(OUT_DIR_ROOT, exist_ok=True)


class LogTest(unittest.TestCase):
    def test_module_opencv(self):
        # 最小流程验证
        module = CreateExecutableModule(work_dir="./sandbox_opencv",
                                        launcher_py_path="./sandbox_opencv/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_opencv/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_qt_paddle(self):
        # 验证自动依赖搜索
        module = CreateExecutableModule(work_dir="./sandbox_qt_paddle",
                                        launcher_py_path="./sandbox_qt_paddle/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    # 验证no debug
    def test_module_m_not_debug(self):
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        with_debug=False,
                                        hidden_terminal=False)
        module.make()

    def test_module_m(self):
        # 最小流程验证
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_m_opt(self):
        # 临时流程验证
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        with_debug=True,
                                        icon=r"M:\ICON\i.ico",
                                        hidden_terminal=False)
        module.make()

    def test_module_m_gui(self):
        # GUI流程验证
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()