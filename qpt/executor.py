# Author: Acer Zhang
# Datetime: 2021/5/26
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import base64
import datetime
import logging
import os
import shutil
import sys
import tempfile
from typing import List

import qpt
from qpt.gui.tk_progressbar import get_func_bind_progressbar
from qpt.kernel.qlog import Logging, TProgressBar, set_logger_file
from qpt.kernel.qos import clean_qpt_cache, copytree, check_warning_char, StdOutLoggerWrapper, warning_msg_box
from qpt.kernel.qpe import make_icon
from qpt.kernel.qterminal import PTerminal
from qpt.memory import QPT_MEMORY
from qpt.memory import QPT_MODE, CheckRun
from qpt.modules.auto_requirements import AutoRequirementsPackage
from qpt.modules.base import SubModule
from qpt.modules.package import QPTDependencyPackage, QPTGUIDependencyPackage, \
    DEFAULT_DEPLOY_MODE, set_default_deploy_mode, CheckCompileCompatibility
from qpt.modules.python_env import BasePythonEnv, AutoPythonEnv
from qpt.smart_opt import set_default_pip_lib
from qpt.version import version as qpt_v

__all__ = ["CreateExecutableModule", "RunExecutableModule"]


class CreateExecutableModule:
    def __init__(self,
                 work_dir,
                 launcher_py_path,
                 save_path,
                 ignore_dirs: list = None,
                 requirements_file="auto",
                 icon=None,
                 deploy_mode=DEFAULT_DEPLOY_MODE,
                 sub_modules: List[SubModule] = None,
                 interpreter_version: int = None,
                 hidden_terminal: bool = False,
                 with_debug: bool = False):
        """
        :param work_dir: 待打包的项目路径，打包后会放置在resources目录下
        :param launcher_py_path: 主程序路径
        :param save_path: 打包后文件所在位置
        :param ignore_dirs: 不进行打包的文件列表
        :param requirements_file: 可供pip读取的环境依赖列表
        :param icon: 主程序图标
        :param deploy_mode: 部署方式，默认为“本地下载后安装”，填写为“setup_install”将减少初始化时间，但会增加体积
        :param sub_modules: 子模块列表
        :param interpreter_version: 解释器Module，例如39、310、311，无子版本号
        :param hidden_terminal: 是否隐藏界面
        :param with_debug: QPT验证模式 - 请勿使用
        """

        Logging.warning(
            msg="QPT 1.0b5版本中有较大更新，且仅对Win10 1809以上版本进行验证，低于该版本的操作系统可能存在无法运行问题。")
        self.with_debug = with_debug
        self.work_dir = work_dir

        # 初始化路径成员变量
        # 主程序文件变量
        self.launcher_py_path = list()

        def make_launcher_py_path(lp_path):
            _launcher_py_path = os.path.relpath(lp_path, work_dir)
            if _launcher_py_path[:1] == "\\":
                _launcher_py_path = _launcher_py_path[1:]

            assert " " not in _launcher_py_path, \
                f"{_launcher_py_path}中的路径或文件名中出现了空格符号，请删去文件夹或文件名中的空格\n" \
                f"例如：C:/123 445/run.py 中123 445文件夹包含了空格符号，该符号将可能导致Python程序运行终止，请修改该类情况！"
            assert os.path.exists(os.path.join(self.work_dir, _launcher_py_path)), \
                f"请检查{lp_path}文件是否存在{self.work_dir}目录"
            return _launcher_py_path

        if isinstance(launcher_py_path, list):
            for lpp in launcher_py_path:
                self.launcher_py_path.append(make_launcher_py_path(lp_path=lpp))
        else:
            self.launcher_py_path.append(make_launcher_py_path(lp_path=launcher_py_path))

        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path, exist_ok=True)
        self.module_path = os.path.join(save_path, "Release")
        self.debug_path = os.path.join(save_path, "Debug")
        self.interpreter_path = os.path.join(self.module_path, "Python")
        if ignore_dirs is None:
            self.ignore_dirs = list()

        self.icon_path = icon

        # 创建基本环境目录
        if os.path.exists(self.save_path):
            if os.path.exists(self.module_path):
                Logging.warning(f"{os.path.abspath(self.module_path)}已存在，已清空该目录")
                self.ignore_dirs.append(self.module_path)
                shutil.rmtree(self.module_path)
            if os.path.exists(self.debug_path):
                Logging.warning(f"{os.path.abspath(self.debug_path)}已存在，已清空该目录")
                self.ignore_dirs.append(self.debug_path)
                shutil.rmtree(self.debug_path)
        else:
            os.makedirs(self.save_path, exist_ok=True)

        # 配置操作参数
        set_default_deploy_mode(deploy_mode)
        set_default_pip_lib(self.interpreter_path)
        self.with_debug = with_debug
        self.hidden_terminal = hidden_terminal

        # 新建配置信息
        self.configs = dict()
        self.configs["launcher_py_path"] = self.launcher_py_path
        self.configs["hidden_terminal"] = hidden_terminal
        self.configs["lazy_module"] = list()
        self.configs["sub_module"] = list()
        self.configs["local_uid"] = base64.b64encode((os.path.abspath(sys.executable) + "|" +
                                                      os.path.abspath(qpt.__file__) + "|" +
                                                      os.path.abspath(self.module_path)).encode('utf-8'))

        # 额外的成员变量
        self.resources_path = os.path.join(self.module_path, "resources")
        self.config_path = os.path.join(self.module_path, "configs")
        self.config_file_path = os.path.join(self.config_path, "configs.txt")
        self.lib_package_path = os.path.join(self.interpreter_path, "Lib/site-packages")

        # 设置全局下载的Python包默认解释器版本号 - 更换兼容性方案
        # set_default_package_for_python_version(interpreter_module.python_version)

        # 避免打包虚拟环境等
        # ToDo 后续用fnmatch来判断
        venv_dir = "-%NONE-FLAG%-"
        for root, dirs, files in os.walk(self.work_dir):
            if "pyvenv.cfg" in files:
                venv_dir = root
                self.ignore_dirs.append(root)
                Logging.warning(
                    f"检测到pyvenv.cfg，推测出{os.path.abspath(root)}为Python虚拟环境主目录，在打包时会忽略该目录")
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
        interpreter_version = AutoPythonEnv() if interpreter_version is None else BasePythonEnv(
            name="interpreter",
            version=interpreter_version)

        # 获取SubModule列表 - 此处均无ExtModule
        self.lazy_modules = [interpreter_version, QPTDependencyPackage()]

        self.sub_modules = sub_modules if sub_modules is not None else list()

        # 放入增强包
        # self.add_sub_module(CheckNotSetupPackage())
        self.add_sub_module(CheckCompileCompatibility())
        # 放入增强包
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
        # ToDo 此处可能需要发生改动，新版QPT没有依赖lazy module在runtime
        self.terminal = None

    def add_sub_module(self, sub_module: SubModule, lazy=False):
        """
        为Module添加子模块
        """
        module = sub_module.get_all_module()
        # 判断是否包含子模块，若包含则获取子模块的子模块
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
            Logging.info(module.name + f"执行优先级{module.level}" + f"\t{module.details}")
        Logging.info("----------程序执行使用了以下OP----------")
        for module in self.sub_modules:
            Logging.info(module.name + f"优先级{module.level}" + f"\t{module.details}")
        Logging.info("------------------------------------")

    def _solve_module(self, lazy=False):
        if lazy:
            modules = self.lazy_modules
            # lazy mode 不支持terminal
            terminal = None
        else:
            self.terminal = PTerminal()
            modules = self.sub_modules
            terminal = self.terminal.shell
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
        # 依靠优先级进行排序
        self.lazy_modules.sort(key=lambda m: m.level, reverse=True)
        self.sub_modules.sort(key=lambda m: m.level, reverse=True)
        self.print_details()

        # 解析子模块
        self._solve_module(lazy=True)
        self._solve_module()

        # 复制资源文件
        assert os.path.exists(self.work_dir), f"{os.path.abspath(self.work_dir)}不存在，请检查该路径是否正确"
        Logging.info("正在复制相关文件，可能会耗时较长")
        copytree(self.work_dir, self.resources_path, ignore_dirs=self.ignore_dirs)
        # 加入wrapper代码
        wrapper_code = """# Create by QPT https://github.com/GT-ZhangAcer/QPT
import os
if "ing" not in os.environ.get("QPT_MODE"):
    from qpt.run_wrapper import wrapper
    wrapper()
    from qpt.executor import RunExecutableModule
    RunExecutableModule("..").run()
"""
        with open(os.path.join(self.lib_package_path, "sitecustomize.py"), "w", encoding="utf-8") as _f:
            _f.write(wrapper_code)
        # QPT的dev模式
        if self.with_debug:
            Logging.debug("当前已开启QPT-dev模式，将会复制当前版本的QPT文件至相应目录")
            qpt_dir_path = os.path.split(qpt.__file__)[0]
            copytree(src=qpt_dir_path, dst=os.path.join(self.interpreter_path, "Lib/site-packages/qpt"))

        # 创建配置文件
        os.makedirs(self.config_path, exist_ok=True)
        with open(self.config_file_path, "w", encoding="utf-8") as config_file:
            config_file.write(str(self.configs))

        # 启动器相关
        launcher_entry_path = os.path.join(os.path.split(qpt.__file__)[0], "ext/launcher_entry")

        # 复制Debug所需文件
        Logging.info("正在复制相关文件，可能会耗时较长")
        debug_ext_dir = os.path.join(os.path.split(qpt.__file__)[0], "ext/launcher_debug")
        copytree(debug_ext_dir, dst=self.debug_path)
        copytree(self.module_path, dst=self.debug_path)
        shutil.copy(src=os.path.join(launcher_entry_path, "entry_debug.cmd"),
                    dst=os.path.join(self.debug_path, "configs/entry.cmd"))
        # 注册主程序文件路径
        with open(os.path.join(self.debug_path, "configs/entry.cmd"), "r", encoding="utf-8") as f:
            data = f.read().replace("QPT_PY_MAIN_FILE=NONE", "QPT_PY_MAIN_FILE=" + self.launcher_py_path[0])
        with open(os.path.join(self.debug_path, "configs/entry.cmd"), "w", encoding="utf-8") as f:
            f.write(data)

        # 生成Debug标识符
        unlock_file_path = os.path.join(self.debug_path, "configs/unlock.cache")
        with open(unlock_file_path, "w", encoding="utf-8") as unlock_file:
            unlock_file.write(str(datetime.datetime.now()))
        # 重命名兼容模式文件
        compatibility_mode_file = os.path.join(self.debug_path, "compatibility_mode.cmd")
        with open(os.path.join(self.debug_path, "compatibility_mode.cmd"), "r", encoding="utf-8") as f:
            data = f.read().replace("QPT_PY_MAIN_FILE=NONE", "QPT_PY_MAIN_FILE=" + self.launcher_py_path[0])
        with open(os.path.join(self.debug_path, "compatibility_mode.cmd"), "w", encoding="utf-8") as f:
            f.write(data)
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
            shutil.copy(src=os.path.join(debug_ext_dir, "Debug.exe"),
                        dst=os.path.join(self.module_path, "启动程序.exe"))
            shutil.copy(src=os.path.join(launcher_entry_path, "entry_run.cmd"),
                        dst=os.path.join(self.module_path, "configs/entry.cmd"))
        # 注册主程序文件路径
        with open(os.path.join(self.module_path, "configs/entry.cmd"), "r", encoding="utf-8") as f:
            data = f.read().replace("QPT_PY_MAIN_FILE=NONE", "QPT_PY_MAIN_FILE=" + self.launcher_py_path[0])
        with open(os.path.join(self.module_path, "configs/entry.cmd"), "w", encoding="utf-8") as f:
            f.write(data)

        copytree(launcher_ext_dir, dst=self.module_path, ignore_files=launcher_ignore_file)
        # 重命名兼容模式文件
        compatibility_mode_file = os.path.join(self.module_path, "compatibility_mode.cmd")
        with open(compatibility_mode_file, "r", encoding="utf-8") as f:
            data = f.read().replace("QPT_PY_MAIN_FILE=NONE", "QPT_PY_MAIN_FILE=" + self.launcher_py_path[0])
        with open(compatibility_mode_file, "w", encoding="utf-8") as f:
            f.write(data)
        if os.path.exists(compatibility_mode_file):
            os.rename(compatibility_mode_file,
                      os.path.join(self.module_path, "使用兼容模式运行.cmd"))
        # 重命名启动器文件
        launcher_file = os.path.join(self.module_path, "Main.exe")
        if os.path.exists(launcher_file):
            os.rename(launcher_file,
                      os.path.join(self.module_path, "启动程序.exe"))
        # 修改icon
        if self.icon_path:
            make_icon(self.icon_path,
                      pe_path=os.path.join(self.module_path, "启动程序.exe"),
                      img_save_path=os.path.join(self.config_path, "Logo.ico"))
            make_icon(self.icon_path,
                      pe_path=os.path.join(self.debug_path, "Debug.exe"),
                      img_save_path=os.path.join(self.debug_path, "configs", "Logo.ico"))

        # Logging Summary
        if Logging.final():
            Logging.warning("SUMMARY结束，发现上述异常情况，请确认后按任意键继续！")
            if not QPT_MEMORY.action_flag:
                Logging.flush()
                input()

        # ToDo 要对__pycache__和.chm文件进行清理

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

        if not QPT_MEMORY.action_flag:
            sys.stdout.flush()
            Logging.info("是否需要保留QPT在打包时产生的缓存文件？若不清空则可能会在下次使用QPT时复用缓存以提升打包速度")
            Logging.info("[保留(Y)/清空(N)]:_", line_feed=False)
            clear_key = input()
            sys.stdout.flush()
            if clear_key.lower() == "n":
                clean_qpt_cache()
                Logging.info("QPT缓存已全部清空")
            os.startfile(os.path.abspath(self.save_path))


