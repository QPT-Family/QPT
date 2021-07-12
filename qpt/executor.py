# Author: Acer Zhang
# Datetime: 2021/5/26
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import sys
import shutil
import importlib
import base64
import datetime

from typing import List

import qpt
from qpt._compatibility import com_configs
from qpt.modules.base import SubModule
from qpt.modules.python_env import BasePythonEnv, AutoPythonEnv
from qpt.modules.package import QPTDependencyPackage, QPTGUIDependencyPackage, \
    DEFAULT_DEPLOY_MODE, \
    set_default_deploy_mode, BatchInstallation
from qpt.modules.auto_requirements import AutoRequirementsPackage

from qpt.kernel.tools.log_op import Logging, TProgressBar, set_logger_file
from qpt.kernel.tools.os_op import clean_qpt_cache, copytree, check_chinese_char, StdOutLoggerWrapper, add_ua
from qpt.kernel.tools.terminal import AutoTerminal
from qpt.kernel.tools.interpreter import set_default_pip_lib
from qpt.sys_info import QPT_MODE, check_all

__all__ = ["CreateExecutableModule", "RunExecutableModule"]


class CreateExecutableModule:
    def __init__(self,
                 work_dir,
                 launcher_py_path,
                 save_path,
                 ignore_dirs: list = None,
                 requirements_file="auto",
                 deploy_mode=DEFAULT_DEPLOY_MODE,
                 sub_modules: List[SubModule] = None,
                 interpreter_module: BasePythonEnv = None,
                 module_name="未命名模型",
                 version="未知版本号",
                 author="未知作者",
                 hidden_terminal: bool = False,
                 with_debug: bool = False):
        self.with_debug = with_debug

        # 初始化路径成员变量
        self.launcher_py_path = os.path.relpath(launcher_py_path, work_dir)
        if self.launcher_py_path[:1] == "\\":
            self.launcher_py_path = self.launcher_py_path[1:]
        assert "." not in self.launcher_py_path.strip(".py"), \
            f"{self.launcher_py_path}中的路径或文件名中出现了除“.py”以外的“.”符号，请保证路径和文件中没有除“.py”以外的“.”符号\n" \
            f"例如：C:/123.445/run.py 中123.445文件夹包含了“.”符号，该符号将可能导致Python程序运行终止，请修改该类情况！"
        assert " " not in self.launcher_py_path, \
            f"{self.launcher_py_path}中的路径或文件名中出现了空格符号，请删去文件夹或文件名中的空格\n" \
            f"例如：C:/123 445/run.py 中123 445文件夹包含了空格符号，该符号将可能导致Python程序运行终止，请修改该类情况！"

        self.work_dir = work_dir
        assert os.path.exists(os.path.join(self.work_dir, self.launcher_py_path)), \
            f"请检查{launcher_py_path}文件是否存在{self.work_dir}目录"
        # try:
        #     # 兼容不同盘符情况
        #     check_same_path = os.path.abspath(os.path.relpath(save_path, work_dir))
        # except ValueError:
        #     check_same_path = save_path + "-"
        # assert check_same_path not in os.path.abspath(save_path), \
        #     "打包后的保存路径不能在被打包的文件夹中，这样会打包了打包后的文件^n (,,•́ . •̀,,)"
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path, exist_ok=True)
        self.module_path = os.path.join(save_path, "Release")
        self.debug_path = os.path.join(save_path, "Debug")
        self.interpreter_path = os.path.join(self.module_path, "Python")
        if ignore_dirs is None:
            self.ignore_dirs = list()

        # 配置操作参数
        set_default_deploy_mode(deploy_mode)
        set_default_pip_lib(self.interpreter_path)
        self.with_debug = with_debug
        self.hidden_terminal = hidden_terminal

        # 新建配置信息
        self.configs = dict()
        self.configs["launcher_py_path"] = self.launcher_py_path
        self.configs["hidden_terminal"] = hidden_terminal
        self.configs["module_name"] = module_name
        self.configs["author"] = author
        self.configs["version"] = version
        self.configs["lazy_module"] = list()
        self.configs["sub_module"] = list()
        self.configs["local_uid"] = base64.b64encode((os.path.abspath(sys.executable) + "|" +
                                                      os.path.abspath(qpt.__file__) + "|" +
                                                      os.path.abspath(self.module_path)).encode('utf-8'))

        # 额外的成员变量
        self.resources_path = os.path.join(self.module_path, "resources")
        self.config_path = os.path.join(self.module_path, "configs")
        self.config_file_path = os.path.join(self.module_path, "configs", "configs.gt")
        self.dependent_file_path = os.path.join(self.module_path, "configs", "dependent.gt")
        self.lib_package_path = os.path.join(self.interpreter_path,
                                             com_configs["RELATIVE_INTERPRETER_SITE_PACKAGES_PATH"])

        # 设置全局下载的Python包默认解释器版本号 - 更换兼容性方案
        # set_default_package_for_python_version(interpreter_module.python_version)

        # 避免打包虚拟环境等
        venv_dir = "-%NONE-FLAG%-"
        for root, dirs, files in os.walk(self.work_dir):
            if "pyvenv.cfg" in files:
                venv_dir = root
                self.ignore_dirs.append(root)
                Logging.warning(f"检测到pyvenv.cfg，推测出{os.path.abspath(root)}为Python虚拟环境主目录，在打包时会忽略该目录")
                continue
            if ".github" in dirs:
                self.ignore_dirs.append(os.path.join(root, ".github"))
                Logging.warning(f"检测到.github，推测出{os.path.abspath(root)}为.github目录，在打包时会忽略该目录")
            if ".git" in dirs:
                self.ignore_dirs.append(os.path.join(root, ".git"))
                Logging.warning(f"检测到.git，推测出{os.path.abspath(root)}为.git目录，在打包时会忽略该目录")
            if ".idea" in dirs:
                self.ignore_dirs.append(os.path.join(root, ".idea"))
                Logging.warning(f"检测到.idea，推测出{os.path.abspath(root)}为.idea目录，在打包时会忽略该目录")
            if "__pycache__" in dirs and not (venv_dir in root and root.index(venv_dir) == 0):
                self.ignore_dirs.append(os.path.join(root, "__pycache__"))

        # Module相关
        # 初始化解释器Module
        if interpreter_module is None:
            interpreter_module = AutoPythonEnv()
        # 获取SubModule列表 - 此处均无ExtModule
        self.lazy_modules = [interpreter_module, QPTDependencyPackage()]

        self.sub_modules = sub_modules if sub_modules is not None else list()

        # 放入增强包
        self.add_sub_module(BatchInstallation())
        # 放入QT增强包
        if self.hidden_terminal:
            self.add_sub_module(QPTGUIDependencyPackage())

        # 解析依赖
        if requirements_file == "auto":
            auto_dependency_module = AutoRequirementsPackage(path=self.work_dir,
                                                             deploy_mode=deploy_mode)
        else:
            auto_dependency_module = AutoRequirementsPackage(path=requirements_file,
                                                             deploy_mode=deploy_mode)
        self.add_sub_module(auto_dependency_module)

        # 初始化终端 - 占位 待lazy_module执行完毕后生成终端（依赖Qt lazy module）
        self.terminal = None

    def add_sub_module(self, sub_module: SubModule, lazy=False):
        """
        为Module添加子模块
        """
        module = sub_module.get_all_module()
        if len(module) > 1:
            for em in module[1:]:
                self.add_sub_module(em)
        if lazy:
            self.lazy_modules += [sub_module]
        else:
            self.sub_modules.append(sub_module)

    def print_details(self):
        Logging.info("----------QPT执行使用了以下OP----------")
        for module in self.lazy_modules:
            Logging.info(module.__class__.__name__ + f"执行优先级{module.level}" + f"\t{module.details}")
        Logging.info("----------程序执行使用了以下OP----------")
        for module in self.sub_modules:
            Logging.info(module.__class__.__name__ + f"优先级{module.level}" + f"\t{module.details}")
        Logging.info("------------------------------------")

    def _solve_module(self, lazy=False):
        if lazy:
            modules = self.lazy_modules
            # lazy mode 不支持terminal
            terminal = None
        else:
            self.terminal = AutoTerminal()
            modules = self.sub_modules
            terminal = self.terminal.shell_func()
        # 依靠优先级进行排序
        modules.sort(key=lambda m: m.level, reverse=True)
        for sub in modules:
            # ToDO设置序列化路径
            sub._module_path = self.module_path
            # 需对每个module设置save_dir和终端
            sub.prepare(work_dir=self.work_dir,
                        interpreter_path=os.path.join(self.module_path, "Python"),
                        module_path=self.module_path,
                        terminal=terminal)
            sub.pack()

            # 保护用户侧接触不到的模块不被泄漏模块名
            if len(sub.unpack_opts) != 0:
                if lazy:
                    self.configs["lazy_module"].append(sub.name)
                else:
                    self.configs["sub_module"].append(sub.name)

    def make(self):
        # 打印sub module信息
        self.print_details()

        # 创建基本环境目录
        if os.path.exists(self.save_path):
            if os.path.exists(self.resources_path):
                Logging.warning(f"{os.path.abspath(self.module_path)}已存在，已清空该目录")
                self.ignore_dirs.append(self.module_path)
                shutil.rmtree(self.module_path)
            if os.path.exists(self.debug_path):
                Logging.warning(f"{os.path.abspath(self.debug_path)}已存在，已清空该目录")
                self.ignore_dirs.append(self.debug_path)
                shutil.rmtree(self.debug_path)
        else:
            os.makedirs(self.save_path, exist_ok=True)

        # 解析子模块
        self._solve_module(lazy=True)
        self._solve_module()

        # 复制资源文件
        assert os.path.exists(self.work_dir), f"{os.path.abspath(self.work_dir)}不存在，请检查该路径是否正确"
        copytree(self.work_dir, self.resources_path, ignore_dirs=self.ignore_dirs)

        # QPT的dev模式
        if self.with_debug:
            Logging.debug("当前已开启QPT-dev模式，将会复制当前版本的QPT文件至相应目录")
            qpt_dir_path = os.path.split(qpt.__file__)[0]
            copytree(src=qpt_dir_path, dst=os.path.join(self.interpreter_path, "Lib/site-packages/qpt"))

        # 避免出现if __name__ == '__main__':
        with open(os.path.join(self.resources_path, self.launcher_py_path), "r", encoding="utf-8") as lf:
            lf_codes = lf.readlines()
        for lf_code_id, lf_code in enumerate(lf_codes):
            if "if" in lf_code and "__name__" in lf_code and "__main__" in lf_code:
                # 懒得写正则了嘿嘿嘿
                Logging.warning(f"{self.launcher_py_path}中包含if __name__ == '__main__'语句，"
                                f"由于用户使用时QPT成为了主程序，故此处代码块会被Python忽略。"
                                f"为保证可以正常执行，当前已自动修复该问题")
                with open(os.path.join(self.resources_path, self.launcher_py_path), "w", encoding="utf-8") as new_lf:
                    lf_codes[lf_code_id] = lf_code[:lf_code.index("if ")] + "if 'qpt':\n"
                    new_lf.writelines(lf_codes)

        # 创建配置文件
        os.makedirs(self.config_path, exist_ok=True)
        with open(self.config_file_path, "w", encoding="utf-8") as config_file:
            config_file.write(str(self.configs))

        # 启动器相关
        launcher_entry_path = os.path.join(os.path.split(qpt.__file__)[0], "ext/launcher_entry")
        # 复制Debug所需文件
        debug_ext_dir = os.path.join(os.path.split(qpt.__file__)[0], "ext/launcher_debug")
        copytree(debug_ext_dir, dst=self.debug_path)
        copytree(self.module_path, dst=self.debug_path)
        shutil.copy(src=os.path.join(launcher_entry_path, "entry_debug.cmd"),
                    dst=os.path.join(self.debug_path, "configs/entry.cmd"))
        # 生成Debug标识符
        unlock_file_path = os.path.join(self.debug_path, "configs/unlock.cache")
        with open(unlock_file_path, "w", encoding="utf-8") as unlock_file:
            unlock_file.write(str(datetime.datetime.now()))
        # 重命名兼容模式文件
        compatibility_mode_file = os.path.join(self.debug_path, "compatibility_mode.cmd")
        if os.path.exists(compatibility_mode_file):
            os.rename(compatibility_mode_file,
                      os.path.join(self.debug_path, "使用兼容模式运行.cmd"))

        # 复制Release启动器文件
        launcher_ext_dir = os.path.join(os.path.split(qpt.__file__)[0], "ext/launcher")
        launcher_ignore_file = None
        if self.hidden_terminal:
            shutil.copy(src=os.path.join(launcher_entry_path, "entry_run_hidden.cmd"),
                        dst=os.path.join(self.module_path, "configs/entry.cmd"))
        else:
            launcher_ignore_file = ["Main.exe"]
            shutil.copy(src=os.path.join(debug_ext_dir, "Debug.exe"), dst=os.path.join(self.module_path, "启动程序.exe"))
            shutil.copy(src=os.path.join(launcher_entry_path, "entry_run.cmd"),
                        dst=os.path.join(self.module_path, "configs/entry.cmd"))

        copytree(launcher_ext_dir, dst=self.module_path, ignore_files=launcher_ignore_file)
        # 重命名兼容模式文件
        compatibility_mode_file = os.path.join(self.module_path, "compatibility_mode.cmd")
        if os.path.exists(compatibility_mode_file):
            os.rename(compatibility_mode_file,
                      os.path.join(self.module_path, "使用兼容模式运行.cmd"))

        # 重命名启动器文件
        launcher_file = os.path.join(self.module_path, "Main.exe")
        if os.path.exists(launcher_file):
            os.rename(launcher_file,
                      os.path.join(self.module_path, "启动程序.exe"))

        # 收尾工作
        Logging.info(f"\n制作完毕，保存位置为：{os.path.abspath(self.module_path)}，该目录下将会有以下文件夹\n"
                     f"| ----------------------------------------------------------------------------- |\n"
                     f"| Debug目录：\t该目录下提供了Debug环境，可简单验证打包后程序是否可以正常执行。        \n"
                     f"| Release目录：\t将该目录进行压缩，并发给您的用户，待您的用户打开该压缩包下的“启动程序.exe”后\n"
                     f"|             \t即可启动您制作的程序  \n"
                     f"| ----------------------------------------------------------------------------- |\n")
        Logging.warning(f"\n| ---------------------------------Warning!------------------------------------ |\n"
                        f"| 请勿在本机打开Release目录下的“启动程序.exe”文件，原因如下： \n"
                        f"| 1. 该程序会加载“一次性部署模块”，部署后该模块会消失，消失后可能无法在其他电脑上使用。\n"
                        f"| 2. 该程序会解压缩当前环境，执行“启动程序.exe”后整个目录大小可能会增加1~5倍。（取决于压缩率）\n"
                        f"| 3. 若需要测试打包后程序是否可以正常运行，请在Debug目录下进行测试。\n"
                        f"| 4. 若特殊情况必须在Release目录下进行测试，请制作Release目录的备份，在他人需要时提供该备份\n"
                        f"|    文件或重新打包，以避免因执行“启动程序.exe”后丢失“一次性部署模块”，从而无法被他人使用。\n"
                        f"| ----------------------------------------------------------------------------- |\n")

        sys.stdout.flush()
        Logging.info("是否需要保留QPT在打包时产生的缓存文件？若不清空则可能会在下次使用QPT时复用缓存以提升打包速度")
        clear_key = input("[保留(Y)/清空(N)]:_")
        sys.stdout.flush()
        if clear_key.lower() == "n":
            clean_qpt_cache()
            Logging.info("QPT缓存已全部清空")


