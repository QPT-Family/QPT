# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import shutil
from typing import List

from qpt.kernel.qinterpreter import DISPLAY_LOCAL_INSTALL, DISPLAY_SETUP_INSTALL, DISPLAY_ONLINE_INSTALL, DISPLAY_COPY
from qpt.kernel.qlog import Logging
from qpt.kernel.qos import FileSerialize, ArgManager
from qpt.kernel.qpackage import get_package_all_file, get_package_name_in_file
from qpt.memory import QPT_MEMORY
from qpt.modules.base import SubModule, SubModuleOpt, TOP_LEVEL_REDUCE, LOW_LEVEL, GENERAL_LEVEL, LOW_LEVEL_REDUCE
from qpt.version import version as qpt_version

# 第三方库部署方式
FLAG_FILE_SERIALIZE = "[FLAG-FileSerialize]"
FLAG_FILE_TXT_REQUIREMENT = "[FLAG_File_txt_Requirement]"
DEFAULT_DEPLOY_MODE = DISPLAY_LOCAL_INSTALL

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
                 package: str = "",
                 version: str = None,
                 no_dependent=False,
                 find_links: str = None,
                 python_version=DEFAULT_PACKAGE_FOR_PYTHON_VERSION,
                 opts: ArgManager = None):
        """
        从镜像源下载该package到打包后的opt/packages目录
        """
        super().__init__()
        if opts is None:
            opts = ArgManager()
        self.package = package
        self.no_dependent = no_dependent
        self.find_links = find_links
        self.opts = opts
        self.version = version
        self.python_version = python_version

    def act(self) -> None:
        # 对固化的Requirement文件进行解冻
        if FLAG_FILE_SERIALIZE in self.package[:32]:
            self.opts += "-r " + FileSerialize.serialize2file(self.package.strip(FLAG_FILE_SERIALIZE))
            self.package = ""
        QPT_MEMORY.pip_tool.download_package(self.package,
                                             version=self.version,
                                             save_path=os.path.join(self.module_path,
                                                                    QPT_MEMORY.get_down_packages_relative_path),
                                             no_dependent=self.no_dependent,
                                             find_links=self.find_links,
                                             python_version=self.python_version,
                                             opts=self.opts)


class LocalInstallWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str = "",
                 version: str = None,
                 static_whl: bool = False,  # 控制是否从指定安装
                 no_dependent=False,
                 opts: ArgManager = None):
        """
        从opt/packages目录中安装该packages
        """
        super().__init__(disposable=True)
        if opts is None:
            opts = ArgManager()
        self.package = package
        self.static_whl = static_whl
        self.no_dependent = no_dependent
        self.opts = opts
        self.version = version

    def act(self) -> None:
        if FLAG_FILE_SERIALIZE in self.package[:32]:
            self.opts += "-r " + FileSerialize.serialize2file(self.package[len(FLAG_FILE_SERIALIZE):])
            self.package = ""
        if FLAG_FILE_TXT_REQUIREMENT in self.package[:32]:
            self.opts += "-r " + os.path.join(self.opt_path, "requirements_dev.txt")
            self.package = ""

        self.opts += "--target " + self.module_site_package_path

        if self.static_whl:
            QPT_MEMORY.pip_tool.install_local_package(
                os.path.join(self.download_packages_path, os.path.basename(self.package)),
                abs_package=True,
                version=self.version,
                whl_dir=os.path.join(self.module_path,
                                     QPT_MEMORY.get_down_packages_relative_path),
                no_dependent=self.no_dependent,
                opts=self.opts)
        else:
            QPT_MEMORY.pip_tool.install_local_package(self.package,
                                                      version=self.version,
                                                      whl_dir=os.path.join(self.module_path,
                                                                           QPT_MEMORY.get_down_packages_relative_path),
                                                      no_dependent=self.no_dependent,
                                                      opts=self.opts)


class OnlineInstallWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str = "",
                 version: str = None,
                 to_module_env_path=True,
                 to_python_env_version=DEFAULT_PACKAGE_FOR_PYTHON_VERSION,
                 no_dependent=False,
                 find_links: str = None,
                 opts: ArgManager = None):
        """
        在线从镜像源中安装该packages
        """
        super().__init__(disposable=True)
        if opts is None:
            opts = ArgManager()
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
        if FLAG_FILE_SERIALIZE in self.package[:32]:
            self.opts += "-r " + FileSerialize.serialize2file(self.package.strip(FLAG_FILE_SERIALIZE))
            self.package = ""
        if FLAG_FILE_TXT_REQUIREMENT in self.package[:32]:
            self.opts += "-r " + os.path.join(self.opt_path, "requirements_dev.txt")
            self.package = ""

        if self.to_module_env:
            self.opts += "--target " + self.module_site_package_path
            if self.to_python_env_version:
                self.opts += f"--python-version {self.to_python_env_version} --only-binary :all:"
        QPT_MEMORY.pip_tool.pip_package_shell(self.package,
                                              act="install",
                                              version=self.version,
                                              find_links=self.find_links,
                                              no_dependent=self.no_dependent,
                                              opts=self.opts)


class CustomPackage(SubModule):
    def __init__(self,
                 package="",
                 version: str = None,
                 deploy_mode=None,
                 no_dependent=False,
                 find_links: str = None,
                 opts: ArgManager = None,
                 name: str = None):
        """
        基础Python包SubModule
        :param package: Python包名
        :param version: 版本号
        :param deploy_mode: 部署模式
        :param no_dependent: 是否包含依赖
        :param find_links: 同pip -f
        :param opts: pip附加命令
        :param name: SubModule name
        """
        if name is None:
            name = "NoneName_" + package
        super().__init__(name=name)
        if opts is None:
            opts = ArgManager()
        if deploy_mode is None:
            deploy_mode = DEFAULT_DEPLOY_MODE
        if deploy_mode == DISPLAY_LOCAL_INSTALL:
            self.add_pack_opt(DownloadWhlOpt(package=package,
                                             version=version,
                                             no_dependent=no_dependent,
                                             find_links=find_links,
                                             opts=opts))
            self.add_unpack_opt(LocalInstallWhlOpt(package=package,
                                                   version=version,
                                                   no_dependent=no_dependent,
                                                   opts=ArgManager() + "-U --upgrade-strategy eager"))
        elif deploy_mode == DISPLAY_ONLINE_INSTALL:
            self.add_unpack_opt(OnlineInstallWhlOpt(package=package,
                                                    version=version,
                                                    no_dependent=no_dependent,
                                                    find_links=find_links,
                                                    opts=opts))
        elif deploy_mode == DISPLAY_SETUP_INSTALL:
            self.add_pack_opt(OnlineInstallWhlOpt(package=package,
                                                  version=version,
                                                  no_dependent=no_dependent,
                                                  find_links=find_links,
                                                  opts=opts))
        elif deploy_mode == DISPLAY_COPY:
            self.add_pack_opt(CopyLocalPackageAllFileOpt(package=package))

        else:
            raise IndexError(f"{deploy_mode}不能够被识别或未注册")


class _FreezeRequirementsOpt(SubModuleOpt):
    def __init__(self, requirements_file_path):
        super(_FreezeRequirementsOpt, self).__init__(disposable=True)
        self.requirements_file_path = requirements_file_path

    def act(self) -> None:
        shutil.copy(src=self.requirements_file_path, dst=self.opt_path)


class _RequirementsPackage(SubModule):
    def __init__(self,
                 requirements_file_path,
                 deploy_mode=None,
                 name: str = None):
        super().__init__(name=name)
        if deploy_mode is None:
            deploy_mode = DEFAULT_DEPLOY_MODE

        fs_data = ""

        if deploy_mode != DISPLAY_SETUP_INSTALL:
            # 部分情况需要序列化requirement.txt文件
            # fs = FileSerialize(requirements_file_path)
            # fs_data = FLAG_FILE_SERIALIZE + fs.get_serialize_data()
            self.add_pack_opt(_FreezeRequirementsOpt(requirements_file_path))
            fs_data = FLAG_FILE_TXT_REQUIREMENT

        requirements_file_path = "-r " + requirements_file_path
        if deploy_mode == DISPLAY_LOCAL_INSTALL:
            self.add_pack_opt(DownloadWhlOpt(opts=ArgManager() + requirements_file_path,
                                             no_dependent=True))
            self.add_unpack_opt(LocalInstallWhlOpt(package=fs_data,
                                                   no_dependent=True))
        elif deploy_mode == DISPLAY_ONLINE_INSTALL:
            self.add_unpack_opt(OnlineInstallWhlOpt(package=fs_data,
                                                    no_dependent=True))
        elif deploy_mode == DISPLAY_SETUP_INSTALL:
            self.add_pack_opt(OnlineInstallWhlOpt(opts=ArgManager() + requirements_file_path,
                                                  no_dependent=True,
                                                  to_module_env_path=True))


