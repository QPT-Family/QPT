# Author: Acer Zhang
# Datetime: 2021/5/26
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import datetime
import os
import pickle
from distutils.sysconfig import get_python_lib

from qpt.kernel.qlog import Logging
from qpt.kernel.qpackage import search_ready_packages, get_package_name_in_file
from qpt.memory import QPT_MODE, CheckRun, QPT_MEMORY

# 定义优先级 优先级越高执行顺序越考前，一般设置为GENERAL_LEVEL
TOP_LEVEL = 5.  # 底层高优先级
TOP_LEVEL_REDUCE = 4.5  # 系统级高优先级
HIGH_LEVEL = 4.  # 高优先级
HIGH_LEVEL_REDUCE = 3.5  # 紧随高优先级
GENERAL_LEVEL = 3.  # 普通优先级 - AutoRequirementsPackage
GENERAL_LEVEL_REDUCE = 2.5  # 紧随普通优先级 - 特殊的CallBack软件包 PaddlePaddlePackage
LOW_LEVEL = 2.  # 低优先级 - CheckNotSetupPackage
LOW_LEVEL_REDUCE = 1.5  # 紧随低优先级 - PaddlePaddleCheckAVX、CheckCompileCompatibility
BOTTOM_LEVEL = 1.  # 系统级低优先级
BOTTOM_LEVEL_REDUCE = 0.5  # 底层低优先级


class SubBase:
    def __init__(self):
        # 路径变量
        # 解释器所在路径占位
        self._interpreter_path = "./"
        # Module目录 - 创建Module时的保存目录/执行Module时的Module目录
        self._module_path = "./"

        # 终端占位
        self._terminal = None
        # 工作目录占位 - 创建Module时的工作目录（待打包的目录）/执行Module时的resources目录
        self._work_dir = "./"

    @property
    def interpreter_path(self):
        """
        解释器路径
        :return:
        """
        return self._interpreter_path

    @property
    def module_path(self):
        """
        创建Module时的保存目录/执行Module时的Module目录
        :return:
        """
        return self._module_path

    @property
    def work_dir(self):
        """
        用户指定的工作目录
        :return:
        """
        return self._work_dir

    @property
    def config_path(self):
        """
        配置文件目录
        :return:
        """
        return os.path.join(self.module_path, "configs")

    @property
    def site_package_path(self):
        """
        获取当前Python环境的默认包管理路径
        :return:
        """
        sp_path = os.path.abspath(get_python_lib())
        return sp_path

    @property
    def module_site_package_path(self):
        """
        获取Module所使用的默认包管理路径
        :return:
        """
        sp_path = os.path.abspath(os.path.join(self.module_path, "Python/Lib/site-packages"))
        return sp_path

    @property
    def download_packages_path(self):
        """
        获取下载的离线whl包路径
        :return:
        """
        return os.path.join(self.module_path, QPT_MEMORY.get_down_packages_relative_path)

    @property
    def opt_path(self):
        """
        获取opt目录的路径
        :return:
        """
        return os.path.join(self.module_path, "opt")

    @property
    def ready_packages(self):
        """
        已经安装成功的packages
        :return:
        """
        packages = search_ready_packages()
        return packages

    @property
    def existing_offline_installation_packages(self):
        """
        存在的离线package
        :return:
        """
        if not os.path.exists(self.download_packages_path):
            return list()
        else:
            whl_list = [whl for whl in os.listdir(self.download_packages_path)
                        if os.path.splitext(whl)[-1] in [".gz", ".whl", "zip"]]
            return whl_list

    @property
    def uninstalled_offline_installation_packages(self):
        """
        未安装的离线package
        :return:
        """
        uninstall_whl = list()
        ready_list = "|".join([k.lower() for k in search_ready_packages().keys()])
        for whl in self.existing_offline_installation_packages:
            name = get_package_name_in_file(whl)
            if name not in ready_list:
                uninstall_whl.append(whl)
        return uninstall_whl


