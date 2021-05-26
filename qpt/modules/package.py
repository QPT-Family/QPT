# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import sys
import zipfile
from tempfile import TemporaryDirectory

from qpt.modules.base import SubModule, SubModuleOpt
from qpt.kernel.tools.log_tools import Logging
from qpt.kernel.tools.interpreter_tools import PipTools

pip = PipTools()

LOCAL_DEPLOY_MODE = "为用户准备Whl包，使用时会自动安装，可能会有兼容性问题"
ONLINE_DEPLOY_MODE = "在线安装Python第三方库"


class DownloadWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str,
                 version: str = None,
                 no_dependent=False,
                 find_links: str = None,
                 opts: str = None):
        super().__init__()
        self.package = package
        self.no_dependent = no_dependent
        self.find_links = find_links
        self.opts = opts
        self.version = version

    def act(self) -> None:
        pip.download_package(self.package,
                             version=self.version,
                             save_path=os.path.join(self.module_path, "opt/packages"),
                             no_dependent=self.no_dependent,
                             find_links=self.find_links,
                             opts=self.opts)


class LocalInstallWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str,
                 version: str = None,
                 no_dependent=False,
                 opts: str = None):
        super().__init__()
        self.package = package
        self.no_dependent = no_dependent
        self.opts = opts
        self.version = version

    def act(self) -> None:
        pip.install_local_package(self.package,
                                  version=self.version,
                                  whl_dir=os.path.join(self.module_path, "opt/packages"),
                                  no_dependent=self.no_dependent,
                                  opts=self.opts)


class OnlineInstallWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str,
                 version: str = None,
                 no_dependent=False,
                 find_links: str = None,
                 opts: str = None):
        super().__init__()
        self.package = package
        self.no_dependent = no_dependent
        self.find_links = find_links
        self.opts = opts
        self.version = version

    def act(self) -> None:
        pip.pip_shell(self.package,
                      act="install",
                      version=self.version,
                      find_links=self.find_links,
                      no_dependent=self.no_dependent,
                      opts=self.opts)


class CustomPackage(SubModule):
    def __init__(self,
                 package,
                 version: str = None,
                 deploy_mode=LOCAL_DEPLOY_MODE,
                 no_dependent=False,
                 find_links: str = None,
                 opts: str = None):
        super().__init__(name=None)
        if deploy_mode == LOCAL_DEPLOY_MODE:
            self.add_pack_opt(DownloadWhlOpt(package=package,
                                             version=version,
                                             no_dependent=no_dependent,
                                             find_links=find_links,
                                             opts=opts))
            self.add_unpack_opt(LocalInstallWhlOpt(package=package,
                                                   version=version,
                                                   no_dependent=no_dependent,
                                                   opts=opts))
        else:
            self.add_unpack_opt(OnlineInstallWhlOpt(package=package,
                                                    version=version,
                                                    no_dependent=no_dependent,
                                                    find_links=find_links,
                                                    opts=opts))


class PaddlePaddle(CustomPackage):
    def __init__(self,
                 version: str = None,
                 include_cuda=False,
                 deploy_mode=LOCAL_DEPLOY_MODE):
        if not include_cuda:
            super().__init__("paddlepaddle",
                             version=version,
                             deploy_mode=deploy_mode)
        else:
            raise Exception("暂不支持该模式，请等待后期更新")
            # Logging.warning("正在为PaddlePaddle添加CUDA支持...\n"
            #                 "请注意2.0版本的PaddlePaddle在添加CUDA支持后，即使用户没有合适的GPU设备，"
            #                 "也将默认以GPU模式进行执行。若不添加判断/设备选择的代码，则可能会出现设备相关的报错！\n"
            #                 "Tips:未来QPT将在ONLINE_DEPLOY_MODE(在线安装)模式中添加“自动选择”参数为用户环境进行自动判断")
            # super(PaddlePaddle, self).__init__("paddlepaddle-gpu",
            #                                    version=version,
            #                                    deploy_mode=deploy_mode)
