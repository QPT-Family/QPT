from qpt.modules.base import SubModule, SubModuleOpt
from qpt.kernel.tools.qpt_venv import VirtualEnv

virtualenv = VirtualEnv()


class CreatePythonEnv(SubModuleOpt):
    def act(self) -> None:
        pass


class Python38(SubModule):
    def __init__(self):
        super().__init__("Python3.8Env")
        pass


class Python39(SubModule):
    def __init__(self):
        super().__init__("Python3.9Env")
        pass
