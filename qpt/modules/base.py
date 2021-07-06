# Author: Acer Zhang
# Datetime: 2021/5/26
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import pickle
import datetime

from qpt.kernel.tools.os_op import download
from qpt.kernel.tools.log_op import Logging
from qpt.sys_info import QPT_MODE

# 定义优先级 优先级越高执行顺序越考前，一般设置为GENERAL_LEVEL
TOP_LEVEL = 5.  # 底层高优先级
TOP_LEVEL_REDUCE = 4.5  # 系统级高优先级
HIGH_LEVEL = 4.  # 高优先级
HIGH_LEVEL_REDUCE = 3.5  # 紧随高优先级
GENERAL_LEVEL = 3.  # 普通优先级
GENERAL_LEVEL_REDUCE = 2.5  # 紧随普通优先级
LOW_LEVEL = 2.  # 低优先级 - BatchInstallation
LOW_LEVEL_REDUCE = 1.5  # 紧随低优先级 - PaddlePaddleCheckAVX
BOTTOM_LEVEL = 1.  # 系统级低优先级
BOTTOM_LEVEL_REDUCE = 0.5  # 底层低优先级


class SubModuleOpt:
    """
    自定义子模块操作，用于子模块封装时和封装后的操作流程设置，支持shell操作和Python原生语言操作
    """

    def __init__(self, disposable=False):
        self.name = self.__class__.__name__

        # 算子是否为一次性算子 - 通常用于安装第三方库等只需要进行一次就可以永久使用的情况
        self.disposable = disposable

        # 环境变量
        # 解释器所在路径占位
        self._interpreter_path = "./"
        # Module目录 - 创建Module时的保存目录/执行Module时的Module目录
        self._module_path = "./"
        # 终端占位
        self._terminal = None
        # 工作目录占位 - 创建Module时的工作目录（待打包的目录）/执行Module时的resources目录
        self._work_dir = "./"

    def act(self) -> None:
        """
        使用Python语句和终端来执行操作
        Example:
            class MyOpt(SubModuleOpt):
                def run_py(self):
                    super().run_py()
                    # 例如新建C:/abc目录
                    import os
                    os.mkdir(r"C:/abc")

                    # 例如在终端中查看当前目录（Windows为dir命令）
                    self.terminal("dir")

                    # 例如在用户使用时为其Module所在的目录中新建abc目录
                    import os
                    os.mkdir(os.path.join(self.module_path, "abc"))
        """
        pass

    def run(self, op_path):
        inactive_file = op_path + ".inactive"
        if self.disposable and os.path.exists(inactive_file):
            Logging.debug(f"找到该OP状态文件{self.name}.inactive，故跳过该OP")
        else:
            self.act()
        if self.disposable and os.path.exists(os.path.dirname(op_path)):
            with open(inactive_file, "w", encoding="utf-8") as f:
                f.write(f"于{str(datetime.datetime.now())}创建了该状态文件")

    @property
    def interpreter_path(self):
        return self._interpreter_path

    @property
    def module_path(self):
        return self._module_path

    @property
    def work_dir(self):
        return self._work_dir

    def prepare(self, work_dir=None, interpreter_path=None, module_path=None, terminal=None):
        self._work_dir = work_dir
        self._interpreter_path = interpreter_path
        self._module_path = module_path
        self._terminal = terminal

    def terminal(self, shell):
        self._terminal(shell)


class SubModule:
    def __init__(self, name=None, level: int = GENERAL_LEVEL):
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

        # 占位out_dir，将会保存序列化文件到该目录，pack时需要被set
        self._module_path = "./"
        self._interpreter_path = "./"
        self._terminal = "./"
        self._work_dir = "./"

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
        ops = os.listdir(os.path.join(self._module_path, "opt", self.name))
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
