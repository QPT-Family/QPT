import os
import collections
import pickle

from qpt.kernel.tools.sys_tools import download
from qpt.kernel.tools.log_tools import Logging

GLOBAL_OPT_ID = 0


class SubModuleOpt:
    """
    自定义子模块操作，用于子模块封装时和封装后的操作流程设置，支持shell操作和Python原生语言操作
    """

    def __init__(self):
        self.name = self.__class__.__name__

        # 环境变量
        # 解释器所在路径占位
        self._interpreter_path = "./"
        # 创建Module时的保存目录/执行Module时的Module目录
        self._module_path = "./"
        # 终端占位
        self._terminal = None

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

    @property
    def interpreter_path(self):
        return self._interpreter_path

    @property
    def module_path(self):
        return self._module_path

    def prepare(self, interpreter_path=None, save_path=None, terminal=None):
        self._interpreter_path = interpreter_path
        self._module_path = save_path
        self._terminal = terminal

    def terminal(self, shell):
        self._terminal(shell)


class SubModule:
    def __init__(self, name):
        self.name = name

        # 占位OP
        self.pack_opts = list()
        self.unpack_opts = list()
        self.ready_unpack_opt_count = 0
        self.details = {"Pack": [], "Unpack": []}

        # 占位out_dir，将会保存序列化文件到该目录，pack时需要被set
        self._module_path = None
        self._interpreter_path = None
        self._terminal = None

    def prepare(self, interpreter_path=None, module_path=None, terminal=None):
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
            Logging.debug(f"正在加载{self.name}-{opt.name}OP")
            opt.prepare(self._interpreter_path, self._module_path, self._terminal)
            opt.act()

        for opt in self.unpack_opts:
            Logging.debug(f"正在封装{self.name}-{opt.name}OP")
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
                with open(os.path.join(self._module_path, "opt", self.name, op_name), "rb") as file:
                    opt = pickle.load(file)
                    opt.prepare(self._interpreter_path, self._module_path, self._terminal)
                    Logging.debug(f"正在加载{self.name}-{opt.name}OP")
                    opt.act()

    # ToDo:做序列化来保存
    def _serialize_op(self, opt):
        name = opt.__class__.__name__
        self.ready_unpack_opt_count += 1
        serialize_path = os.path.join(self._module_path, "opt", self.name)
        serialize_file_path = os.path.join(serialize_path, f"{self.ready_unpack_opt_count:03d}-{name}.op")

        os.makedirs(serialize_path, exist_ok=True)

        with open(serialize_file_path, "wb") as file:
            pickle.dump(opt, file)
