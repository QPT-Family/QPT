import os

from qpt.kernel.tools.sys_tools import SubCMD

# 默认安装的PaddlePaddle版本，None则为最新版
PADDLE_VERSION = None
CUDA_TOOLKIT = '11.0'


class CondaVenv:
    channels = ["conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/",
                "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/",
                "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/",
                "conda config --set show_channel_urls yes"]

    def __init__(self):
        self.venv_info = list()
        self.venv_list = list()

        # 默认workdir为用户安装QPT的目录
        self.workdir = os.getenv("QPT_BASE")
        # workdir/conda_base为Conda安装目录
        self.conda_path = os.path.join(self.workdir, "conda_base")
        self.conda_bat = os.path.join(self.workdir, "conda_base/condabin/conda.bat")
        # workdir/venvs为Conda的虚拟环境目录
        self.venvs_path = os.path.join(self.workdir, "venvs")

        self.cmd = SubCMD()

    def req_venv_info(self):
        """
        获取当前虚拟环境目录下的所有环境
        """
        self.venv_info.clear()
        self.venv_list.clear()
        for d in os.listdir(self.venvs_path):
            if "#venv#" in d:
                self.venv_info.append(d)
                self.venv_list.append(d.split("#", 2)[-1])
        return self.venv_list

    def create_venv(self,
                    py_version="3.8",
                    whl_venv_name="paddlepaddle",
                    with_gpu=False,
                    whl_venv_version=PADDLE_VERSION,
                    venv_name: str = None):
        """
        创建一Conda环境
        环境将会在QPT_BASE环境变量下的conda_base目录生成以 id#venv#whl_venv_name+whl_venv_version
        :param py_version: Python版本
        :param whl_venv_name: whl名
        :param with_gpu: 是否包含GPU环境（当前仅作用于Paddle）
        :param whl_venv_version: whl版本
        :param venv_name: 环境名
        """
        # .\conda.bat create paddlepaddle python=3.8 -y -p .\venvs

        __whl_version = whl_venv_version if whl_venv_version else "static"
        __device = "GPU" if with_gpu else "CPU"
        if venv_name is None:
            venv_name = f"#venv#{len(self.venv_info) + 1}#{whl_venv_name}-{__whl_version}-{__device}"
        else:
            venv_name = f"#venv#{len(self.venv_info) + 1}#{venv_name}-{__device}"
        # 是否为GPU版本（目前仅兼容Paddle）
        if with_gpu:
            # 此操作会修改whl_venv_name
            whl_venv_name += "-gpu cudatoolkit=" + CUDA_TOOLKIT
        # 若指定版本号则增加“=版本号”
        if whl_venv_version is not None:
            whl_venv_name += "=" + whl_venv_version
        # 若为空白环境则省去一处空格
        if whl_venv_name is None:
            whl_venv_name = ""
        else:
            whl_venv_name += " "

        # 创建环境
        self._shell(f"{self.conda_bat} create {whl_venv_name}python={py_version}"
                    f" -y -p {self.venvs_path}/{venv_name}")
        # 更新环境列表信息
        self.req_venv_info()

    def activate_env(self, index):
        """
        激活环境
        :param index: 环境索引号
        :return 返回激活成功的环境名
        """
        actual_name = self.venv_info[index]
        name = self.venv_list[index]

        self._shell(f"{self.conda_bat} activate {self.venvs_path}/{actual_name}")
        return name

    def pip(self, whl, version):
        """
        使用pip命令进行安装
        :param version: 版本号
        :param whl: whl名
        """
        # 待完善 - 可能会缺获取Python-pip路径，待验证该问题是否存在
        self._shell(f"pip {whl}=={version}")

    def set_channels(self):
        """
        设置镜像源
        """
        # 待完善 - 缺pip镜像源设置以及所调用的路径
        for channel in self.channels:
            self._shell(channel)

    def _shell(self, shell):
        self.cmd.shell(shell)
