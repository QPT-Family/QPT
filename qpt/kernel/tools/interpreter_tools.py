# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
from pip import main as pip_main

from qpt.kernel.tools.log_tools import Logging


class PipTools:
    """
    Python解释器管理器
    """

    def __init__(self, source: str = "https://pypi.tuna.tsinghua.edu.cn/simple"):
        self.source = source
        # ToDo 增加环境管理部分
        pass

    def pip_shell(self,
                  package: str,
                  version: str = None,
                  act="install",
                  no_dependent=False,
                  find_links: str = None,
                  opts: str = None):
        if version:
            package += "==" + version
        shell = [act, package, "-i", self.source]
        if no_dependent:
            shell.append("--no-deps")
        if find_links:
            shell.append("-f")
            shell.append(find_links)

        if opts:
            for opt in opts.split(" "):
                shell.append(opt)
        pip_main(shell)

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
        self.pip_shell(package=package,
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
        self.pip_shell(package=package,
                       act="install",
                       version=version,
                       no_dependent=no_dependent,
                       find_links=whl_dir,
                       opts=opts)


# shell = ["download", "pillow", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-d", "./test"]
# pip_main(shell)

if __name__ == '__main__':
    a = PipTools()
    a.download_package("pillow", save_path="./test")
    a.install_local_package("pillow", whl_dir="./test")
