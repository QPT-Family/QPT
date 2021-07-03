# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

from qpt.version import version as qpt_version
from qpt.modules.base import SubModule, SubModuleOpt, TOP_LEVEL_REDUCE, LOW_LEVEL
from qpt.kernel.tools.interpreter import PIP
from qpt.kernel.tools.os_op import FileSerialize
from qpt._compatibility import com_configs

DOWN_PACKAGES_RELATIVE_PATH = "opt/packages"

# 第三方库部署方式
LOCAL_DOWNLOAD_DEPLOY_MODE = "为用户准备Whl包，首次启动时会自动安装，即使这样也可能会有兼容性问题"
LOCAL_INSTALL_DEPLOY_MODE = "[不推荐]预编译第三方库，首次启动无需安装但将额外消耗硬盘空间，可能会有兼容性问题并且只支持二进制包"
ONLINE_DEPLOY_MODE = "用户使用时在线安装Python第三方库"
DEFAULT_DEPLOY_MODE = LOCAL_DOWNLOAD_DEPLOY_MODE

# 第三方库下载版本
PACKAGE_FOR_PYTHON38_VERSION = "3.8"
DEFAULT_PACKAGE_FOR_PYTHON_VERSION = None  # None表示不设置


def set_default_deploy_mode(mode):
    """
    设置全局部署方式
    :param mode: 部署方式
    """
    global DEFAULT_DEPLOY_MODE
    DEFAULT_DEPLOY_MODE = mode


def set_default_package_for_python_version(version):
    """
    设置全局下载的Python包默认解释器版本号
    :param version: Python版本号
    """
    global DEFAULT_PACKAGE_FOR_PYTHON_VERSION
    DEFAULT_PACKAGE_FOR_PYTHON_VERSION = version


class DownloadWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str,
                 version: str = None,
                 no_dependent=False,
                 find_links: str = None,
                 python_version=DEFAULT_PACKAGE_FOR_PYTHON_VERSION,
                 opts: str = None):
        super().__init__()
        self.package = package
        self.no_dependent = no_dependent
        self.find_links = find_links
        self.opts = opts
        self.version = version
        self.python_version = python_version

    def act(self) -> None:
        if "[FLAG-FileSerialize]" in self.package[:32]:
            self.package = self.package.strip("[FLAG-FileSerialize]")
            self.package = "-r " + FileSerialize.serialize2file(self.package)
        PIP.download_package(self.package,
                             version=self.version,
                             save_path=os.path.join(self.module_path, DOWN_PACKAGES_RELATIVE_PATH),
                             no_dependent=self.no_dependent,
                             find_links=self.find_links,
                             python_version=self.python_version,
                             opts=self.opts)


class LocalInstallWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str,
                 version: str = None,
                 no_dependent=False,
                 opts: str = None):
        super().__init__(disposable=True)
        self.package = package
        self.no_dependent = no_dependent
        self.opts = opts
        self.version = version

    def act(self) -> None:
        if "[FLAG-FileSerialize]" in self.package[:32]:
            self.package = self.package.strip("[FLAG-FileSerialize]")
            self.package = "-r " + FileSerialize.serialize2file(self.package)
        if self.opts is None:
            self.opts = ""
        # self.opts += "--target " + os.path.join(self.interpreter_path,
        #                                         com_configs["RELATIVE_INTERPRETER_SITE_PACKAGES_PATH"])
        PIP.install_local_package(self.package,
                                  version=self.version,
                                  whl_dir=os.path.join(self.module_path, DOWN_PACKAGES_RELATIVE_PATH),
                                  no_dependent=self.no_dependent,
                                  opts=self.opts)


class OnlineInstallWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str,
                 version: str = None,
                 to_module_env_path=True,
                 to_python_env_version=DEFAULT_PACKAGE_FOR_PYTHON_VERSION,
                 no_dependent=False,
                 find_links: str = None,
                 opts: str = None):
        super().__init__(disposable=True)
        self.package = package
        self.to_module_env = to_module_env_path
        self.no_dependent = no_dependent
        self.find_links = find_links
        self.opts = opts
        self.version = version
        self.to_python_env_version = to_python_env_version
        if to_python_env_version:
            assert to_module_env_path, "安装在当前环境则不需要设置Python版本号参数to_python_env_version。" \
                                       "若需要安装其它位置，请设置to_module_env_path参数使包安装在其它位置。"
            self.to_python_env_version = DEFAULT_PACKAGE_FOR_PYTHON_VERSION

    def act(self) -> None:
        if self.to_module_env:
            if not self.opts:
                self.opts = ""
            self.opts += "--target " + os.path.join(self.interpreter_path,
                                                    com_configs["RELATIVE_INTERPRETER_SITE_PACKAGES_PATH"])
            if self.to_python_env_version:
                self.opts += f" --python-version {self.to_python_env_version} --only-binary :all:"
        PIP.pip_package_shell(self.package,
                              act="install",
                              version=self.version,
                              find_links=self.find_links,
                              no_dependent=self.no_dependent,
                              opts=self.opts)


