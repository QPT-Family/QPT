# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import sys
from pip import main as pip_main

from qpt.kernel.tools.log_op import Logging


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

    def analyze_dependence(self):
        ori_stdout = sys.stdout
        with open("./test.txt", "w") as f:
            sys.stdout = f
            self.pip_shell("freeze")
        sys.stdout = ori_stdout


# shell = ["download", "pillow", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-d", "./test"]
# pip_main(shell)

if __name__ == '__main__':
    a = PipTools()
    ori_stdout = sys.stdout
    with open("./test.txt", "w") as f:
        sys.stdout = f
        a.pip_shell("freeze")
    sys.stdout = ori_stdout

    pass
    # a.install_local_package("pillow", whl_dir="./test")
