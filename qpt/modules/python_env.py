import os
import sys
import zipfile

from base import SubModule, SubModuleOpt


class PackPythonEnv(SubModuleOpt):
    def __init__(self, version: str = "3.8"):
        super().__init__()

    def act(self) -> None:
        # ToDO Download QPT-Python
        zip_path = ""
        # 解压至输出文件夹
        with zipfile.ZipFile(zip_path) as zip_obj:
            zip_obj.extractall(os.path.join(self.get_save_dir(), "Python"), pwd="gt_qpt".encode("utf-8"))


class UnPackPythonEnv(SubModuleOpt):
    def __init__(self, version: str = "3.8"):
        super().__init__()
        self.version = version

    def act(self) -> None:
        # 添加Python以及Python/lib/python/site_packages_path下的包到环境变量/工作目录
        python_path = self.get_interpreter_dir()
        site_packages_path = os.path.join(self.get_interpreter_dir(), "lib/python" + self.version + "site-packages")
        sys.path.append(python_path)
        sys.path.append(site_packages_path)


class Python38(SubModule):
    def __init__(self):
        super().__init__("Python3.8Env")
        version = "3.8"
        self.add_pack_opt(PackPythonEnv(version))
        self.add_unpack_opt(UnPackPythonEnv(version))


class Python39(SubModule):
    def __init__(self):
        super().__init__("Python3.9Env")
        version = "3.9"
        self.add_pack_opt(PackPythonEnv(version))
        self.add_unpack_opt(UnPackPythonEnv(version))