class RunExecutableModule:
    def __init__(self, module_path: str = None):
        # 正常情况下module_path应为上一级目录，因为会先cd到resources再执行python，所以运行时的工作目录为module_path\resources
        if os.getenv("QPT_MODE") == "Run" or "Debug":
            os.environ["QPT_MODE"] = "Running" if QPT_MODE == "Run" else "Debugging"
        if module_path is None:
            module_path = os.path.abspath("./")
        self.base_dir = os.path.abspath(module_path)
        self.config_path = os.path.abspath(os.path.join(self.base_dir, "configs"))
        self.config_file_path = os.path.abspath(os.path.join(self.base_dir, "configs", "configs.txt"))
        self.work_dir = os.path.abspath(os.path.join(self.base_dir, "resources"))
        self.interpreter_path = os.path.abspath(os.path.join(self.base_dir, "Python"))

        # 初始化Log
        log_name = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-") + ".txt"
        if not os.path.exists(os.path.join(self.config_path, "logs")):
            log_name = "First-" + log_name
            os.mkdir(os.path.join(self.config_path, "logs"))
        if QPT_MODE == "Debugging":
            log_name = "#Debug#" + log_name
        set_logger_file(os.path.join(self.config_path, "logs", "QPT-" + log_name))
        sys.stdout = StdOutLoggerWrapper(os.path.join(self.config_path, "logs", "APP-" + log_name))

        # 软件信息
        Logging.info(
            f"QPT Runtime版本号为{qpt_v}，若无法使用该程序，可向程序发布者或GitHub: QPT-Family/QPT提交issue寻求帮助")

        # 强制本地PIP
        set_default_pip_lib(self.interpreter_path)

        # 检查路径是否非法
        check_path = __file__
        if os.path.realpath(tempfile.gettempdir()) in os.path.realpath(self.base_dir):
            warning_msg_box(text=f"{self.base_dir}\n"
                                 f"上述目录存在于系统的临时目录下，该情况可能会对程序运行造成影响\n"
                                 f"建议的解决方案如下：\n"
                                 f"1. 请勿在压缩软件中打开本程序，务必解压后再运行。\n"
                                 f"2. 请在物理硬盘上执行本程序。")
        if check_warning_char(check_path) or " " in check_path:
            warning_msg_box(text=f"{self.base_dir}\n"
                                 f"警告！当前路径↑中包含中文或空格等无法识别的字符，部分软件包将无法运行，强烈建议您修改相关的文件夹名，\n"
                                 f"---------------------------------------\n"
                                 f"不符合规范的路径如下：\n"
                                 f"C:/GT真菜/xxx/yyy\r\r！“真菜”为中文\n"
                                 f"C:/zzz/GT真 菜/yyy\r\r！“GT真 菜”中“真”字后带有空格\n"
                                 f"C:/zzz/GT真*&！的菜/yyy\r\r！“*&！”为特殊字符\n"
                                 f"---------------------------------------\n"
                                 f"符合规范的路径如下：\n"
                                 f"C:/hello/xxx/yyy\n"
                                 f"---------------------------------------\n"
                                 f"当然，您也可将Windows系统的默认编码模式更改为UTF-8，这可以更好兼容中文，但操作难度较高。\n"
                                 f"---------------------------------------\n"
                                 f"请修改相关文件名后重新运行，谢谢！",
                            force=False)

        try:
            with open(self.config_file_path, "r", encoding="utf-8") as config_file:
                # ToDo 此处会有注入漏洞
                self.configs = eval(config_file.read())
        except Exception as e:
            Logging.error("请检查杀毒软件、防火墙等限制策略，当前程序无法正常访问Config.gt文件，完整报错如下：\n" + str(e))

        # 获取GUI选项
        self.hidden_terminal = self.configs["hidden_terminal"]

        # 获取Module
        self.lazy_module = self.configs["lazy_module"]
        self.sub_module = self.configs["sub_module"]

        # 实例化终端
        self.auto_terminal = PTerminal()

    def _solve_module(self):
        modules = self.lazy_module + self.sub_module

        def render(arg=None):
            Logging.info("初次使用将会适应本地环境，可能需要几分钟时间，请耐心等待...")
            terminal = self.auto_terminal.shell
            tp = TProgressBar("初始化进度", max_len=len(modules) + 2)
            for sub_module_id, sub_name in enumerate(modules):
                tp.step(add_end_info=f"{sub_name}部署中...")
                if arg:
                    arg.step(text="正在适配" + sub_name)
                sub_module = SubModule(sub_name)
                sub_module.prepare(work_dir=self.work_dir,
                                   interpreter_path=self.interpreter_path,
                                   module_path=self.base_dir,
                                   terminal=terminal)
                sub_module.unpack()
            tp.step(add_end_info=f"初始化完毕")

        if self.hidden_terminal:
            get_func_bind_progressbar(bind_fuc=render, max_step=len(modules))
        else:
            render()

    def run(self):
        # 获取启动信息 - 避免在Release下进行Debug
        env_warning_flag = False
        local_uid = base64.b64decode(self.configs["local_uid"]).decode("utf-8")
        if all([os.path.exists(uid) for uid in local_uid.split("|")]):
            env_warning_flag = True
        lock_file_path = os.path.join(self.config_path, "unlock.cache")
        if os.path.exists(lock_file_path):
            env_warning_flag = False

        if env_warning_flag:
            msg = warning_msg_box("Warning", f"非常不建议在该环境下进行调试，原因如下： \n"
                                             f" 1. 继续执行将会加载“一次性部署模块”，部署后该模块会消失，消失后可能无法在其他电脑上使用。\n"
                                             f" 2. 该程序会解压缩当前环境，执行“启动程序.exe”后整个目录大小可能会增加1~5倍。（取决于压缩率）\n"
                                             f" 3. 若需要测试打包后程序是否可以正常运行，请在Debug目录下进行测试。\n"
                                             f" 4. 若特殊情况必须在Release目录下进行测试，请制作Release目录的备份，在他人需要时提供该备份\n"
                                             f"    文件或重新打包，以避免因执行“启动程序.exe”后丢失“一次性部署模块”，从而无法被他人使用。\n"
                                             f"---------------------------------------------------------------------------\n"
                                             f"当然，这个警告框并不会在其它电脑上弹出，仅会在本计算机运行时提示"
                                             f"请问是否还要在该环境下继续执行？")
            if not msg:
                Logging.info("程序已停止")
                exit(1)
        # prepare module - GUI组件需要在此之后才能进行
        self._solve_module()

        if Logging.final():
            msg = warning_msg_box(title="ERROR 发生异常 -GitHub: QPT-Family/QPT",
                                  text="检测到安装中出现问题，若您为未成功运行过本程序，请点击 取消 \n"
                                       "若您已经成功运行了本程序，可点击 确定 来隐藏该窗口")
            if msg:
                CheckRun.make_run_file(self.config_path)
        else:
            CheckRun.make_run_file(self.config_path)

        # os.chdir(self.work_dir)
        Logging.info("环境部署完毕！")
