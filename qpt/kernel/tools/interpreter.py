# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import sys
from pip import main as pip_main

from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.pipreqs.pipreqs import make_requirements


class PipTools:
    """
    Python解释器管理器
    """

    def __init__(self, source: str = "https://pypi.tuna.tsinghua.edu.cn/simple"):
        self.source = source
        # ToDo 增加环境管理部分 - 可考虑生成软链
        pass

    @staticmethod
    def pip_shell(shell):
        pip_main(shell.split(" "))

    def pip_package_shell(self,
                          package: str,
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
            shell += opts

        self.pip_shell(shell)

    def download_package(self,
                         package: str,
                         save_path: str,
                         version: str = None,
                         no_dependent=False,
                         find_links: str = None,
                         opts: str = None):
        d_opts = "-d " + save_path
        if opts:
            d_opts += " " + opts
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

    def analyze_dependence(self, analyze_path, save_file_path=None):
        if save_file_path is None:
            save_file_path = os.path.join(analyze_path, "依赖列表.txt")
        ori_stdout = sys.stdout

        with open(save_file_path, "w") as stout_cache:
            # 获取pip给出的依赖列表
            sys.stdout = stout_cache
            self.pip_shell("freeze")
            sys.stdout = ori_stdout
            requirements_dict_search = make_requirements(analyze_path)

        # 搜索py文件中import的依赖项
        requirements_dict_pip = dict()
        with open(save_file_path, "r") as req_file:
            data = req_file.readlines()
            for line in data:
                package, version = line.strip("\n").split("==")
                requirements_dict_pip[package] = version

        # 以pip为基准匹配版本号
        requirements = "".join(
            [package + "==" + requirements_dict_pip[package] + "\n" for package in requirements_dict_search
             if package in requirements_dict_pip])

        with open(save_file_path, "w") as req_file:
            req_file.write(requirements)

        # 供用户检查/修改
        input(f"依赖分析完毕!\n已在\033[32m{os.path.abspath(save_file_path)}\033[0m 中创建了依赖列表\n请检查依赖是否正确后在此处按下回车键继续...")

        requirements = dict()
        with open(save_file_path, "r") as req_file:
            data = req_file.readlines()
            for line in data:
                package, version = line.strip("\n").split("==")
                requirements[package] = version
        return requirements


if __name__ == '__main__':
    a = PipTools()
    b = a.analyze_dependence("/Users/zhanghongji/PycharmProjects/QPT")
    print(b)
