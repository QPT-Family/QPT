# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import unittest
import sys
import os

from qpt.executor import CreateExecutableModule
from qpt.modules.package import ONLINE_DEPLOY_MODE
from qpt.modules.python_env import Python37, Python38, Python39

# from qpt.kernel.tools.interpreter import set_default_pip_source
# set_default_pip_source("https://mirror.baidu.com/pypi/simple")

# 测试时需要手动修改，挺费硬盘的其实
OUT_DIR_ROOT = r"M:\QPT_UT_OUT_CACHE"

os.makedirs(OUT_DIR_ROOT, exist_ok=True)


class LogTest(unittest.TestCase):
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

    # 验证no debug
    def test_module_m_not_debug(self):
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        with_debug=False,
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

    def test_module_m_gui_python37(self):
        # 验证Python兼容性
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        interpreter_module=Python37(),
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_m_gui_python38(self):
        # 验证Python兼容性
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        interpreter_module=Python38(),
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_m_gui_python39(self):
        # 验证Python兼容性
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        interpreter_module=Python39(),
                                        with_debug=True,
                                        hidden_terminal=False)
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

    # def test_module_paddle_gpu(self):
    #     # 验证CUDA
    #     module = CreateExecutableModule(work_dir="./sandbox_paddle_gpu",
    #                                     launcher_py_path="./sandbox_paddle_gpu/run.py",
    #                                     save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
    #                                     requirements_file="sandbox_paddle_gpu/requirements_with_opt.txt",
    #                                     with_debug=True,
    #                                     hidden_terminal=False)
    #     module.make()

    def test_module_tk(self):
        # 验证TK
        module = CreateExecutableModule(work_dir="./sandbox_tk",
                                        launcher_py_path="./sandbox_tk/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_qt(self):
        # 验证QT
        module = CreateExecutableModule(work_dir="./sandbox_qt",
                                        launcher_py_path="./sandbox_qt/run.py",
                                        save_path=os.path.join(OUT_DIR_ROOT, sys._getframe().f_code.co_name),
                                        requirements_file="sandbox_qt/requirements_with_opt.txt",
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
                                        deploy_mode=ONLINE_DEPLOY_MODE)
        module.make()