class SubModuleOpt(SubBase):
    """
    自定义子模块操作，用于子模块封装时和封装后的操作流程设置，支持shell操作和Python原生语言操作
    """

    def __init__(self, disposable=False):
        super().__init__()
        """
        :param disposable: 算子是否为一次性算子，默认非一次性 - 通常用于安装第三方库等只需要进行一次就可以永久使用的情况
        """
        self.name = self.__class__.__name__

        # 算子是否为一次性算子 - 通常用于安装第三方库等只需要进行一次就可以永久使用的情况
        self.disposable = disposable

    def act(self) -> None:
        """
        使用Python语句和终端来执行操作
        Example:
            class MyOpt(SubModuleOpt):
                def run(self):
                    super().run()
                    # 例如新建C:/abc目录
                    import os
                    os.mkdir(r"C:/abc")

                    # 例如在终端中查看当前目录（Windows为dir命令）
                    self.terminal("dir")

                    # 例如在用户使用时为其Module所在的目录中新建abc目录
                    import os
                    os.mkdir(os.path.join(self.module_path, "abc"))

            sub_module = XXXModule()
            sub_module.add_pack_opt(MyOpt()) or sub_module.add_unpack_opt(MyOpt())
        """
        pass

    def run(self, op_path):
        inactive_file = op_path + ".inactive"
        if (self.disposable and os.path.exists(inactive_file)) and CheckRun.check_run_file(self.config_path):
            Logging.debug(f"找到该OP状态文件{self.name}.inactive，故跳过该OP")
        else:
            self.act()
        if self.disposable and os.path.exists(os.path.dirname(op_path)):
            with open(inactive_file, "w", encoding="utf-8") as f:
                f.write(f"于{str(datetime.datetime.now())}创建了该状态文件")

    def prepare(self, work_dir=None, interpreter_path=None, module_path=None, terminal=None):
        """
        Todo: 后续实例化Memory，不再设置prepare
        :param work_dir:
        :param interpreter_path:
        :param module_path:
        :param terminal:
        :return:
        """
        self._work_dir = work_dir
        self._interpreter_path = interpreter_path
        self._module_path = module_path
        self._terminal = terminal

    def terminal(self, shell):
        self._terminal(shell)


class SubModule(SubBase):
    def __init__(self, name=None, level: int = GENERAL_LEVEL):
        super().__init__()
        if name is None:
            name = self.__class__.__name__
        self.name = name
        self.level = level

        # 占位OP
        self.pack_opts = list()
        self.unpack_opts = list()
        self.ready_unpack_opt_count = 0
        self.details = {"Pack": [], "Unpack": []}
        self._ext_module = list()

    def add_ext_module(self, module):
        """
        额外的Module
        :param module:额外的Module
        """
        # ToDo 加个raise，避免没有完成__init__就开始add，针对super__init__的情况
        Logging.info(f"{self.__class__.__name__}中自动添加了名为{module.name}的ExtModule")
        self._ext_module.append(module)

    def get_all_module(self) -> list:
        return [self] + self._ext_module

    def prepare(self, work_dir=None, interpreter_path=None, module_path=None, terminal=None):
        self._work_dir = work_dir
        self._interpreter_path = interpreter_path
        self._module_path = module_path
        self._terminal = terminal

    def add_pack_opt(self, opt: SubModuleOpt):
        self.details["Pack"].append(opt.__class__.__name__)
        self.pack_opts.append(opt)

    def add_unpack_opt(self, opt: SubModuleOpt):
        self.details["Unpack"].append(opt.__class__.__name__)
        self.unpack_opts.append(opt)

    def pack(self):
        """
        在撰写该Module时，开发侧需要的操作
        """
        assert self._module_path, "SubModule的out_dir未设置！"
        for opt in self.pack_opts:
            Logging.info(f"正在加载{self.name}-{opt.name}OP")
            op_path = os.path.join(self._module_path, "opt", self.name, opt.name)
            opt.prepare(interpreter_path=self._interpreter_path,
                        module_path=self._module_path,
                        terminal=self._terminal,
                        work_dir=self._work_dir)
            opt.run(op_path)

        for opt in self.unpack_opts:
            Logging.info(f"正在封装{self.name}-{opt.name}OP")
            self._serialize_op(opt)

    def unpack(self):
        """
        用户使用该Module时，需要完成的操作
        """
        files = os.listdir(os.path.join(self._module_path, "opt", self.name))
        ops = list()
        for file in files:
            if file[:3].isdigit():
                ops.append(file)
            else:
                Logging.warning(f"{self.name}-{file} op可能已损坏，建议重新解压并运行或联系软件提供者")
        ops.sort(key=lambda x: int(x[:3]))
        for op_name in ops:
            op_name = str(op_name)
            if os.path.splitext(op_name)[-1] == ".op":
                op_path = os.path.join(self._module_path, "opt", self.name, op_name)
                with open(op_path, "rb") as file:
                    opt = pickle.load(file)
                    opt.prepare(interpreter_path=self._interpreter_path,
                                module_path=self._module_path,
                                terminal=self._terminal,
                                work_dir=self._work_dir)
                    if QPT_MODE != "Run":
                        Logging.debug(f"正在加载{self.name}-{opt.name}OP")
                    opt.run(op_path)

    # ToDo:做序列化来保存
    def _serialize_op(self, opt):
        name = opt.__class__.__name__
        self.ready_unpack_opt_count += 1
        serialize_path = os.path.join(self._module_path, "opt", self.name)
        serialize_file_path = os.path.join(serialize_path, f"{self.ready_unpack_opt_count:03d}-{name}.op")

        os.makedirs(serialize_path, exist_ok=True)

        with open(serialize_file_path, "wb") as file:
            pickle.dump(opt, file)