class QPTDependencyPackage(SubModule):
    def __init__(self):
        """
        QPT依赖相关SubModule
        """
        self.level = TOP_LEVEL_REDUCE
        super().__init__(name=None)
        kernel_dependency_path = os.path.join(os.path.split(__file__)[0], "kernel_dependency.txt")
        lazy_dependency_path = os.path.join(os.path.split(__file__)[0], "qpt_lazy_dependency.txt")
        lazy_dependency_serialize = FLAG_FILE_SERIALIZE + FileSerialize(lazy_dependency_path).get_serialize_data()
        kernel = "-r " + kernel_dependency_path
        lazy = "-r " + lazy_dependency_path
        self.add_pack_opt(OnlineInstallWhlOpt(package="qpt",
                                              version=qpt_version,
                                              no_dependent=True,
                                              to_module_env_path=True))
        self.add_pack_opt(OnlineInstallWhlOpt(no_dependent=False,
                                              to_module_env_path=True,
                                              opts=ArgManager() + "-U" + kernel))
        self.add_pack_opt(DownloadWhlOpt(opts=ArgManager() + lazy,
                                         no_dependent=False))
        self.add_unpack_opt(LocalInstallWhlOpt(package=lazy_dependency_serialize,
                                               no_dependent=False))


class QPTGUIDependencyPackage(SubModule):
    def __init__(self):
        """
        QPT GUI依赖相关SubModule
        """
        self.level = TOP_LEVEL_REDUCE
        super().__init__(name=None)
        kernel_dependency_path = os.path.join(os.path.split(__file__)[0], "kernel_dependency_GUI.txt")
        kernel = "-r " + kernel_dependency_path
        self.add_pack_opt(OnlineInstallWhlOpt(opts=ArgManager() + kernel,
                                              no_dependent=False,
                                              to_module_env_path=True))


class CheckNotSetupOpt(SubModuleOpt):
    """
    ToDo 未测试
    """

    def __init__(self, path=None):
        """
        指定目录，检测目录中是否有Python包安装被遗漏
        """
        super().__init__(disposable=True)
        self.path = path

    def act(self) -> None:
        if self.path is None:
            self.path = self.download_packages_path
            whl_list = self.uninstalled_offline_installation_packages
        else:
            whl_list = [whl for whl in os.listdir(self.path)
                        if os.path.splitext(whl)[-1] in [".gz", ".whl", "zip"]]

        Logging.info(f"需要补充的安装包数量为：{len(whl_list)}")
        for whl_name in whl_list:
            QPT_MEMORY.pip_tool.install_local_package(os.path.join(self.download_packages_path, whl_name),
                                                      abs_package=True,
                                                      no_dependent=True)


class CheckNotSetupPackage(SubModule):
    """
    ToDo 未测试
    """

    def __init__(self, name):
        """
        指定目录，检测目录中是否有Python包安装被遗漏
        """
        super().__init__(name=name)
        self.level = LOW_LEVEL
        if DEFAULT_DEPLOY_MODE == DISPLAY_LOCAL_INSTALL:
            self.add_unpack_opt(CheckNotSetupOpt())


