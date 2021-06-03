# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

from qpt.modules.base import SubModule, SubModuleOpt, HIGH_LEVEL, TOP_LEVEL_REDUCE, GENERAL_LEVEL_REDUCE
from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.interpreter import PipTools
from qpt.kernel.tools.os_op import get_qpt_tmp_path, FileSerialize
from qpt._compatibility import com_configs

pip = PipTools()


def set_pip_tools(lib_package_path=None,
                  source: str = "https://pypi.tuna.tsinghua.edu.cn/simple"):
    """
    设置全局pip工具组件
    :param lib_package_path: pip所在位置
    :param source: 镜像源地址
    """
    global pip
    pip = PipTools(lib_packages_path=lib_package_path, source=source)


# 第三方库部署方式
LOCAL_DOWNLOAD_DEPLOY_MODE = "为用户准备Whl包，首次启动时会自动安装，可能会有兼容性问题"
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
        pip.download_package(self.package,
                             version=self.version,
                             save_path=os.path.join(self.module_path, "opt/packages"),
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
        pip.install_local_package(self.package,
                                  version=self.version,
                                  whl_dir=os.path.join(self.module_path, "opt/packages"),
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
        pip.pip_package_shell(self.package,
                              act="install",
                              version=self.version,
                              find_links=self.find_links,
                              no_dependent=self.no_dependent,
                              opts=self.opts)


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
            fs_data = "[FLAG-FileSerialize]" + fs.get_data()
        requirements_file_path = "-r " + requirements_file_path
        if deploy_mode == LOCAL_DOWNLOAD_DEPLOY_MODE:
            self.add_pack_opt(DownloadWhlOpt(package=requirements_file_path,
                                             no_dependent=False))
            self.add_unpack_opt(LocalInstallWhlOpt(package=fs_data,
                                                   no_dependent=True))
        elif deploy_mode == ONLINE_DEPLOY_MODE:
            self.add_unpack_opt(OnlineInstallWhlOpt(package=fs_data,
                                                    no_dependent=False))
        elif deploy_mode == LOCAL_INSTALL_DEPLOY_MODE:
            self.add_pack_opt(OnlineInstallWhlOpt(package=requirements_file_path,
                                                  no_dependent=False,
                                                  to_module_env_path=True))


class AutoRequirementsPackage(_RequirementsPackage):
    """
    注意，这并不是个普通的Module
    """

    def __init__(self,
                 path,
                 module_list: list,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        """
        自动获取Requirements
        :param path: 待扫描的文件夹路径或requirements文件路径，若提供了requirements文件路径则不会自动分析依赖情况
        :param module_list: Module callback
        :param deploy_mode: 部署模式
        """
        if os.path.isfile(path):
            requirements = pip.analyze_requirements_file(path)
        else:
            Logging.info(f"正在分析{os.path.abspath(path)}下的依赖情况...")
            requirements = pip.analyze_dependence(path, return_path=False)

        # 对特殊包进行过滤和特殊化
        for requirement in dict(requirements):
            if requirement in SPECIAL_MODULE:
                special_module, parameter = SPECIAL_MODULE[requirement]
                parameter["version"] = requirements[requirement]
                parameter["deploy_mode"] = deploy_mode
                module_list.append(special_module(**parameter))
                requirements.pop(requirement)

        # 保存依赖至
        requirements_path = os.path.join(get_qpt_tmp_path(), "requirements_dev.txt")
        pip.save_requirements_file(requirements, requirements_path)

        # 执行常规的安装
        super().__init__(requirements_file_path=requirements_path,
                         deploy_mode=deploy_mode)


class QPTDependencyPackage(SubModule):
    def __init__(self):
        self.level = TOP_LEVEL_REDUCE
        super().__init__(name=None)
        # ToDO 上线后修改qpt_dependency.txt文件
        kernel_dependency_path = os.path.join(os.path.split(__file__)[0], "qpt_kernel_dependency.txt")
        lazy_dependency_path = os.path.join(os.path.split(__file__)[0], "qpt_lazy_dependency.txt")
        kernel = "-r " + kernel_dependency_path
        lazy = "-r " + lazy_dependency_path
        self.add_pack_opt(OnlineInstallWhlOpt(package=kernel,
                                              no_dependent=False,
                                              to_module_env_path=True))
        self.add_pack_opt(DownloadWhlOpt(package=lazy,
                                         no_dependent=False))
        self.add_unpack_opt(LocalInstallWhlOpt(package=lazy,
                                               no_dependent=False))


class PaddlePaddlePackage(CustomPackage):
    def __init__(self,
                 version: str = None,
                 include_cuda=False,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        self.level = GENERAL_LEVEL_REDUCE
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


# 自动推理依赖时需要特殊处理的Module配置列表 格式{包名: (Module, Module参数字典)}
# version、deploy_mode 为必填字段
SPECIAL_MODULE = {"paddlepaddle": (PaddlePaddlePackage, {"version": None,
                                                         "include_cuda": False,
                                                         "deploy_mode": DEFAULT_DEPLOY_MODE}),
                  "paddlepaddle-gpu": (PaddlePaddlePackage, {"version": None,
                                                             "include_cuda": True,
                                                             "deploy_mode": DEFAULT_DEPLOY_MODE})}
