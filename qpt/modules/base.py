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
        self._user_qpt_base_path = "/"
        self.terminal = None

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

                    # 例如在qpt环境主目录中新建abc目录
                    import os
                    os.mkdir(os.path.join(self.get_user_qpt_base_path(), "abc"))
        """
        pass

    def get_user_qpt_base_path(self):
        return self._user_qpt_base_path

    def terminal(self, shell):
        self.terminal(shell)
        pass


class SubModule:
    def __init__(self, name):
        self.name = name

        # 占位OP
        self.pack_opts = list()
        self.details = {"Pack": [], "Unpack": []}

        # 占位out_dir，将会保存序列化文件到该目录
        self.out_dir = None

        # 占位terminal
        self.terminal = None

    def set_terminal_func(self, terminal_func):
        self.terminal = terminal_func

    def set_out_dir(self, path):
        self.out_dir = path

    def add_pack_opt(self, opt: SubModuleOpt):
        self.details["Pack"].append(opt.__class__.__name__)
        self.pack_opts.append(opt)

    def add_unpack_opt(self, opt: SubModuleOpt):
        self.details["Unpack"].append(opt.__class__.__name__)
        self._serialize_op(opt)

    def pack(self):
        """
        在撰写该Module时，开发侧需要的操作
        """
        for opt in self.pack_opts:
            Logging.debug(f"正在加载{self.name}-{opt.name}OP")
            opt()

    def unpack(self):
        """
        用户使用该Module时，需要完成的操作
        """
        ops = os.listdir(os.path.join(self.out_dir, "opt", self.name))
        for op_name in ops:
            op_name = str(op_name)
            if os.path.splitext(op_name)[-1] == ".op":
                with open(os.path.join(self.out_dir, "opt", self.name, op_name), "rb") as file:
                    opt = pickle.load(file)
                    Logging.debug(f"正在加载{self.name}-{opt.name}OP")
                    opt()

    # ToDo:做序列化来保存
    def _serialize_op(self, opt):
        name = opt.__class__.__name__
        serialize_path = os.path.join(self.out_dir, "opt", self.name)
        serialize_file_path = serialize_path + name + ".op"

        os.makedirs(serialize_path, exist_ok=True)

        with open(serialize_file_path, "wb") as file:
            pickle.dump(opt, file)
