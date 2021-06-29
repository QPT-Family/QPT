# Author: Acer Zhang
# Datetime: 2021/6/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os

from qpt.kernel.tools.os_op import Logging
from qpt.executor import CreateExecutableModule

import click


@click.command()
@click.option("-f",
              "--folder",
              prompt="请输入待打包的文件夹路径",
              help='待打包的文件夹路径，该目录也应当为整个项目的根目录或工作目录，否则可能会导致出现找不到模块等Python基础报错。',
              required=True)
@click.option("-p",
              "--py",
              prompt="请输入待打包的主要Py脚本文件路径",
              help="待打包的主要Py脚本文件所在的路径，例如要yyy/xxx.py中xxx.py是需要打包的主要Python文件，那么该处填写xxx.py即可。",
              required=True)
@click.option("-s", "--save", prompt="请输入打包后文件保存的路径", help='打包后文件保存的路径。', required=True)
@click.option("-r",
              "--require",
              default="auto",
              prompt="请输入requirements.txt文件路径，若无该文件可直接按下[回车键]自动生成该文件",
              help="自动检测软件包依赖，填写auto后将会自动查找待打包的文件夹路径中所有py文件的import使用情况，最终生成requirements文件\n"
                   "当然，也可传入requirements.txt文件路径，这样即可指定依赖列表进行安装。")
@click.option("-h",
              "--hidden",
              default=False,
              type=bool,
              help="是否隐藏全部终端窗口，若输入true或判定为真则隐藏全部Terminal窗口（适用于使用了PyQT、TK等桌面级可视化程序），"
                   "输入false或判定为否则不隐藏（适用于Console & 终端程序）。")
def cli(folder,
        py,
        save,
        require,
        hidden):
    Logging.info("-----------------------------QPT--------------------------------")
    Logging.info("当前执行模式为命令式执行，仅提供QPT基础功能，高阶操作可在GitHub参考最新文档")
    Logging.info("            https://github.com/GT-ZhangAcer/QPT")
    Logging.info("-----------------------------QPT--------------------------------")
    Logging.info(f"[--folder]待打包的文件夹路径为\t{os.path.abspath(folder)}")
    Logging.info(f"[--py]待打包的主Python文件路径为\t{os.path.abspath(py)}")
    Logging.info(f"[--save]打包后文件保存路径为\t{os.path.abspath(save)}")
    if require.lower() == "auto":
        Logging.info(f"[--require]使用自动化依赖查找Module：AutoRequirementsPackage")
    else:
        Logging.info(f"[--require]使依赖列表文件路径为：{os.path.abspath(require)}")
    if hidden:
        Logging.info("当前打包模式为：隐藏全部的Terminal窗口")
    else:
        Logging.info("当前打包模式为：显示Terminal窗口（就是用户打开后的那个黑色框框，可通过指定 -h True 命令来隐藏）")

    Logging.info("QPT使用命令可输入：qpt --help 获取")
    module = CreateExecutableModule(work_dir=folder,
                                    launcher_py_path=py,
                                    save_path=save,
                                    requirements_file=require,
                                    hidden_terminal=hidden)
    module.make()


if __name__ == '__main__':
    cli(["--help"])
