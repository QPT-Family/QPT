# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.interpreter import PIP
from qpt.sys_info import AVX_SUPPORT_FLAG
from qpt.modules.base import SubModuleOpt, GENERAL_LEVEL_REDUCE
from qpt.modules.package import CustomPackage, DEFAULT_DEPLOY_MODE, ONLINE_DEPLOY_MODE


class SetPaddleFamilyEnvValueOpt(SubModuleOpt):
    def __init__(self):
        super(SetPaddleFamilyEnvValueOpt, self).__init__()

    def act(self) -> None:
        os.environ["HUB_HOME"] = os.path.join(self.module_path, "opt/HUB_HOME")
        os.environ["PPNLP_HOME"] = os.path.join(self.module_path, "opt/PPNLP_HOME")
        os.environ["SEG_HOME"] = os.path.join(self.module_path, "opt/SEG_HOME")


class NoAVXOpt(SubModuleOpt):
    def __init__(self):
        super(NoAVXOpt, self).__init__(disposable=True)

    pass


# ToDO要不要重构SubModule，使其增加ExtModule

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
            if not AVX_SUPPORT_FLAG:
                # ToDO 变成Opt才会成功
                new_v = version.split(".")[:-1]
                Logging.warning("当前CPU不支持AVX指令集，正在尝试在线下载noavx版本的PaddlePaddle")
                PIP.pip_shell("uninstall paddlepaddle --quiet")
                PIP.pip_shell(
                    f"install paddlepaddle>={new_v} -f https://www.paddlepaddle.org.cn/whl/mkl/stable/noavx.html"
                    " --no-index --no-deps")

        else:
            # ToDo 增加Soft-CUDA
            raise Exception("暂不支持PaddlePaddle-GPU模式，请等待近期更新")
            # Logging.warning("正在为PaddlePaddle添加CUDA支持...\n"
            #                 "请注意2.0版本的PaddlePaddle在添加CUDA支持后，即使用户没有合适的GPU设备，"
            #                 "也将默认以GPU模式进行执行。若不添加判断/设备选择的代码，则可能会出现设备相关的报错！\n"
            #                 "Tips:未来QPT将在ONLINE_DEPLOY_MODE(在线安装)模式中添加“自动选择”参数为用户环境进行自动判断")
            # super(PaddlePaddle, self).__init__("paddlepaddle-gpu",
            #                                    version=version,
            #                                    deploy_mode=deploy_mode)
        self.add_unpack_opt(SetPaddleFamilyEnvValueOpt())


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