class CopyLocalPackageAllFileOpt(SubModuleOpt):
    def __init__(self, package: str or List[str]):
        """
        对指定Python包的所以相关文件进行复制，可以避免需要编译的包在客户端编译
        :param package: Python包名
        """
        super().__init__(disposable=True)
        self.package = package

    def act(self) -> None:
        def make(name):
            # Package文件缺失时仅警告一次
            missing_file_warning_flag = True

            # 获取文件列表
            records = get_package_all_file(package=name)
            for record in records:
                # 过滤cache
                if record.endswith(".pyc"):
                    continue

                src_path = os.path.abspath(os.path.join(QPT_MEMORY.site_packages_path, record))
                # 检查对应文件是否存在
                if not os.path.exists(src_path):
                    if missing_file_warning_flag:
                        Logging.warning(f"[SubModule]{self.name}\t| {name}\t可能存在文件缺失")
                        missing_file_warning_flag = False
                    Logging.debug(f"[SubModule]{self.name}\t| {name}\t{src_path}文件缺失")
                    continue
                else:
                    dst_path = os.path.abspath(os.path.join(self.module_site_package_path, record))
                    dst_dir = os.path.dirname(dst_path)
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                    shutil.copy(src_path, dst_path)

        if isinstance(self.package, list):
            for p in self.package:
                make(p)
        else:
            make(self.package)


class CopyWhl2PackagesOpt(SubModuleOpt):
    def __init__(self, whl_path):
        """
        适用于安装额外且单一的whl包，将whl包移动至打包后的opt/packages目录，在首次运行EXE时会自动对该包进行安装。
        :param whl_path: whl路径
        """
        super().__init__(disposable=True)
        self.whl_path = whl_path

    def act(self) -> None:
        shutil.copy(src=self.whl_path, dst=self.download_packages_path)


class CopyWhl2Packages(SubModule):
    def __init__(self,
                 whl_path,
                 level=GENERAL_LEVEL,
                 not_install=False,
                 opt=None,
                 name: str = None):
        """
        适用于安装额外且单一的whl包，将whl包移动至打包后的opt/packages目录，在首次运行EXE时会自动对该包进行安装。
        :param whl_path: whl路径
        """
        if name is None:
            name = os.path.basename(whl_path).replace(".", "")[:10]
        super().__init__(name=name, level=level)
        self.add_pack_opt(CopyWhl2PackagesOpt(whl_path))

        if not not_install:
            if opt is None:
                opt = ArgManager(["-U --force-reinstall"])
            self.add_unpack_opt(LocalInstallWhlOpt(package=whl_path, static_whl=True, opts=opt))


class CheckCompileCompatibilityOpt(CopyLocalPackageAllFileOpt):
    def __init__(self):
        super().__init__(package=None)

    def act(self) -> None:
        # Overwrite CopyLocalPackageAllFileOpt 的self.package
        self.package = list()
        del_file = list()

        # 读取AutoRequirement文件，目的判断是否需要被Check，没有在文件内的不Check
        with open(os.path.join(self.opt_path, "requirements_dev.txt"), "r", encoding="utf-8") as f:
            requirements = f.read()
        for whl in self.existing_offline_installation_packages:
            if os.path.splitext(whl)[-1] != ".whl":
                name = get_package_name_in_file(whl).replace("-", "_").lower()
                if name in requirements:
                    # 需要注意，生成临时的Requirement文件时，首行不可为依赖
                    requirements = requirements.replace("\n" + name, f"\n# Ignore {name}")
                    self.package.append(name)
                    del_file.append(whl)

        if self.package:
            Logging.warning(f"\n以下Python依赖，其官方并未提供二进制whl包，为保证在无编译环境下仍可正常运行，"
                            f"即将复制本地编译后文件至运行环境。\n"
                            f"{', '.join(self.package)}")
        super().act()

        with open(os.path.join(self.opt_path, "requirements_dev.txt"), "w", encoding="utf-8") as f:
            f.write(requirements)

        for whl in del_file:
            if os.path.splitext(whl)[-1] != ".whl":
                os.remove(os.path.join(self.download_packages_path, whl))


class CheckCompileCompatibility(SubModule):
    def __init__(self):
        """
        非二进制包检查，本地拷贝对应包后删除对应包
        ToDo -> 在线模式要如何做？
        """
        super().__init__()
        self.level = LOW_LEVEL_REDUCE
        self.add_pack_opt(CheckCompileCompatibilityOpt())
