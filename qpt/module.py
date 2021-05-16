import os
import shutil
from typing import List

from qpt.kernel.sub_modules.base import SubModule
from qpt.kernel.sub_modules.python_env import Python38
from qpt.kernel.tools.qpt_qt import QTerminal, MessageBoxTerminalCallback


class CreateExecutableModule:
    def __init__(self,
                 main_py_path,
                 workdir,
                 save_dir,
                 sub_modules: List[SubModule] = None,
                 module_name="未命名模型",
                 version="未知版本号",
                 author="未知作者",
                 none_gui: bool = False):
        # 初始化成员变量
        self.main_py_path = os.path.abspath(main_py_path).strip(os.path.abspath(workdir))
        self.work_dir = workdir
        self.save_dir = save_dir
        self.sub_module = sub_modules if sub_modules is not None else list()
        self.configs = dict()
        self.configs["main_py_path"] = self.main_py_path
        self.configs["none_gui"] = none_gui
        self.configs["module_name"] = module_name
        self.configs["author"] = author
        self.configs["version"] = version
        self.configs["sub_module"] = list()

        # 额外的成员变量
        self.resources_path = os.path.join(self.save_dir, "resources")
        self.config_path = os.path.join(self.save_dir, "configs")
        self.config_file_path = os.path.join(self.save_dir, "configs", "configs.gt")
        self.dependent_file_path = os.path.join(self.save_dir, "configs", "dependent.gt")

    # ToDO 增加对子工作目录支持
    # def add_sub_workdir(self, path):
    #     pass

    def add_sub_module(self, sub_module: SubModule):
        """
        为Module添加子模块
        """
        # 需对每个module设置save_dir和终端
        # ToDO 增加终端
        sub_module.set_out_dir(self.save_dir)
        self.sub_module.append(sub_module)

    def print_details(self):
        for module in self.sub_module:
            print(module.__class__.__name__, module.details)

    def make(self):
        # 子模块添加默认支持
        if len(self.sub_module) == 0:
            self.add_sub_module(Python38())

        # 打印sub module信息
        self.print_details()

        # 创建基本环境目录
        if os.path.exists(self.save_dir):
            key = input(f"{os.path.abspath(self.save_dir)}已存在，是否清空该目录(Y/N):")
            if key.lower() == "y":
                shutil.rmtree(self.save_dir)
                os.mkdir(self.save_dir)
        else:
            os.mkdir(self.save_dir)

        # 复制资源文件
        assert not os.path.exists(self.work_dir), f"{os.path.abspath(self.work_dir)}不存在，请检查该路径是否正确"
        shutil.copytree(self.work_dir, self.resources_path, dirs_exist_ok=True)

        # 解析子模块
        for sub in self.sub_module:
            sub.pack()
            self.configs["sub_module"].append(sub.name)

        # 创建配置文件
        with open(self.config_path, "w", encoding="utf-8") as config_file:
            config_file.write(str(self.configs))

        # ToDO 复制启动器文件


class RunExecutableModule:
    def __init__(self, file_path):
        # 初始化Module信息
        self.base_dir = os.path.split(file_path)[0]
        self.config_path = os.path.join(self.base_dir, "configs")
        self.config_file_path = os.path.join(self.base_dir, "configs", "configs.gt")
        self.dependent_file_path = os.path.join(self.base_dir, "configs", "dependent.gt")
        self.workdir = os.path.join(self.base_dir, "resources")
        with open(self.config_file_path, "r", encoding="utf-8") as config_file:
            self.configs = eval(config_file.read())

        # 初始化终端
        self.terminal = QTerminal()

        # prepare
        self.solve_sub_module()

    def solve_qpt_env(self):
        pass

    def solve_python_env(self):
        pass

    def solve_sub_module(self):
        """
        执行子模块
        """
        sub_name_list = self.configs["sub_module"]
        for sub_name in sub_name_list:
            sub_module = SubModule(sub_name)
            sub_module.set_out_dir(self.base_dir)
            sub_module.set_terminal_func(
                self.terminal.shell_func(
                    callback=MessageBoxTerminalCallback()
                )
            )
            sub_module.unpack()

    def unzip_resources(self):
        pass

    def solve_workdir(self):
        pass

    def run(self):
        # solve_workdir
        pass
