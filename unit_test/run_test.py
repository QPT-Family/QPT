# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import sys
import unittest

# 测试Action 模式
os.environ["QPT_Action"] = "True"

from qpt.executor import CreateExecutableModule
from qpt.modules.package import DISPLAY_ONLINE_INSTALL
from qpt.modules.python_env import *

# from qpt.kernel.tools.interpreter import set_default_pip_source
# set_default_pip_source("https://mirror.baidu.com/pypi/simple")

# 测试时需要手动修改，挺费硬盘的其实
OUT_DIR_ROOT = r"J:\QPT_UT_OUT_CACHE"

os.makedirs(OUT_DIR_ROOT, exist_ok=True)


class LogTest(unittest.TestCase):

    def test_module_m_gui_python38(self):
        # 验证Python兼容性
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        interpreter_version=38,
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    def test_module_m_gui_python39(self):
        # 验证Python兼容性
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        interpreter_version=39,
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    def test_module_m_gui_python310(self):
        # 验证Python兼容性
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        interpreter_version=310,
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    def test_module_m_gui_python311(self):
        # 验证Python兼容性
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        interpreter_version=311,
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    def test_module_m_gui_python312(self):
        # 验证Python兼容性
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        interpreter_version=312,
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    def test_module_paddle(self):
        # 验证Paddle
        module = CreateExecutableModule(work_dir="./sandbox",
                                        launcher_py_path="./sandbox/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="./sandbox/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_paddle_gpu(self):
        # 验证CUDA
        module = CreateExecutableModule(work_dir="./sandbox_paddle_gpu",
                                        launcher_py_path="./sandbox_paddle_gpu/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        # requirements_file="sandbox_paddle_gpu/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_qt(self):
        # 验证QT
        module = CreateExecutableModule(work_dir="./sandbox_qt",
                                        launcher_py_path="./sandbox_qt/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        # requirements_file="sandbox_qt/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    def test_module_online_paddle(self):
        # 验证在线安装
        module = CreateExecutableModule(work_dir="./sandbox",
                                        launcher_py_path="./sandbox/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="./sandbox/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False,
                                        deploy_mode=DISPLAY_ONLINE_INSTALL)
        module.make()
