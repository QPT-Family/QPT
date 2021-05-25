import os
import sys
import zipfile
from tempfile import TemporaryDirectory

from qpt.modules.base import SubModule, SubModuleOpt
from qpt.kernel.tools.log_tools import Logging
from qpt.kernel.tools.sys_tools import download

"""
Python镜像打包指南
1. 下载嵌入式版本Python
2. 在Python文档或ext文件夹下获取get-pip.py
3. 安装pip
4. LZMA-64-64 zip格式上传至文件床，必要时设置密码
"""


class PackPythonEnv(SubModuleOpt):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def act(self) -> None:
        with TemporaryDirectory() as dir_name:
            Logging.info(f"正在下载Python解释器原文件至{dir_name}")
            download(self.url, dir_name, "Python.zip")
            zip_path = os.path.join(dir_name, "Python.zip")
            # 解压至输出文件夹
            with zipfile.ZipFile(zip_path) as zip_obj:
                zip_obj.extractall(os.path.join(self.save_path, "Python"), pwd="gt_qpt".encode("utf-8"))


class UnPackPythonEnv(SubModuleOpt):
    def __init__(self):
        super().__init__()

    def act(self) -> None:
        # 添加Python以及Python/lib/python/site_packages_path下的包到环境变量/工作目录
        python_path = self.interpreter_path
        site_packages_path = os.path.join(self.interpreter_path, "lib/site-packages")
        script_path = os.path.join(self.interpreter_path, "Scripts")
        sys.path.append(python_path)
        sys.path.append(site_packages_path)
        sys.path.append(script_path)


class Python38(SubModule):
    def __init__(self):
        super().__init__("Python3.8Env")
        url = "https://bj.bcebos.com/v1/ai-studio-online/000b6ef8041b4e8f9a081369c1cad85938689722428b451" \
              "c850c19133f293347?responseContentDisposition=attachment%3B%20filename%3DPython%233.8%23.zip"
        self.add_pack_opt(PackPythonEnv(url))
        self.add_unpack_opt(UnPackPythonEnv())

# class Python39(SubModule):
#     def __init__(self):
#         super().__init__("Python3.9Env")
#         url = "https://bj.bcebos.com/v1/ai-studio-online/000b6ef8041b4e8f9a081369c1cad85938689722428b451" \
#               "c850c19133f293347?responseContentDisposition=attachment%3B%20filename%3DPython%233.8%23.zip"
#         self.add_pack_opt(PackPythonEnv(url))
#         self.add_unpack_opt(UnPackPythonEnv())
