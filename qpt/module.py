import click
from qpt.kernel.sub_modules.base_sub_module import BaseSubModule


class CreateModule:
    def __init__(self,
                 py_file_path,
                 workdir,
                 save_dir,
                 version="1.0",
                 requirements_file_path="Auto",
                 none_gui: bool = False):
        self.save_dir = save_dir
        pass

    def add_workdir(self, path):
        pass

    def add_files(self, file, workdir=None):
        pass

    def add_sub_module(self, sub_module: BaseSubModule):
        # ToDO 对每个module设置save_dir
        pass

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
