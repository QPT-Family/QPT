import os
import shutil

from pip import main as pip_main

from qpt.kernel.tools.log_op import Logging

# 缺省环境变量值 ToDo:当前版本仅为适配Windows考虑
ENVIRON_VARS = {"QPT_BASE": "C:/QPT_HOME"}


class QPTEnv:
    """
    QPT环境变量管理器
    """

    def __init__(self):
        # 环境变量占位
        self.environ_vars_check = dict()
        self.qpt_base_path = None
        self.python_path = None
        self.env_base_path = None

        # 检查环境变量是否正确设置
        self.check_environ_var()

    def set_environ_var(self, qpt_base_path: str = None):
        # 环境变量 ToDO:增加CUDA目录
        self.qpt_base_path = os.environ["QPT_BASE"]
        self.python_path = os.path.join(os.environ["QPT_BASE"], "/interpreter")
        self.env_base_path = os.path.join(os.environ["QPT_BASE"], "/env")

    def check_environ_var(self):
        """
        检查环境变量是否被设置，若不设置则使用缺省值
        """
        for var_id, var in enumerate(ENVIRON_VARS):
            try:
                value = os.environ[var]
            except KeyError as e:
                Logging.warning(str(e))
                os.environ[var] = ENVIRON_VARS[var]
                value = var
            self.environ_vars_check[var] = value


class Interpreter:
    """
    Python解释器管理器
    """

    def __init__(self):
        pass

    @staticmethod
    def pip(package,
            mode="install",
            source="https://pypi.tuna.tsinghua.edu.cn/simple",
            opts: str = None):
        shell = [mode, " " + package, "-i " + source]
        if opts:
            shell.append(" " + opts)
        pip_main(shell)


class VirtualEnv:
    """
    Python虚拟环境控制组件 - 貌似不需要了
    """

    # ToDO 需要增加Auto模式
    def __init__(self, qpt_env: QPTEnv = QPTEnv()):
        # 虚拟环境列表占位
        self.env_dict = dict()

        # 获取虚拟环境文件夹
        self.env_base_path = qpt_env.env_base_path

        # 获取当前虚拟环境信息
        self.req_env_list()

    def create_env(self, env_id, base_name):
        env_path = os.path.join(self.env_base_path, f"venv#{env_id}#{base_name}")
        virtualenv.cli_run([env_path])
        Logging.info(f"{env_path}环境创建完毕")

    def del_env(self, env_id):
        env_path = self.get_env_path(env_id)
        shutil.rmtree(env_path)
        Logging.info(f"{env_path}环境删除完毕")

    def req_env_list(self):
        """
        获取当前已有的环境信息
        """
        self.env_dict.clear()
        for env_dir in os.listdir(self.env_base_path):
            if os.path.isdir(env_dir) and "venv#" in env_dir:
                env_id = env_dir.split("#")[1]
                self.env_dict[env_id] = env_dir

    def get_env_path(self, env_id):
        return os.path.join(self.env_base_path, self.env_dict[env_id])

    def active(self, env_id, shell_method):
        """
        为终端激活一个虚拟环境
        :param env_id: 虚拟环境id
        :param shell_method: 终端的shell方法
        """
        shell_method(os.path.join(self.get_env_path(env_id), "Scripts/activate"))
        Logging.info(f"尝试激活{self.env_dict[env_id]}环境")
