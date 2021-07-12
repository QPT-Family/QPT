import os
import sys
import zipfile

from qpt.modules.base import SubModule, SubModuleOpt, TOP_LEVEL
from qpt.modules.package import set_default_package_for_python_version
from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.os_op import download, get_qpt_tmp_path
from qpt._compatibility import com_configs

"""
Python镜像打包指南
1. 下载嵌入式版本Python
2. 在Python文档或ext文件夹下获取get-pip.py
3. 安装pip
4. 使用LZMA-64-64 zip的格式上传至文件床，必要时设置密码
"""

PYTHON_ENV_MODE_SPEED_FIRST = "预先解压好Python环境，占用部分硬盘资源但能减少用户使用时速度损失"
PYTHON_ENV_MODE_PACKAGE_VOLUME_FIRST = "[暂不支持]封装后保留压缩的Python环境以减少硬盘资源占用"
PYTHON_ENV_MODE_ONLINE_INSTALLATION = "[暂不支持]不封装Python环境，用户使用时在线进行下载并部署"
DEFINE_PYTHON_ENV_MODE = PYTHON_ENV_MODE_SPEED_FIRST

RESOURCES_URLS = {"Python3.7Env": "https://bj.bcebos.com/v1/ai-studio-online/90d3e6c134c5425394178839aed9b0351"
                                  "586bf4dec46451d8e5e10ac54723064?responseContentDisposition=attachment%3B%20"
                                  "filename%3DPython3.7.9-vc2019.zip",
                  "Python3.8Env": "https://bj.bcebos.com/v1/ai-studio-online/f254c18b13654d3da11ddf855277812c3"
                                  "b52aa55bd574b979d8a3999aa14a155?responseContentDisposition=attachment%3B%20"
                                  "filename%3DPython3.8.10-vc2019.zip",
                  "Python3.9Env": "https://bj.bcebos.com/v1/ai-studio-online/2fd4ef0f3432448f8da656434097d0861"
                                  "308da335cf44da28c08a3f8ace766fe?responseContentDisposition=attachment%3B%20"
                                  "filename%3DPython3.9.5-vc2019.zip"}

DEFAULT_PYTHON_IMAGE_VERSION = "3.8"


class PackPythonEnvOpt(SubModuleOpt):
    def __init__(self, url: str = None, mode=PYTHON_ENV_MODE_SPEED_FIRST):
        super().__init__()
        self.url = url
        self.mode = mode

    def act(self) -> None:
        if self.mode == PYTHON_ENV_MODE_SPEED_FIRST:
            dir_name = get_qpt_tmp_path(os.path.join("Python", "".join(list(filter(str.isdigit, self.url)))[-10:]))
            Logging.info(f"正在加载Python解释器原文件至{dir_name}")
            download(self.url, "Python.zip", dir_name)
            zip_path = os.path.join(dir_name, "Python.zip")
            # 解压至输出文件夹
            with zipfile.ZipFile(zip_path) as zip_obj:
                zip_obj.extractall(os.path.join(self.module_path, "Python"), pwd="gt_qpt".encode("utf-8"))
        elif self.mode == PYTHON_ENV_MODE_PACKAGE_VOLUME_FIRST:
            Logging.info(f"正在加载Python解释器原文件")
            download(self.url, "Python.zip", self.module_path)
        elif self.mode == PYTHON_ENV_MODE_ONLINE_INSTALLATION:
            pass


class UnPackPythonEnvOpt(SubModuleOpt):
    def __init__(self, url: str = None, mode=PYTHON_ENV_MODE_SPEED_FIRST):
        super().__init__()
        self.url = url
        self.mode = mode

    def act(self) -> None:
        if self.mode == PYTHON_ENV_MODE_SPEED_FIRST:
            pass
        elif self.mode == PYTHON_ENV_MODE_PACKAGE_VOLUME_FIRST:
            zip_path = os.path.join(self.module_path, "Python.zip")
            # 解压至输出文件夹
            with zipfile.ZipFile(zip_path) as zip_obj:
                zip_obj.extractall(os.path.join(self.module_path, "Python"), pwd="gt_qpt".encode("utf-8"))
        elif self.mode == PYTHON_ENV_MODE_ONLINE_INSTALLATION:
            dir_name = get_qpt_tmp_path(os.path.join("Python", "".join(list(filter(str.isdigit, self.url)))[-10:]))
            Logging.debug(f"正在下载Python解释器原文件至{dir_name}")
            download(self.url, "Python.zip", dir_name)
            zip_path = os.path.join(dir_name, "Python.zip")
            # 解压至输出文件夹
            with zipfile.ZipFile(zip_path) as zip_obj:
                zip_obj.extractall(os.path.join(self.module_path, "Python"), pwd="gt_qpt".encode("utf-8"))

        # 添加Python以及Python/lib/python/site_packages_path下的包到环境变量/工作目录
        python_path = self.interpreter_path
        site_packages_path = os.path.join(self.interpreter_path, com_configs["RELATIVE_INTERPRETER_SITE_PACKAGES_PATH"])
        script_path = os.path.join(self.interpreter_path, "Scripts")
        sys.path.append(python_path)
        sys.path.append(site_packages_path)
        sys.path.append(script_path)


class BasePythonEnv(SubModule):
    def __init__(self, name, version=None, mode=DEFINE_PYTHON_ENV_MODE, url=None):
        if version:
            resources_name = f"Python{version}Env"
            if resources_name in RESOURCES_URLS:
                Logging.info(f"已在QPT中找到{resources_name}镜像")
            else:
                Logging.warning(f"----------------------------------------------------------------------\n"
                                f"未在QPT中找到{resources_name}镜像，QPT目前提供的Python镜像版本有限，\n"
                                f"请尽可能使用Python3.8/Python3.9等主流Python版本进行打包。\n"
                                f"----------------------------------------------------------------------\n"
                                f"已强制设置目标版本号为{DEFAULT_PYTHON_IMAGE_VERSION}，可能存在以下兼容性问题：\n"
                                f"1. Pip只接受具备对应版本的Whl依赖安装包。\n"
                                f"2. 如*.gz的非二进制依赖安装包等均可能无法直接通过当前环境下的Pip自动下载，可能需要手动下载对应包并使用pip安装至"
                                f"“输出目录/Python/Lib/site-packages”目录下\n"
                                f"----------------------------------------------------------------------\n")
                set_default_package_for_python_version(DEFAULT_PYTHON_IMAGE_VERSION)
            url = RESOURCES_URLS[resources_name]
        assert url and version, "请至少设置url和version中任一字段"
        super().__init__(name, level=TOP_LEVEL)
        self.add_pack_opt(PackPythonEnvOpt(url=url, mode=mode))
        self.add_unpack_opt(UnPackPythonEnvOpt(url=url, mode=mode))
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
