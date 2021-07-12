# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import sys

from qpt.kernel.tools.os_op import StdOutWrapper, dynamic_load_package, get_qpt_tmp_path
from qpt.kernel.tools.log_op import clean_stout, Logging
from qpt.kernel.tools.terminal import PTerminal, TerminalCallback, LoggingTerminalCallback

TSINGHUA_PIP_SOURCE = "https://pypi.tuna.tsinghua.edu.cn/simple"
BAIDU_PIP_SOURCE = "https://mirror.baidu.com/pypi/simple"
DOUBAN_PIP_SOURCE = "https://pypi.douban.com/simple"
BFSU_PIP_SOURCE = "https://mirrors.bfsu.edu.cn/pypi/web/simple"
DEFAULT_PIP_SOURCE = BFSU_PIP_SOURCE


class PIPTerminal(PTerminal):
    def __init__(self, python_path):
        super(PIPTerminal, self).__init__()
        self.head = os.path.abspath(python_path) + " -m pip"

    def shell_func(self, callback: TerminalCallback = LoggingTerminalCallback()):
        def closure(closure_shell):
            if isinstance(closure_shell, list):
                tmp = [" " + bit_shell for bit_shell in closure_shell]
                closure_shell = "".join(tmp)
            closure_shell = self.head + closure_shell
            Logging.debug(f"SHELL: {closure_shell}")
            closure_shell += "&&echo GACT:DONE!||echo GACT:ERROR!\n"
            self.main_terminal.stdin.write(closure_shell.encode("gbk"))
            self.main_terminal.stdin.flush()
            callback.handle(self.main_terminal)

        return closure


