# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import sys

import qpt
from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.interpreter import PIP
from qpt.modules.base import SubModule, SubModuleOpt, GENERAL_LEVEL_REDUCE, LOW_LEVEL_REDUCE
from qpt.modules.package import CustomPackage, DEFAULT_DEPLOY_MODE
from qpt.modules.cuda import CopyCUDAPackage


class SetPaddleFamilyEnvValueOpt(SubModuleOpt):
    def __init__(self):
        super(SetPaddleFamilyEnvValueOpt, self).__init__()

    def act(self) -> None:
        os.environ["HUB_HOME"] = os.path.join(self.module_path, "opt/HUB_HOME")
        os.environ["PPNLP_HOME"] = os.path.join(self.module_path, "opt/PPNLP_HOME")
        os.environ["SEG_HOME"] = os.path.join(self.module_path, "opt/SEG_HOME")


class CheckAVXOpt(SubModuleOpt):
    def __init__(self, version, use_cuda=False):
        super(CheckAVXOpt, self).__init__(disposable=True)
        self.version = version
        # ToDo 做CUDA的适配 + 去掉>=
        self.use_cuda = use_cuda

    @staticmethod
    def _check_dll():
        from qpt.modules.tools.check_paddle_noavx import SUPPORT_AVX
        return SUPPORT_AVX

    def act(self) -> None:
        if not self._check_dll():
            Logging.warning("为保证可以成功在NoAVX平台执行PaddlePaddle，即将忽略小版本号进行安装PaddlePaddle-NoAVX")
            new_v = self.version[:self.version.rindex(".")]
            Logging.warning("当前CPU不支持AVX指令集，正在尝试在线下载noavx版本的PaddlePaddle")
            PIP.pip_shell(
                f"install paddlepaddle=={new_v} -f https://www.paddlepaddle.org.cn/whl/mkl/stable/noavx.html"
                " --no-index --no-deps --force-reinstall")


def split_paddle_version(package_dist):
    """
    paddle_dist信息分割
    :param package_dist: 形如paddlepaddle_gpu-xxx.postyyy.dist-info的版本信息
    :return: xxx和yyy
    """
    package_dist = package_dist.strip(".dist-info").strip("paddlepaddle_gpu-")
    if ".post" in package_dist:
        paddle_version, cuda_version = package_dist.split(".post")
        cuda_version_a, cuda_version_b = cuda_version[:-1], cuda_version[-1]
    else:
        paddle_version = package_dist
        cuda_version_a, cuda_version_b = "10", "2"
    return paddle_version, cuda_version_a + "." + cuda_version_b


def search_paddle_cuda_version(package_dist=None):
    """
    paddle_dist信息分割，若未提供package_dist则自动搜索
    :param package_dist: 形如paddlepaddle_gpu-xxx.postyyy.dist-info的版本信息
    :return: xxx和yyy
    """
    if package_dist:
        return split_paddle_version(package_dist)
    else:
        import pip
        site_packages_path = os.path.dirname(os.path.dirname(pip.__file__))
        packages_list = os.listdir(site_packages_path)
        paddle_version, cuda_version = None, None
        for package in packages_list:
            if "paddlepaddle_gpu" in package and ".dist-info" in package:
                paddle_version, cuda_version = split_paddle_version(package)
                Logging.info(f"搜索到PaddlePaddle-GPU版本信息：{paddle_version}，所需CUDA版本：{cuda_version}")
                return paddle_version, cuda_version
        if paddle_version is None:
            Logging.info(f"当前Python解释器路径为：{sys.executable}")
            Logging.error(f"当前Python环境下没有PaddlePaddle程序包，请切换至含有PaddlePaddle-GPU的程序包下使用QPT")
            exit(2)


class PaddlePaddleCheckAVX(SubModule):
    """
    解决AVX的适配，并且给予更低优先级
    """

    def __init__(self, version, use_cuda=False):
        super(PaddlePaddleCheckAVX, self).__init__(level=LOW_LEVEL_REDUCE)
        self.add_unpack_opt(CheckAVXOpt(version=version, use_cuda=use_cuda))


class PaddlePaddlePackage(CustomPackage):
    def __init__(self,
                 version: str = None,
                 include_cuda=False,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        self.level = GENERAL_LEVEL_REDUCE
        opts = None
        if not include_cuda:
            super().__init__("paddlepaddle",
                             version=version,
                             deploy_mode=deploy_mode,
                             opts=opts)
        else:
            paddle_version, cuda_version = search_paddle_cuda_version(version)
            paddle_version += ".post" + cuda_version.replace(".", "")

            super().__init__("paddlepaddle-gpu",
                             version=paddle_version,
                             deploy_mode=deploy_mode,
                             find_links="https://paddlepaddle.org.cn/whl/mkl/stable.html")
            self.add_ext_module(CopyCUDAPackage(cuda_version=cuda_version))
        # ToDO 当前方案需要放置在init后
        self.add_unpack_opt(SetPaddleFamilyEnvValueOpt())
        self.add_ext_module(PaddlePaddleCheckAVX(version=version, use_cuda=include_cuda))


class PaddleHubPackage(CustomPackage):
    def __init__(self,
                 version: str = None,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        super().__init__("paddlehub",
                         version=version,
                         deploy_mode=deploy_mode)


class PaddleDetectionPackage(CustomPackage):
    def __init__(self,
                 version: str = None,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        super().__init__("paddledetection",
                         version=version,
                         deploy_mode=deploy_mode)


class PaddleSegPackage(CustomPackage):
    def __init__(self,
                 version: str = None,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        super().__init__("paddleseg",
                         version=version,
                         deploy_mode=deploy_mode)


class PaddleXPackage(CustomPackage):
    def __init__(self,
                 version: str = None,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        super().__init__("paddlex",
                         version=version,
                         deploy_mode=deploy_mode)


class PaddleGANPackage(CustomPackage):
    def __init__(self,
                 version: str = None,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        super().__init__("paddlegan",
                         version=version,
                         deploy_mode=deploy_mode)
