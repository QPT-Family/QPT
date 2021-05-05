import os
import collections
import pickle

from qpt.kernel.tools.sys_tools import download

GLOBAL_OPT_ID = 0


class SubModuleOpt:
    """
    自定义子模块操作，用于子模块封装时和封装后的操作流程设置，支持shell操作和Python原生语言操作
    """

    def __init__(self, opt_name=None):
        if opt_name is None:
            global GLOBAL_OPT_ID
            opt_name = str(GLOBAL_OPT_ID)
            GLOBAL_OPT_ID += 1

        self.name = opt_name

        # 环境变量
        self._user_qpt_base_path = "./"
        self.shell = None

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

    def get_user_qpt_base_path(self):
        return self._user_qpt_base_path

    def terminal(self, shell):
        self.shell(shell)
        pass


class SubModule:
    def __init__(self, name):
        self.name = name

        # 占位OP
        self.pack_ops = collections.OrderedDict()
        self.apply_ops = collections.OrderedDict()

        # 占位out_dir，将会保存序列化文件到该目录
        self.out_dir = None

    def add_pack_opt(self, opt: SubModuleOpt):
        self._add_op(self.pack_ops, opt)

    def add_unpack_opt(self, opt: SubModuleOpt):
        self._add_op(self.apply_ops, opt)

    def pack(self):
        """
        在撰写该Module时，开发侧需要的操作
        """
        pass

    def unpack(self):
        """
        用户使用该Module时，需要完成的操作
        """
        pass

    def print_details(self):
        pass

    # ToDo:做序列化来保存
    def _add_op(self, op_dict: collections.OrderedDict, opt: SubModuleOpt, serialize=False):
        name = opt.name
        act = opt.act
        op_dict[name] = act
        if serialize:
            serialize_path = os.path.join(self.out_dir, "opt", self.name)
            serialize_file_path = serialize_path + name + ".op"

            os.makedirs(serialize_path, exist_ok=True)

            with open(serialize_file_path, "w") as file:
                pickle.dump(act, file)