class RunExecutableModule:
    def __init__(self, module_path):
        import win32api
        import win32con
        self.win32api = win32api
        self.win32con = win32con
        # 初始化Module信息
        self.base_dir = os.path.abspath(module_path)
        self.config_path = os.path.join(self.base_dir, "configs")
        self.config_file_path = os.path.join(self.base_dir, "configs", "configs.gt")
        self.dependent_file_path = os.path.join(self.base_dir, "configs", "dependent.gt")
        self.work_dir = os.path.join(self.base_dir, "resources")
        self.interpreter_path = os.path.join(self.base_dir, "Python")

        # 初始化Log
        log_name = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-") + ".txt"
        if not os.path.exists(os.path.join(self.config_path, "logs")):
            log_name = "First-" + log_name
            os.mkdir(os.path.join(self.config_path, "logs"))
        if QPT_MODE == "Debug":
            log_name = "#Debug#" + log_name
        set_logger_file(os.path.join(self.config_path, "logs", "QPT-" + log_name))
        sys.stdout = StdOutLoggerWrapper(os.path.join(self.config_path, "logs", "APP-" + log_name))

        # 向用户提出申请UA保护
        add_ua()

        # 系统信息
        check_all()

        # 强制本地PIP
        set_default_pip_lib(self.interpreter_path)

        # 检查路径是否非法
        check_path = __file__
        if check_chinese_char(check_path) or " " in check_path:
            self.warning_msg_box(text=f"{self.base_dir}\n"
                                      f"警告！当前路径中包含中文或空格，部分软件包将无法运行，强烈建议您修改相关的文件夹名，\n"
                                      f"---------------------------------------\n"
                                      f"不符合规范的路径如下：\n"
                                      f"C:/GT真菜/xxx/yyy      -   ！“GT真菜”带有中文！\n"
                                      f"C:/zzz/GT真 菜/yyy     -   ！“GT真 菜”中带有空格！\n"
                                      f"---------------------------------------\n"
                                      f"符合规范的路径如下：\n"
                                      f"C:/hello/xxx/yyy\n"
                                      f"---------------------------------------\n"
                                      f"当然，您也可将Windows系统的默认编码模式更改为UTF-8，这可以更好兼容中文，但操作难度较高。\n"
                                      f"---------------------------------------\n"
                                      f"请修改相关文件名后重新运行，谢谢！",
                                 force=True)
            Logging.info("程序已停止")
            exit(1)

        with open(self.config_file_path, "r", encoding="utf-8") as config_file:
            self.configs = eval(config_file.read())

        # 获取GUI选项
        self.hidden_terminal = self.configs["hidden_terminal"]

        # 获取Module
        self.lazy_module = self.configs["lazy_module"]
        self.sub_module = self.configs["sub_module"]

    def warning_msg_box(self, title="Warning - QPT", text="", force=False):
        """
        发出警告框
        :param title: 标题
        :param text: 文本
        :param force: 是否强制只有确定按钮
        :return: 用户反馈
        """
        if force:
            flag = self.win32con.MB_OK | self.win32con.MB_ICONEXCLAMATION
        else:
            flag = self.win32con.MB_OKCANCEL | self.win32con.MB_ICONEXCLAMATION
        msg = self.win32api.MessageBox(0, text, title, flag)
        if not force and msg == 2:
            return False
        else:
            return True

    def _solve_module(self):
        modules = self.lazy_module + self.sub_module
        if self.hidden_terminal:
            from qpt.gui.qpt_unzip import Unzip
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtGui import QIcon
            auto_terminal = AutoTerminal()
            terminal = auto_terminal.shell_func()
            app = QApplication(sys.argv)
            unzip_bar = Unzip()
            unzip_bar.setWindowIcon(QIcon(os.path.join(self.base_dir, "configs/Logo.ico")))
            unzip_bar.show()
            for sub_module_id, sub_name in enumerate(modules):
                sub_module = SubModule(sub_name)
                sub_module.prepare(work_dir=self.work_dir,
                                   interpreter_path=self.interpreter_path,
                                   module_path=self.base_dir,
                                   terminal=terminal)
                sub_module.unpack()
                unzip_bar.update_value(min((sub_module_id + 1) / len(modules) * 100, 99))
                unzip_bar.update_title(f"正在初始化：{sub_name}")
                app.processEvents()
            unzip_bar.close()
            # app.exit()
        else:
            auto_terminal = AutoTerminal()
            terminal = auto_terminal.shell_func()
            tp = TProgressBar("初始化进度", max_len=len(modules) + 1)
            for sub_module_id, sub_name in enumerate(modules):
                tp.step(add_end_info=f"{sub_name}部署中...")
                sub_module = SubModule(sub_name)
                sub_module.prepare(work_dir=self.work_dir,
                                   interpreter_path=self.interpreter_path,
                                   module_path=self.base_dir,
                                   terminal=terminal)
                sub_module.unpack()
            tp.step(add_end_info=f"初始化完毕")

    def solve_work_dir(self):
        # ToDo 加个Lock 彻底去除非Python的环境变量
        # Set Sys ENV
        sys.path.append(self.work_dir)
        sys.path.append(os.path.abspath("./Python/Lib/site-packages"))
        sys.path.append(os.path.abspath("./Python/Lib/ext"))
        sys.path.append(os.path.abspath("./Python/Lib"))
        sys.path.append(os.path.abspath("./Python"))
        sys.path.append(os.path.abspath("./Python/Scripts"))

        # Set PATH ENV
        path_env = os.environ.get("path").split(";")
        ignore_env_field = ["conda", "Python", "python"]
        pre_add_env = os.path.abspath("./Python/Lib/site-packages") + ";" + \
                      os.path.abspath("./Python/Lib") + ";" + \
                      os.path.abspath("./Python/Lib/ext") + ";" + \
                      os.path.abspath("./Python") + ";" + \
                      os.path.abspath("./Python/Scripts") + ";"

        for pe in path_env:
            if pe:
                add_flag = True
                for ief in ignore_env_field:
                    if ief in pe:
                        add_flag = False
                        break
                if add_flag:
                    pre_add_env += pe + ";"
        os.environ["PATH"] = pre_add_env

        # Set PYTHON PATH ENV
        os.environ["PYTHONPATH"] = os.path.abspath("./Python/Lib/site-packages") + ";" + \
                                   self.work_dir + ";" + \
                                   os.path.abspath("./Python")

    def run(self):
        # 设置工作目录
        self.solve_work_dir()

        # 获取启动信息 - 避免在Release下进行Debug
        env_warning_flag = False
        local_uid = base64.b64decode(self.configs["local_uid"]).decode("utf-8")
        if all([os.path.exists(uid) for uid in local_uid.split("|")]):
            env_warning_flag = True
        lock_file_path = os.path.join(self.config_path, "unlock.cache")
        if os.path.exists(lock_file_path):
            env_warning_flag = False

        if env_warning_flag:
            msg = self.warning_msg_box("Warning", f"非常不建议在该环境下进行调试，原因如下： \n"
                                                  f" 1. 继续执行将会加载“一次性部署模块”，部署后该模块会消失，消失后可能无法在其他电脑上使用。\n"
                                                  f" 2. 该程序会解压缩当前环境，执行“启动程序.exe”后整个目录大小可能会增加1~5倍。（取决于压缩率）\n"
                                                  f" 3. 若需要测试打包后程序是否可以正常运行，请在Debug目录下进行测试。\n"
                                                  f" 4. 若特殊情况必须在Release目录下进行测试，请制作Release目录的备份，在他人需要时提供该备份\n"
                                                  f"    文件或重新打包，以避免因执行“启动程序.exe”后丢失“一次性部署模块”，从而无法被他人使用。\n"
                                                  f"---------------------------------------------------------------------------\n"
                                                  f"请问是否还要在该环境下继续执行？")
            if not msg:
                Logging.info("程序已停止")
                exit(1)
        # prepare module - GUI组件需要在此之后才能进行
        self._solve_module()

        # 执行主程
        main_lib_path = self.configs["launcher_py_path"].replace(".py", "")
        main_lib_path = main_lib_path. \
            replace(".py", ""). \
            replace(r"\\", "."). \
            replace("\\", "."). \
            replace("/", ".")
        # ToDo 等日志系统做好了再取消注释
        # os.system('cls')
        lib = importlib.import_module(main_lib_path)
        # input("QPT执行完毕，请按任意键退出")
