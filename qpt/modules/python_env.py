import os
import sys
import zipfile

from qpt.modules.base import SubModule, SubModuleOpt, TOP_LEVEL
from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.os_op import download, get_qpt_tmp_path

"""
Python镜像打包指南
1. 下载嵌入式版本Python
2. 在Python文档或ext文件夹下获取get-pip.py
3. 安装pip
4. 使用LZMA-64-64 zip的格式上传至文件床，必要时设置密码
"""

PYTHON_ENV_MODE_SPEED_FIRST = "预先解压好Python环境，占用部分硬盘资源但能减少用户使用时速度损失"
PYTHON_ENV_MODE_PACKAGE_VOLUME_FIRST = "封装后保留压缩的Python环境以减少硬盘资源占用"
PYTHON_ENV_MODE_ONLINE_INSTALLATION = "不封装Python环境，用户使用时在线进行下载并部署"

RESOURCES_URLS = {"Python3.8Env": "https://bj.bcebos.com/v1/ai-studio-online/000b6ef8041b4e8f9a081"
                                  "369c1cad85938689722428b451c850c19133f293347?responseContentDisp"
                                  "osition=attachment%3B%20filename%3DPython%233.8%23.zip"}


class PackPythonEnvOpt(SubModuleOpt):
    def __init__(self, url: str = None, mode=PYTHON_ENV_MODE_SPEED_FIRST):
        super().__init__()
        self.url = url
        self.mode = mode

    def act(self) -> None:
        if self.mode == PYTHON_ENV_MODE_SPEED_FIRST:
            dir_name = get_qpt_tmp_path(os.path.join("Python", "".join(list(filter(str.isdigit, self.url)))[-10:]))
            Logging.info(f"正在下载Python解释器原文件至{dir_name}")
            download(self.url, dir_name, "Python.zip")
            zip_path = os.path.join(dir_name, "Python.zip")
            # 解压至输出文件夹
            with zipfile.ZipFile(zip_path) as zip_obj:
                zip_obj.extractall(os.path.join(self.module_path, "Python"), pwd="gt_qpt".encode("utf-8"))
        elif self.mode == PYTHON_ENV_MODE_PACKAGE_VOLUME_FIRST:
            Logging.info(f"正在下载Python解释器原文件")
            download(self.url, self.module_path, "Python.zip")
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
            download(self.url, dir_name, "Python.zip")
            zip_path = os.path.join(dir_name, "Python.zip")
            # 解压至输出文件夹
            with zipfile.ZipFile(zip_path) as zip_obj:
                zip_obj.extractall(os.path.join(self.module_path, "Python"), pwd="gt_qpt".encode("utf-8"))

        # 添加Python以及Python/lib/python/site_packages_path下的包到环境变量/工作目录
        python_path = self.interpreter_path
        site_packages_path = os.path.join(self.interpreter_path, "lib/site-packages")
        script_path = os.path.join(self.interpreter_path, "Scripts")
        sys.path.append(python_path)
        sys.path.append(site_packages_path)
        sys.path.append(script_path)


class BasePythonEnv(SubModule):
    def __init__(self, name, url, mode):
        super().__init__(name, level=TOP_LEVEL)
        self.add_pack_opt(PackPythonEnvOpt(url=url, mode=mode))
        self.add_unpack_opt(UnPackPythonEnvOpt(url=url, mode=mode))


class Python38(BasePythonEnv):
    def __init__(self, mode=PYTHON_ENV_MODE_SPEED_FIRST):
        url = RESOURCES_URLS["Python3.8Env"]
        super().__init__(name=None, url=url, mode=mode)
