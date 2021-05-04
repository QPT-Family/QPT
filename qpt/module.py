import click


class CreateModule:
    def __init__(self,
                 py_file_path,
                 workdir,
                 version="1.0",
                 requirements_file_path="Auto",
                 none_gui: bool = False):
        pass


class RunModule:
    def __init__(self, file_path):
        pass

    def load_module_config(self):
        pass

    def solve_qpt_base(self):
        pass

    def solve_package(self):
        pass

    def solve_workdir(self):
        pass

    def run_module(self):
        pass
