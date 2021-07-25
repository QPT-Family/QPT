# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import unittest

from qpt.executor import CreateExecutableModule
from qpt.modules.package import ONLINE_DEPLOY_MODE

from qpt.kernel.tools.interpreter import set_default_pip_source


# set_default_pip_source("https://mirror.baidu.com/pypi/simple")

class LogTest(unittest.TestCase):
    def test_module_m(self):
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path="./unit_out/mini",
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_m_gui(self):
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path="./unit_out/mini_gui",
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    def test_module_paddle(self):
        module = CreateExecutableModule(work_dir="./sandbox",
                                        launcher_py_path="./sandbox/run.py",
                                        save_path="./unit_out/paddle-cpu",
                                        requirements_file="./sandbox/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_paddle_gpu(self):
        module = CreateExecutableModule(work_dir="./sandbox_paddle_gpu",
                                        launcher_py_path="./sandbox_paddle_gpu/run.py",
                                        save_path="./unit_out/paddle-gpu",
                                        requirements_file="sandbox_paddle_gpu/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_tk(self):
        module = CreateExecutableModule(work_dir="./sandbox_tk",
                                        launcher_py_path="./sandbox_tk/run.py",
                                        save_path="./unit_out/tk_m",
                                        with_debug=True,
                                        hidden_terminal=False)
        module.make()

    def test_module_qt(self):
        module = CreateExecutableModule(work_dir="./sandbox_qt",
                                        launcher_py_path="./sandbox_qt/run.py",
                                        save_path="./unit_out/qt_m",
                                        requirements_file="sandbox_qt/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=True)
        module.make()

    def test_module_online_paddle(self):
        module = CreateExecutableModule(work_dir="./sandbox",
                                        launcher_py_path="./sandbox/run.py",
                                        save_path="./unit_out/paddle-cpu-online",
                                        requirements_file="./sandbox/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False,
                                        deploy_mode=ONLINE_DEPLOY_MODE)
        module.make()