class BatchInstallationOpt(SubModuleOpt):
    def __init__(self, path=None):
        super(BatchInstallationOpt, self).__init__(disposable=True)
        self.path = path

    def act(self) -> None:
        if self.path is None:
            self.path = os.path.join(self.module_path, DOWN_PACKAGES_RELATIVE_PATH)
        whl_list = [whl.split("-")[0] for whl in os.listdir(self.path)]
        # opts = "--target " + os.path.join(self.interpreter_path,
        #                                   com_configs["RELATIVE_INTERPRETER_SITE_PACKAGES_PATH"])
        opts = ""
        for whl_name in whl_list:
            PIP.install_local_package(whl_name,
                                      whl_dir=self.path,
                                      no_dependent=True,
                                      opts=opts)


class CustomPackage(SubModule):
    def __init__(self,
                 package,
                 version: str = None,
                 deploy_mode=DEFAULT_DEPLOY_MODE,
                 no_dependent=False,
                 find_links: str = None,
                 opts: str = None):
        super().__init__(name=None)
        if deploy_mode == LOCAL_DOWNLOAD_DEPLOY_MODE:
            self.add_pack_opt(DownloadWhlOpt(package=package,
                                             version=version,
                                             no_dependent=no_dependent,
                                             find_links=find_links,
                                             opts=opts))
            self.add_unpack_opt(LocalInstallWhlOpt(package=package,
                                                   version=version,
                                                   no_dependent=no_dependent,
                                                   opts=opts))
        elif deploy_mode == ONLINE_DEPLOY_MODE:
            self.add_unpack_opt(OnlineInstallWhlOpt(package=package,
                                                    version=version,
                                                    no_dependent=no_dependent,
                                                    find_links=find_links,
                                                    opts=opts))
        elif deploy_mode == LOCAL_INSTALL_DEPLOY_MODE:
            self.add_pack_opt(OnlineInstallWhlOpt(package=package,
                                                  version=version,
                                                  no_dependent=no_dependent,
                                                  find_links=find_links,
                                                  opts=opts))


class _RequirementsPackage(SubModule):
    def __init__(self,
                 requirements_file_path,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        super().__init__(name=None)
        fs_data = ""
        # 部分情况需要序列化requirement.txt文件
        if deploy_mode != LOCAL_INSTALL_DEPLOY_MODE:
            fs = FileSerialize(requirements_file_path)
            fs_data = "[FLAG-FileSerialize]" + fs.get_serialize_data()
        requirements_file_path = "-r " + requirements_file_path
        if deploy_mode == LOCAL_DOWNLOAD_DEPLOY_MODE:
            self.add_pack_opt(DownloadWhlOpt(package=requirements_file_path,
                                             no_dependent=False))
            self.add_unpack_opt(LocalInstallWhlOpt(package=fs_data,
                                                   no_dependent=False))
        elif deploy_mode == ONLINE_DEPLOY_MODE:
            self.add_unpack_opt(OnlineInstallWhlOpt(package=fs_data,
                                                    no_dependent=False))
        elif deploy_mode == LOCAL_INSTALL_DEPLOY_MODE:
            self.add_pack_opt(OnlineInstallWhlOpt(package=requirements_file_path,
                                                  no_dependent=False,
                                                  to_module_env_path=True))


class QPTDependencyPackage(SubModule):
    def __init__(self):
        self.level = TOP_LEVEL_REDUCE
        super().__init__(name=None)
        kernel_dependency_path = os.path.join(os.path.split(__file__)[0], "kernel_dependency.txt")
        lazy_dependency_path = os.path.join(os.path.split(__file__)[0], "qpt_lazy_dependency.txt")
        lazy_dependency_serialize = "[FLAG-FileSerialize]" + FileSerialize(lazy_dependency_path).get_serialize_data()
        kernel = "-r " + kernel_dependency_path
        lazy = "-r " + lazy_dependency_path
        self.add_pack_opt(OnlineInstallWhlOpt(package="qpt",
                                              version=qpt_version,
                                              no_dependent=True))
        self.add_pack_opt(OnlineInstallWhlOpt(package=kernel,
                                              no_dependent=False,
                                              to_module_env_path=True))
        self.add_pack_opt(DownloadWhlOpt(package=lazy,
                                         no_dependent=False))
        self.add_unpack_opt(LocalInstallWhlOpt(package=lazy_dependency_serialize,
                                               no_dependent=False))


class QPTGUIDependencyPackage(SubModule):
    def __init__(self):
        self.level = TOP_LEVEL_REDUCE
        super().__init__(name=None)
        kernel_dependency_path = os.path.join(os.path.split(__file__)[0], "kernel_dependency_GUI.txt")
        kernel = "-r " + kernel_dependency_path
        self.add_pack_opt(OnlineInstallWhlOpt(package=kernel,
                                              no_dependent=False,
                                              to_module_env_path=True))


class BatchInstallation(SubModule):
    def __init__(self):
        super().__init__()
        self.level = LOW_LEVEL
        if DEFAULT_DEPLOY_MODE == LOCAL_DOWNLOAD_DEPLOY_MODE:
            self.add_unpack_opt(BatchInstallationOpt())


# 自动推理依赖时需要特殊处理的Module配置列表 格式{包名: (Module, Module参数字典)}
# version、deploy_mode 为必填字段
