import os
import sys
import zipfile

from qpt.kernel.qlog import Logging
from qpt.kernel.qos import copytree
from qpt.memory import QPT_MEMORY
from qpt.modules.base import SubModule, SubModuleOpt, TOP_LEVEL

"""
Python镜像打包指南
1. 下载嵌入式版本Python
2. 删除__pycache__
3. ADD 运行库
4. 使用LZMA-64-64 zip的格式上传至文件床，必要时设置密码
"""

PYTHON_ENV_MODE_SPEED_FIRST = "预先解压好Python环境，占用部分硬盘资源但能减少用户使用时速度损失"
PYTHON_ENV_MODE_PACKAGE_VOLUME_FIRST = "[暂不支持]封装后保留压缩的Python环境以减少硬盘资源占用"
PYTHON_ENV_MODE_ONLINE_INSTALLATION = "[暂不支持]不封装Python环境，用户使用时在线进行下载并部署"
DEFINE_PYTHON_ENV_MODE = PYTHON_ENV_MODE_SPEED_FIRST

SUPPORT_PYTHON_VERSION = ["3.8", "3.9", "3.10", "3.11"]
DEFAULT_PYTHON_IMAGE_VERSION = "3.8"


class PackPythonEnvOpt(SubModuleOpt):
    def __init__(self, version: str = None, mode=PYTHON_ENV_MODE_SPEED_FIRST):
        super().__init__()
        self.version = ".".join(version.split('.')[:2])
        self.mode = mode

    def act(self) -> None:
        for _ in range(2):
            import QPT_SDK
            v = f"python{self.version.replace('.', '')}"
            if v not in QPT_SDK.__all__:
                QPT_MEMORY.pip_tool.pip_package_shell(package="QEnvPython", version=self.version)
            copytree(os.path.abspath(os.path.join(QPT_SDK.__file__, v)), os.path.join(self.module_path, "Python"))

            # ToDo 未来对Tinkter和VC2019进行分离，先暂时放一起
            v = f"tkinter{self.version.replace('.', '')}"
            if v not in QPT_SDK.__all__:
                QPT_MEMORY.pip_tool.pip_package_shell(package="QEnvPython", version=self.version)
            copytree(os.path.abspath(os.path.join(QPT_SDK.__file__, v)), os.path.join(self.module_path, "Python"))

            v = "vcredist"
            if v not in QPT_SDK.__all__:
                QPT_MEMORY.pip_tool.pip_package_shell(package="QEnvPython", version=self.version)
            copytree(os.path.abspath(os.path.join(QPT_SDK.__file__, v)), os.path.join(self.module_path, "Python"))


class BasePythonEnv(SubModule):
    def __init__(self, name, version, mode=DEFINE_PYTHON_ENV_MODE):
        if version not in SUPPORT_PYTHON_VERSION:
            Logging.warning(f"----------------------------------------------------------------------\n"
                            f"未在QPT中找到Python{version}镜像，QPT目前提供的Python镜像版本有限，\n"
                            f"请尽可能使用Python3.7~Python3.10等主流Python版本进行打包，兼容性如下。\n"
                            f"----------------------------------------------------------------------\n"
                            f"Python版本|XP Win7 Win8.1 Win10+\n"
                            f"Python37 | X   1     1      1  \n"
                            f"Python38 | X   1     -      1  \n"
                            f"Python39 | X   X     -      1  \n"
                            f"Python310| X   X     x      1  \n"
                            f"Python311| X   X     x      1  \n"
                            f"..."
                            f"完整说明详见：https://github.com/QPT-Family/QPT/blob/开发分支/examples/advanced/打包兼容性更强的Python解释器.md"
                            f"----------------------------------------------------------------------\n"
                            f"已强制设置目标版本号为{DEFAULT_PYTHON_IMAGE_VERSION}，请检查存在以下兼容性问题：\n"
                            f"1. 需考虑待打包的代码是否兼容该Python版本\n"
                            f"2. 该Python版本是否可以在目标用户操作系统上执行\n"
                            f"----------------------------------------------------------------------\n")
        super().__init__(name, level=TOP_LEVEL)
        self.add_pack_opt(PackPythonEnvOpt(version=version, mode=mode))
        self.python_version = "非标准的PythonSubModule，需指定版本号"


class AutoPythonEnv(BasePythonEnv):
    def __init__(self, mode=DEFINE_PYTHON_ENV_MODE):
        import platform
        version = platform.python_version()
        Logging.info(f"当前解释器版本为{version}，正在向QPT查询是否存在合适的Python镜像...")
        # 截断版本号，只保留两位
        version = "".join([v if version_index == 1 else v + "."
                           for version_index, v in enumerate(version.split(".")[:2])])
        super().__init__(name=None, url=None, mode=mode, version=version)


class Python37(BasePythonEnv):
    def __init__(self, mode=DEFINE_PYTHON_ENV_MODE):
        super().__init__(name=None, version="3.7", mode=mode)


class Python38(BasePythonEnv):
    def __init__(self, mode=DEFINE_PYTHON_ENV_MODE):
        super().__init__(name=None, version="3.8", mode=mode)


class Python39(BasePythonEnv):
    def __init__(self, mode=DEFINE_PYTHON_ENV_MODE):
        super().__init__(name=None, version="3.9", mode=mode)


class Python310(BasePythonEnv):
    def __init__(self, mode=DEFINE_PYTHON_ENV_MODE):
        super().__init__(name=None, version="3.9", mode=mode)