class PipTools:
    """
    Python解释器管理器
    """

    def __init__(self,
                 source: str = None,
                 pip_path=None):
        if source is None:
            source = DEFAULT_PIP_SOURCE
        if pip_path:
            pip_main = dynamic_load_package(packages_name="pip", lib_packages_path=pip_path).main
        else:
            from pip._internal.cli.main import main as pip_main
        self.pip_main = pip_main
        self.pip_local = pip_main
        self.source = source

        # 安静模式
        self.quiet = True if os.getenv("QPT_MODE") == "Run" else False
        if self.quiet:
            Logging.debug("PipTools进入安静模式")

        # ToDo 可考虑增加环境管理部分 - 可考虑生成软链
        pass

    def pip_shell(self, shell):
        if not os.path.exists(get_qpt_tmp_path('pip_cache')):
            os.makedirs(get_qpt_tmp_path('pip_cache'), exist_ok=True)
        shell += f" --isolated --disable-pip-version-check --cache-dir {get_qpt_tmp_path('pip_cache')}" \
                 f" --timeout 60"
        if self.quiet:
            shell += " --quiet"
        self.pip_main(shell.split(" "))
        clean_stout(['console', 'console_errors', 'console_subprocess'])

    def pip_package_shell(self,
                          package: str = None,
                          version: str = None,
                          act="install",
                          no_dependent=False,
                          find_links: str = None,
                          opts: str = None):
        if version:
            package += "==" + version

        shell = f"{act} {package} -i {self.source}"

        if no_dependent:
            shell += " --no-deps"

        if find_links:
            shell += " -f " + find_links

        if opts:
            shell += " " + opts

        self.pip_shell(shell)

    def download_package(self,
                         package: str,
                         save_path: str,
                         version: str = None,
                         no_dependent=False,
                         find_links: str = None,
                         python_version: str = None,
                         opts: str = None):
        d_opts = "-d " + save_path
        if python_version:
            d_opts += " --python-version " + python_version
            d_opts += " --only-binary :all:"

        if opts:
            d_opts += " " + opts

        # pip download xxx -d ./test
        # pip install xxx -f ./test --no-deps
        self.pip_package_shell(package=package,
                               version=version,
                               act="download",
                               no_dependent=no_dependent,
                               find_links=find_links,
                               opts=d_opts)

    def install_local_package(self,
                              package: str,
                              version: str = None,
                              whl_dir: str = None,
                              no_dependent=False,
                              opts: str = None):
        i_opts = "--no-index"
        if opts:
            i_opts += " " + opts
        self.pip_package_shell(package=package,
                               act="install",
                               version=version,
                               no_dependent=no_dependent,
                               find_links=whl_dir,
                               opts=i_opts)

    def analyze_dependence(self, analyze_path, save_file_path=None, return_path=False):
        from qpt.kernel.tools.pipreqs.pipreqs import make_requirements

        if save_file_path is None:
            save_file_path = os.path.join(analyze_path, "requirements_with_opt.txt")

        # 获取pip给出的包信息
        pip_freeze_out = list()
        tmp_stout = StdOutWrapper(container=pip_freeze_out)
        ori_stdout = sys.stdout
        sys.stdout = tmp_stout
        self.pip_local(["freeze"])
        tmp_stout.flush()
        sys.stdout = ori_stdout

        with open(save_file_path, "w", encoding="utf-8") as req_file:
            req_file.writelines(pip_freeze_out)

        # 搜索py文件中import的依赖项
        requirements_dict_search = make_requirements(analyze_path)
        # 读取pip给出的依赖项
        requirements_dict_pip = self.analyze_requirements_file(save_file_path)

        # 以pip为基准匹配版本号
        requirements = {"existent": "", "non-existent": ""}
        for package in requirements_dict_pip:
            if package in requirements_dict_search:
                requirements["existent"] += package + "==" + requirements_dict_pip[package] + "\n"
            elif package.lower() in requirements_dict_search:
                requirements["existent"] += package + "==" + requirements_dict_pip[package.lower()] + "\n"
            else:
                requirements["non-existent"] += "# " + package + "\n"

        with open(save_file_path, "w", encoding="utf-8") as req_file:
            req_file.write("# Here is the list of packages automatically derived by QPT\n"
                           "# you can ignore the dependent packages in the main package and only care "
                           "about the main package\n"
                           "# For example, you need to install paddlepaddle and pillow, because paddlepaddle "
                           "relies on pillow, so you only need to install paddlepaddle.\n"
                           "# ---------------------------------------------------------------------\n"
                           "# QPT Home:        https://github.com/GT-ZhangAcer/QPT\n"
                           "# ---------------------------------------------------------------------\n"
                           "# \n")
            req_file.write(requirements["existent"])
            req_file.write(requirements["non-existent"])

        # 供用户检查/修改
        input(f"依赖分析完毕!\n"
              f"已在\033[32m{os.path.abspath(save_file_path)}\033[0m 中创建了依赖列表\n"
              f"Tips 1: 查看文件后可能需要关闭查看该文件的文本查看器，这样可以有效避免文件被占用\n"
              f"Tips 2: 请务必检查上方文件中所写入的依赖列表情况，因为自动分析并不能保证程序依赖均可以被检出\n"
              f"        若在执行EXE时提示:ImportError: No module named xxx 报错信息，请在该依赖文件中加入xxx或取消xxx前的 # 符号\n"
              f"---------------------------------------------------------------------\n"
              f"\033[41m请在检查/修改依赖文件后\033[0m在此处按下回车键继续...\n"
              f"请键入指令[回车键 - 一次不行可以试试按两次]:_")

        if return_path:
            return save_file_path
        else:
            return self.analyze_requirements_file(save_file_path)

    @staticmethod
    def analyze_requirements_file(file_path):
        requirements = dict()
        try:
            with open(file_path, "r", encoding="utf-8") as req_file:
                data = req_file.readlines()
                for line in data:
                    line = line.strip("\n")
                    if "==" in line:
                        package, version = line.split("==")
                    else:
                        package = line
                        version = None
                    requirements[package] = version
        except Exception as e:
            raise Exception(f"{file_path}文件解析失败，文件可能被其他程序占用或格式异常\n"
                            f"报错信息如下：{e}")
        return requirements

    @staticmethod
    def save_requirements_file(requirements_dict, save_file_path, encoding="utf-8"):
        with open(save_file_path, "w", encoding=encoding) as file:
            for requirement in requirements_dict:
                if requirements_dict[requirement] is not None:
                    line = f"{requirement}=={requirements_dict[requirement]}\n"
                else:
                    line = requirement + "\n"
                file.write(line)


PIP = PipTools()


def set_default_pip_source(source: str):
    global PIP, DEFAULT_PIP_SOURCE
    PIP.source = source
    DEFAULT_PIP_SOURCE = source
    Logging.debug(f"已设置PIP镜像源为：{source}")


def set_default_pip_lib(interpreter_path: str):
    global PIP
    if not os.path.splitext(interpreter_path)[1]:
        interpreter_path = os.path.join(interpreter_path, "python.exe")
    PIP.pip_main = PIPTerminal(interpreter_path).shell_func()
    Logging.debug(f"已设置PIP跨版本编译模式，目标解释器路径为：{interpreter_path}")


def set_pip_configs(lib_package_path=None,
                    source: str = DEFAULT_PIP_SOURCE):
    """
    设置全局pip工具组件
    :param lib_package_path: pip所在位置
    :param source: 镜像源地址
    """
    # 存在Bug，建议开个set接口来替换
    global PIP
    PIP = PipTools(pip_path=lib_package_path, source=source)
