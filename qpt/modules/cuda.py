# Author: Acer Zhang
# Datetime: 2021/7/12
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import sys

from qpt.kernel.tools.os_op import copytree
from qpt.kernel.tools.log_op import Logging
from qpt.modules.base import SubModule, SubModuleOpt


class CopyCUDADLL(SubModuleOpt):
    def __init__(self, cuda_version):
        super(CopyCUDADLL, self).__init__()
        self.cuda_version = cuda_version

    def act(self) -> None:
        if self.cuda_version is None:
            raise Exception("暂不接受不指定版本的情况")
        else:
            version = self.cuda_version.split(".")
            assert len(version) == 2, "CUDA版本号需要为以下格式传入：主版本号.从版本号，例如11.0"
            base_path = os.environ.get(f"CUDA_PATH_V{version[0]}_{version[1]}")
            bin_path = os.path.join(base_path, "bin")
            if not os.path.exists(bin_path):
                raise FileNotFoundError(f"当前环境的{os.path.abspath(bin_path)}目录下无CUDA驱动，无法封装。")
            copytree(bin_path, os.path.join(self.module_path, "opt/CUDA"), ignore_files=["compute-sanitizer.bat"])


class SetCUDAEnv(SubModuleOpt):
    def __init__(self):
        super(SetCUDAEnv, self).__init__()

    def act(self) -> None:
        cuda_path = os.path.join(os.path.abspath(self.module_path), "opt/CUDA")
        os.environ["PATH"] += ";" + cuda_path
        sys.path.append(cuda_path)


class CopyCUDAPackage(SubModule):
    def __init__(self, cuda_version):
        super(CopyCUDAPackage, self).__init__()
        self.add_pack_opt(CopyCUDADLL(cuda_version=cuda_version))
        self.add_unpack_opt(SetCUDAEnv())
