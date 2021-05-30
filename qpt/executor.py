import os
import sys
import shutil
import importlib

from typing import List

from qpt._compatibility import com_configs

from qpt.modules.base import SubModule
from qpt.modules.python_env import BasePythonEnv, AutoPythonEnv
from qpt.modules.package import AutoRequirementsPackage, QPTDependencyPackage, DEFAULT_DEPLOY_MODE, \
    set_default_package_for_python_version

from qpt.kernel.tools.log_op import Logging


class CreateExecutableModule:
    def __init__(self,
                 launcher_py_path,
                 work_dir,
                 save_path,
                 auto_dependency=True,
                 deploy_mode=DEFAULT_DEPLOY_MODE,
                 sub_modules: List[SubModule] = None,
                 interpreter_module: BasePythonEnv = AutoPythonEnv(),
                 module_name="未命名模型",
                 version="未知版本号",
                 author="未知作者",
                 none_gui: bool = False):
        # 初始化路径成员变量
        self.launcher_py_path = os.path.abspath(launcher_py_path).replace(os.path.abspath(work_dir) + "\\", "./")
        self.work_dir = work_dir
        self.module_path = save_path
        self.interpreter_path = os.path.join(self.module_path, "Python")

        # 新建配置信息
        self.configs = dict()
        self.configs["launcher_py_path"] = self.launcher_py_path
        self.configs["none_gui"] = none_gui
        self.configs["module_name"] = module_name
        self.configs["author"] = author
        self.configs["version"] = version
        self.configs["lazy_module"] = list()
        self.configs["sub_module"] = list()

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
        if auto_dependency:
            auto_dependency_module = AutoRequirementsPackage(work_home=self.work_dir,
                                                             module_list=self.sub_module,
                                                             deploy_mode=deploy_mode)
            self.sub_module.append(auto_dependency_module)

        # 初始化终端 - 占位 待lazy_module执行完毕后生成终端（依赖Qt lazy module）
        self.terminal = None

    # ToDO 增加对子工作目录支持
    # def add_sub_workdir(self, path):
    #     pass

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
            terminal = None
        else:
            from qpt.kernel.tools.qpt_qt import QTerminal, MessageBoxTerminalCallback
            self.terminal = QTerminal()
            modules = self.sub_module
            terminal = self.terminal.shell_func(callback=MessageBoxTerminalCallback())
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
        if os.path.exists(self.module_path):
            Logging.warning(f"{os.path.abspath(self.module_path)}已存在，已清空该目录")
            shutil.rmtree(self.module_path)
        os.mkdir(self.module_path)

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

        # ToDO 复制启动器文件

        # 结束
        Logging.info(f"制作完毕，保存位置为：{os.path.abspath(self.module_path)}")


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
        # ToDO 增加NoneGUI模式
        if self.configs["none_gui"] is False:
            pass

    def solve_python_env(self):
        # ToDO 解决集市部分包管理问题
        pass

    def _solve_module(self, lazy=False):
        if lazy:
            modules = self.lazy_module
            terminal = None
        else:
            from qpt.kernel.tools.qpt_qt import QTerminal, MessageBoxTerminalCallback
            self.terminal = QTerminal()
            modules = self.sub_module
            terminal = self.terminal.shell_func(callback=MessageBoxTerminalCallback())
        for sub_name in modules:
            sub_module = SubModule(sub_name)
            sub_module.prepare(work_dir=self.work_dir,
                               interpreter_path=self.interpreter_path,
                               module_path=self.base_dir,
                               terminal=terminal)
            sub_module.unpack()

    def unzip_resources(self):
        # ToDO 增加单文件执行模式，优先级暂时靠后
        pass

    def solve_work_dir(self):
        os.chdir(self.work_dir)
        sys.path.append(self.work_dir)

    def run(self):
        # prepare qpt lazy module - GUI组件需要在此之后才能进行
        self._solve_module(lazy=True)
        # prepare module
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
        # ToDO 必要时自动替换对应字段，并生成类似混淆名称的函数，在程序末尾执行run
        lib = importlib.import_module(main_lib_path)
        input("QPT执行完毕，请按任意键退出")
