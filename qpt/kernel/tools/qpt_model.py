# Author: Acer Zhang
# Datetime: 2020/12/28 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import zipfile

from qpt.kernel.tools.log_tools import Logging


def check_file(QPT_extract, zip_file_names):
    """
    简单检测已解压文件的完整性
    """
    if os.path.exists(QPT_extract):
        Logging.info(f"正在简略校验QPT_EXTRACT目录下文件，如环境出现问题可删除 {os.path.abspath(QPT_extract)} 中所有文件后重试")
        for file_name in zip_file_names:
            if not os.path.exists(os.path.join(QPT_extract, file_name)):
                return True
        return False
    else:
        return True


class GModule:
    def __init__(self, module_file_path):
        """
        GModule管理器
        :param module_file_path: Module文件路径
        """
        self.module_file_path = module_file_path
        # *.QPT文件路径 -> 文件所在目录、文件名
        self.module_path, self.module_file = os.path.split(module_file_path)
        # 编码类型
        self.decode_type = b'utf-8'
        # 读取压缩包
        self.zip_file = zipfile.ZipFile(module_file_path, "r")

    def load_module(self, progressbar=None, text=None):
        """
        读取Module
        :param progressbar: QT进度条对象 - 将会返回当前进度值
        :param text: QT文本框对象 - 将会返回当前解压文件名
        """

        # 获取QPT拓展文件路径
        qpt_extract = os.path.join(self.module_path, "QPT_EXTRACT")
        # 获取拓展文件列表
        zip_file_names = self.zip_file.namelist()
        if len(zip_file_names) == 0:
            Logging.warning(f"压缩包{os.path.abspath(self.module_file_path)}中不包含任何文件！")
        # 校验拓展文件
        re_flag = check_file(qpt_extract, zip_file_names)
        if re_flag:
            file_sum = len(zip_file_names)
            for file_id, name in enumerate(zip_file_names):
                self.zip_file.extract(name, qpt_extract)
                percentage = int(100 * file_id / file_sum)
                print(percentage)
                if progressbar:
                    progressbar.setValue(percentage)
                if text:
                    text.setText("当前目录下/" + name)
        else:
            if progressbar:
                progressbar.setValue(100)
            if text:
                text.setText("解压完毕！")

    def make_module(self, build_path, module_name, author, version):
        # 读取压缩包
        self.zip_file = zipfile.ZipFile(self.module_file_path, "w")
        # 检测主程序是否存在
        run_py_path = os.path.join(build_path, "run.py")
        if not os.path.exists(run_py_path):
            raise FileNotFoundError(f"[主程序]{run_py_path}文件未找到，请将模块主Python文件命名为run.py")
        # 检测SHELL.txt是否存在
        venv_txt_path = os.path.join(build_path, "VENV.txt")
        if not os.path.exists(venv_txt_path):
            raise FileNotFoundError(f"[虚拟环境]{run_py_path}文件未找到，请撰写VENV.txt文件")
        # 将Module信息写入INFO文件
        # noinspection PyTypeChecker
        self.zip_file.writestr("INFO", str(dict(locals().items())))
        # 打包拓展文件
        for path, dir_names, file_names in os.walk(build_path):
            file_path = path.replace(build_path, './')
            for file_name in file_names:
                self.zip_file.write(os.path.join(path, file_name), os.path.join(file_path, file_name))
        Logging.info(f"文件制作完毕，QPT文件被保存至{os.path.abspath(self.module_file_path)}")

    def match_venv(self, cmd):
        shell_list = self.zip_file.read("VENV").decode("utf-8")
        shell_list = shell_list.split("\n")
        for line in shell_list:
            if "main$" in line:
                line = line.replace("main$", "")
                # !需更改 判断是否存在该环境->安装对应环境->切换conda环境
                cmd.run(line)
            elif "shell$" in line:
                line = line.replace("shell$", "")
                # !需更改
                cmd.run(line)
            else:
                cmd.run(line)

    def req_module_info(self):
        # 加载模块信息
        module_info = self.zip_file.read("INFO").decode("utf-8")
        return module_info


if __name__ == '__main__':
    print("测试生成")
    tmp = GModule("../tmp.QPT")
    # # build_path需更换为所需打包的路径，其中run.py为主程序
    tmp.make_module(build_path="./buildQPT", module_name="testname", author="testauthor", version=1.1)

    # print("测试读取ing")
    # tmp.load_module()
    # print(tmp.req_module_info())
