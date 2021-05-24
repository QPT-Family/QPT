from qpt.modules.base import SubModule, SubModuleOpt
from qpt.kernel.tools.qpt_venv import VirtualEnv

virtualenv = VirtualEnv()


class CreatePythonEnv(SubModuleOpt):
    def act(self) -> None:
        print("创建了个Python环境")


class Python38(SubModule):
    def __init__(self):
        super().__init__(name="Python3.8Env")
        self.add_pack_opt(CreatePythonEnv())
        self.add_unpack_opt(CreatePythonEnv())


class Python39(SubModule):
    def __init__(self):
        super().__init__(name="Python3.9Env")
        pass
