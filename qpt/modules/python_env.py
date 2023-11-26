import os

from qpt.kernel.qlog import Logging
from qpt.kernel.qos import copytree, check_and_install_sdk_in_this_env
from qpt.modules.base import SubModule, SubModuleOpt, TOP_LEVEL

PYTHON_ENV_MODE_SPEED_FIRST = "预先解压好Python环境，占用部分硬盘资源但能减少用户使用时速度损失"
PYTHON_ENV_MODE_PACKAGE_VOLUME_FIRST = "[暂不支持]封装后保留压缩的Python环境以减少硬盘资源占用"
PYTHON_ENV_MODE_ONLINE_INSTALLATION = "[暂不支持]不封装Python环境，用户使用时在线进行下载并部署"
DEFINE_PYTHON_ENV_MODE = PYTHON_ENV_MODE_SPEED_FIRST

SUPPORT_PYTHON_VERSION = [38, 39, 310, 311, 312]


class PackPythonEnvOpt(SubModuleOpt):
    def __init__(self, version: int, mode=PYTHON_ENV_MODE_SPEED_FIRST):
        super().__init__()
        self.version = version
        self.mode = mode

    def act(self) -> None:
        # ToDo 增加版本控制
        m = f"python{self.version}"
        path = check_and_install_sdk_in_this_env(f"QEnvPython{self.version}")
        copytree(os.path.join(os.path.join(path, "QEnvPython"), m), os.path.join(self.module_path, "Python"))

        # ToDo 未来对Tinkter和VC2019进行分离，先暂时放一起
        m = f"tkinter{self.version}"
        path = check_and_install_sdk_in_this_env(f"QEnvPython{self.version}")
        copytree(os.path.join(os.path.join(path, "QEnvPython"), m), os.path.join(self.module_path, "Python"))

        m = "vcredist"
        path = check_and_install_sdk_in_this_env("QVCRedist")
        copytree(os.path.join(os.path.join(path, "QVCRedist"), m), os.path.join(self.module_path, "Python"))


class BasePythonEnv(SubModule):
    def __init__(self, name, version: int, mode=DEFINE_PYTHON_ENV_MODE):
        if version not in SUPPORT_PYTHON_VERSION:
            if version < SUPPORT_PYTHON_VERSION[0]:
                n_version = SUPPORT_PYTHON_VERSION[0]
            else:
                n_version = SUPPORT_PYTHON_VERSION[-1]
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
                            f"已强制设置目标版本号为{n_version}，请检查存在以下兼容性问题：\n"
                            f"1. 需考虑待打包的代码是否兼容该Python版本\n"
                            f"2. 该Python版本是否可以在目标用户操作系统上执行\n"
                            f"----------------------------------------------------------------------\n")
            version = n_version

        super().__init__(name, level=TOP_LEVEL)
        self.add_pack_opt(PackPythonEnvOpt(version=version, mode=mode))


class AutoPythonEnv(BasePythonEnv):
    def __init__(self, mode=DEFINE_PYTHON_ENV_MODE):
        import platform
        version = platform.python_version_tuple()
        version = "".join(version[0:2])
        Logging.info(f"当前解释器版本为Python{version}，正在向QPT查询是否存在合适的Python镜像...")
        # 截断版本号，只保留两位

        super().__init__(name="interpreter", mode=mode, version=int(version))
