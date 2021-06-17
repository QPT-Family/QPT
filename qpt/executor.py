import os
import sys
import shutil
import importlib
import datetime
import base64

from typing import List

import qpt
from qpt._compatibility import com_configs
from qpt.modules.base import SubModule
from qpt.modules.python_env import BasePythonEnv, AutoPythonEnv
from qpt.modules.package import AutoRequirementsPackage, QPTDependencyPackage, DEFAULT_DEPLOY_MODE

from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.os_op import clean_qpt_cache


class CreateExecutableModule:
    def __init__(self,
                 work_dir,
                 launcher_py_path,
                 save_path,
                 requirements_file="auto",
                 deploy_mode=DEFAULT_DEPLOY_MODE,
                 sub_modules: List[SubModule] = None,
                 interpreter_module: BasePythonEnv = AutoPythonEnv(),
                 module_name="未命名模型",
                 version="未知版本号",
                 author="未知作者",
                 none_gui: bool = False,
                 with_debug: bool = True):
        # 初始化路径成员变量
        self.launcher_py_path = os.path.abspath(launcher_py_path).replace(os.path.abspath(work_dir) + "\\", "./")
        self.work_dir = work_dir
        self.save_path = save_path
        self.module_path = os.path.join(save_path, "Release")
        self.debug_path = os.path.join(save_path, "Debug")
        self.interpreter_path = os.path.join(self.module_path, "Python")

        self.with_debug = with_debug

        # 新建配置信息
        self.configs = dict()
        self.configs["launcher_py_path"] = self.launcher_py_path
        self.configs["none_gui"] = none_gui
        self.configs["module_name"] = module_name
        self.configs["author"] = author
        self.configs["version"] = version
        self.configs["lazy_module"] = list()
        self.configs["sub_module"] = list()
        self.configs["local_uid"] = base64.b64encode(os.path.abspath(os.path.abspath(launcher_py_path)).encode('utf-8'))

        # 额外的成员变量
        self.resources_path = os.path.join(self.module_path, "resources")
        self.config_path = os.path.join(self.module_path, "configs")
        self.config_file_path = os.path.join(self.module_path, "configs", "configs.gt")
        self.dependent_file_path = os.path.join(self.module_path, "configs", "dependent.gt")
        self.lib_package_path = os.path.join(self.interpreter_path,
                                             com_configs["RELATIVE_INTERPRETER_SITE_PACKAGES_PATH"])

        # 设置全局下载的Python包默认解释器版本号 - 更换兼容性方案
        # set_default_package_for_python_version(interpreter_module.python_version)

        # 获取SubModule列表
        self.lazy_module = [interpreter_module, QPTDependencyPackage()]

        if none_gui is False:
            pass
        self.sub_module = sub_modules if sub_modules is not None else list()

        # 解析依赖
        if requirements_file == "auto":
            auto_dependency_module = AutoRequirementsPackage(path=self.work_dir,
                                                             module_list=self.sub_module,
                                                             deploy_mode=deploy_mode)
        else:
            auto_dependency_module = AutoRequirementsPackage(path=requirements_file,
                                                             module_list=self.sub_module,
                                                             deploy_mode=deploy_mode)
        self.sub_module.append(auto_dependency_module)

        # 初始化终端 - 占位 待lazy_module执行完毕后生成终端（依赖Qt lazy module）
        self.terminal = None

    def add_sub_module(self, sub_module: SubModule):
        """
        为Module添加子模块
        """
        self.sub_module.append(sub_module)

    def print_details(self):
        Logging.info("----------QPT执行使用了以下OP----------")
        for module in self.lazy_module:
            Logging.info(module.__class__.__name__ + f"\t{module.details}")
        Logging.info("----------程序执行使用了以下OP----------")
        for module in self.sub_module:
            Logging.info(module.__class__.__name__ + f"\t{module.details}")
        Logging.info("------------------------------------")

    def _solve_module(self, lazy=False):
        if lazy:
            modules = self.lazy_module
            # lazy mode 不支持terminal
            terminal = None
        else:
            from qpt.kernel.tools.qpt_qt import QTerminal, MessageBoxTerminalCallback
            self.terminal = QTerminal()
            modules = self.sub_module
            terminal = self.terminal.shell_func(callback=MessageBoxTerminalCallback())
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
            Logging.warning(f"{os.path.abspath(self.save_path)}已存在，已清空该目录")
            shutil.rmtree(self.save_path)
        os.mkdir(self.save_path)

        # 解析子模块
        self._solve_module(lazy=True)
        self._solve_module()

        # 复制资源文件
        assert os.path.exists(self.work_dir), f"{os.path.abspath(self.work_dir)}不存在，请检查该路径是否正确"
        shutil.copytree(self.work_dir, self.resources_path)

        # 创建配置文件
        os.makedirs(self.config_path, exist_ok=True)
        with open(self.config_file_path, "w", encoding="utf-8") as config_file:
            config_file.write(str(self.configs))

        # 复制Debug所需文件
        if self.with_debug:
            debug_dir = os.path.join(os.path.split(qpt.__file__)[0], "ext/launcher_debug")
            shutil.copytree(debug_dir, dst=self.debug_path, dirs_exist_ok=True)
            shutil.copytree(self.module_path, dst=self.debug_path, dirs_exist_ok=True)
            # 生成Debug标识符
            unlock_file_path = os.path.join(self.debug_path, "configs/unlock.cache")
            with open(unlock_file_path, "w", encoding="utf-8") as unlock_file:
                unlock_file.write(str(datetime.datetime.now()))

        # 复制Release启动器文件
        launcher_dir = os.path.join(os.path.split(qpt.__file__)[0], "ext/launcher")
        shutil.copytree(launcher_dir, dst=self.module_path, dirs_exist_ok=True)

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

        Logging.info("是否需要保留QPT在打包时产生的缓存文件？若不清空则可能会在下次使用QPT时复用缓存以提升打包速度")
        clear_key = input("[保留(Y)/清空(N)]:_")
        if clear_key.lower() == "n":
            clean_qpt_cache()
            Logging.info("QPT缓存已全部清空")


