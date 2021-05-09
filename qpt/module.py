import click
from qpt.kernel.sub_modules.sub_module import SubModule


class CreateModule:
    def __init__(self,
                 main_py_path,
                 workdir,
                 save_dir,
                 version="1.0",
                 requirements_file_path="Auto",
                 none_gui: bool = False):
        # 初始化成员变量
        self.main_py_path = main_py_path
        self.work_dir = workdir
        self.version = version
        self.requirements_file_path = requirements_file_path
        self.none_gui = none_gui
        self.save_dir = save_dir

        # Module列表
        self.modules = list()

    def add_workdir(self, path):
        pass

    def add_files(self, file, workdir=None):
        pass

    def add_sub_module(self, sub_module: SubModule):
        """
        为Module添加子模块
        """
        # 需对每个module设置save_dir和终端
        # ToDO 增加终端
        sub_module.out_dir = self.save_dir
        self.modules.append(sub_module)

    def print_details(self):
        pass

    def make(self):
        pass


class RunModule:
    def __init__(self, file_path):
        pass

    def load_module_config(self):
        pass

    def solve_qpt_base(self):
        pass

    def solve_sub_module(self):
        pass

    def solve_package(self):
        pass

    def unzip_resources(self):
        pass

    def solve_workdir(self):
        pass

    def run_module(self):
        pass
