# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import sys

from qpt.kernel.tools.os_op import StdOutWrapper, dynamic_load_package
from qpt.kernel.tools.log_op import clean_stout


class PipTools:
    """
    Python解释器管理器
    """

    def __init__(self,
                 source: str = "https://pypi.tuna.tsinghua.edu.cn/simple",
                 lib_packages_path=None):
        if lib_packages_path:
            pip_main = dynamic_load_package(packages_name="pip", lib_packages_path=lib_packages_path).main
        else:
            from pip._internal.cli.main import main as pip_main
        self.pip_main = pip_main
        self.source = source
        # ToDo 可考虑增加环境管理部分 - 可考虑生成软链
        pass

    def pip_shell(self, shell):
        shell += " --isolated --disable-pip-version-check"
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
            shell += " -f" + find_links

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
        self.pip_shell("freeze")
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
            req_file.write("# 以下是QPT自动推导出的包列表 - 此处可无视主包中的依赖包，只关心主要包情况即可\n"
                           "# 例如paddlepaddle依赖Pillow，即使Pillow在下方被注释，但在封装时依旧会被打包\n"
                           "# ---------------------------------------------------------------------\n"
                           "# QPT源码:        https://github.com/GT-ZhangAcer/QPT\n"
                           "# ---------------------------------------------------------------------\n"
                           "# \n")
            req_file.write(requirements["existent"])
            req_file.write(requirements["non-existent"])

        # 供用户检查/修改
        input(f"依赖分析完毕!\n"
              f"已在\033[32m{os.path.abspath(save_file_path)}\033[0m 中创建了依赖列表\n"
              f"Tips:查看文件后可能需要关闭查看该文件的文本查看器，这样可以有效避免文件被占用\n"
              f"---------------------------------------------------------------------\n"
              f"请在检查/修改依赖后在此处按下回车键继续...\n")

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
    def save_requirements_file(requirements_dict, save_file_path):
        with open(save_file_path, "w", encoding="utf-8") as file:
            for requirement in requirements_dict:
                if requirements_dict[requirement] is not None:
                    line = f"{requirement}=={requirements_dict[requirement]}\n"
                else:
                    line = requirement + "\n"
                file.write(line)