class RunExecutableModule:
    def __init__(self, module_path):
        # 初始化Module信息
        self.base_dir = os.path.abspath(module_path)
        self.config_path = os.path.join(self.base_dir, "configs")
        self.config_file_path = os.path.join(self.base_dir, "configs", "configs.gt")
        self.dependent_file_path = os.path.join(self.base_dir, "configs", "dependent.gt")
        self.work_dir = os.path.join(self.base_dir, "resources")
        self.interpreter_path = os.path.join(self.base_dir, "Python")

        with open(self.config_file_path, "r", encoding="utf-8") as config_file:
            self.configs = eval(config_file.read())

        # 初始化终端
        self.terminal = None

        # 获取Module
        self.lazy_module = self.configs["lazy_module"]
        self.sub_module = self.configs["sub_module"]

    def solve_qpt_env(self):
        # ToDO 集市部分代码
        pass

    def _solve_module(self):
        modules = self.lazy_module + self.sub_module
        from qpt.kernel.tools.qpt_qt import QTerminal, MessageBoxTerminalCallback
        from qpt.gui.qpt_unzip import Unzip
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QIcon
        self.terminal = QTerminal()
        terminal = self.terminal.shell_func(callback=MessageBoxTerminalCallback())
        app = QApplication(sys.argv)
        unzip_bar = Unzip()
        unzip_bar.setWindowIcon(QIcon(os.path.join(self.base_dir, "Logo.ico")))
        unzip_bar.show()
        for sub_module_id, sub_name in enumerate(modules):
            sub_module = SubModule(sub_name)
            sub_module.prepare(work_dir=self.work_dir,
                               interpreter_path=self.interpreter_path,
                               module_path=self.base_dir,
                               terminal=terminal)
            sub_module.unpack()
            unzip_bar.update_value(sub_module_id / len(self.sub_module) * 100)
            unzip_bar.update_title(f"正在初始化：{sub_name}")
            app.processEvents()

    def unzip_resources(self):
        # ToDO 增加单文件执行模式，优先级暂时靠后
        pass

    def solve_work_dir(self):
        os.chdir(self.work_dir)
        sys.path.append(self.work_dir)

    def run(self):
        # 获取启动信息 - 避免在Release下进行Debug
        env_warning_flag = True
        local_uid = base64.b64decode(self.configs["local_uid"]).decode("utf-8")
        if os.path.exists(local_uid):
            env_warning_flag = True
        lock_file_path = os.path.join(self.config_path, "unlock.cache")
        if os.path.exists(lock_file_path):
            env_warning_flag = False

        # if env_warning_flag:
        #     try:
        #         from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
        #         app = QApplication(sys.argv)
        #         widget = QWidget()
        #         msg = QMessageBox.information(widget,
        #                                       'Warning',
        #                                       f"非常不建议在该环境下进行调试，原因如下： \n"
        #                                       f" 1. 继续执行将会加载“一次性部署模块”，部署后该模块会消失，消失后可能无法在其他电脑上使用。\n"
        #                                       f" 2. 该程序会解压缩当前环境，执行“启动程序.exe”后整个目录大小可能会增加1~5倍。（取决于压缩率）\n"
        #                                       f" 3. 若需要测试打包后程序是否可以正常运行，请在Debug目录下进行测试。\n"
        #                                       f" 4. 若特殊情况必须在Release目录下进行测试，请制作Release目录的备份，在他人需要时提供该备份\n"
        #                                       f"    文件或重新打包，以避免因执行“启动程序.exe”后丢失“一次性部署模块”，从而无法被他人使用。\n"
        #                                       f"-----------------------------------------------------------------------------\n"
        #                                       f"请问是否还要在该环境下继续执行？",
        #                                       QMessageBox.Yes | QMessageBox.No)
        #         if msg == QMessageBox.No:
        #             exit(0)
        #         widget.close()
        #         app.exit()
        #     except Exception as e:
        #         Logging.error("部署失败，报错信息如下：\n" + str(e))

        # prepare module - GUI组件需要在此之后才能进行
        self._solve_module()

        # 设置工作目录
        self.solve_work_dir()
        # 执行主程序
        main_lib_path = self.configs["launcher_py_path"].replace(".py", "")
        assert "." not in main_lib_path[1:], "封装Module时需要避免路径中带有'.'字符，该字符将影响执行程序"
        main_lib_path = main_lib_path[2:]. \
            replace(".py", ""). \
            replace(r"\\", "."). \
            replace("\\", "."). \
            replace("/", ".")
        # 需提醒用户避免使用if __name__ == '__main__':
        # ToDO 必要时删除该字段并代码块整体缩进一格
        lib = importlib.import_module(main_lib_path)
        input("QPT执行完毕，请按任意键退出")
