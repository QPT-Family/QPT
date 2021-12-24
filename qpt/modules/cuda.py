# Author: Acer Zhang
# Datetime: 2021/7/12
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import sys

from qpt.kernel.qos import copytree
from qpt.modules.base import SubModule, SubModuleOpt


class SearchCUDA:
    def __init__(self):
        self.paths = dict()

    def search_sys(self):
        for a_v in range(9, 13):
            for b_v in range(5):
                path = os.environ.get(f"CUDA_PATH_V{a_v}_{b_v}")
                if path:
                    bin_path = os.path.join(path, "bin")
                    self.paths[str(a_v) + "." + str(b_v)] = bin_path

    def search_conda(self):
        pass

    def get_paths(self):
        return self.paths


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
            if not base_path or not os.path.exists(os.path.join(base_path, f"bin/cublas64_{version[0]}.dll")):
                raise FileNotFoundError(f"当前环境的下无{version}版本的CUDA驱动，"
                                        f"请添加环境变量CUDA_PATH_V{version[0]}_{version[1]}为对应版本的CUDA目录，例如：\n"
                                        r"CUDA_PATH_V10_2=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2")
            bin_path = os.path.join(base_path, "bin")
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
        super().__init__()
        self.add_pack_opt(CopyCUDADLL(cuda_version=cuda_version))
        self.add_unpack_opt(SetCUDAEnv())
