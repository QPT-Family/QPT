# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os

from qpt.kernel.qlog import Logging
from qpt.kernel.qos import get_qpt_tmp_path, ArgManager, download
from qpt.kernel.qinterpreter import display_flag, DISPLAY_IGNORE, DISPLAY_COPY, DISPLAY_FORCE, DISPLAY_NET_INSTALL, \
    DISPLAY_LOCAL_INSTALL
from qpt.modules.package import _RequirementsPackage, DEFAULT_DEPLOY_MODE, CustomPackage
from qpt.modules.paddle_family import PaddlePaddlePackage, PaddleOCRPackage
from qpt.memory import QPT_MEMORY


class AutoRequirementsPackage(_RequirementsPackage):
    """
    注意，这并不是个普通的Module
    """

    def __init__(self,
                 path,
                 deploy_mode=DEFAULT_DEPLOY_MODE):
        """
        自动获取Requirements
        :param path: 待扫描的文件夹路径或requirements文件路径，若提供了requirements文件路径则不会自动分析依赖情况
        :param deploy_mode: 部署模式
        """
        if not os.path.exists(path):
            Logging.info(f"当前路径{os.path.abspath(path)}中不存在Requirements文件，"
                         f"请优先检查路径是否提供正确，必要时使用绝对路径")

        if os.path.isfile(path):
            Logging.info(f"正在读取{os.path.abspath(path)}下的依赖情况...")
            requirements = QPT_MEMORY.pip_tool.analyze_requirements_file(path)
        else:
            Logging.info(f"[Auto]正在分析{os.path.abspath(path)}下的依赖情况...")
            requirements = QPT_MEMORY.pip_tool.analyze_dependence(path,
                                                                  return_path=False,
                                                                  action_mode=QPT_MEMORY.action_flag)

        # module_name_list = [m.name for m in module_list]
        pre_add_module = list()
        for requirement in dict(requirements):
            requirement, version, display = requirement, requirements["version"], requirements["display"]
            # 对特殊包进行过滤和特殊化
            if requirement in SPECIAL_MODULE:
                special_module, parameter = SPECIAL_MODULE[requirement]
                parameter["version"] = version
                parameter["deploy_mode"] = deploy_mode if not display else display
                module = special_module(**parameter)
                pre_add_module.append(module)
                requirements.pop(requirement)
            # 使用依赖文件中指定的方式封装
            else:
                display_mode = display_flag.get_flag(display)
                if display_mode == DISPLAY_IGNORE:
                    requirements.pop(requirement)
                elif display_mode == DISPLAY_FORCE:
                    pre_add_module.append(CustomPackage(package=requirement,
                                                        version=version,
                                                        deploy_mode=deploy_mode,
                                                        opts=ArgManager(["--no-deps --force-reinstall"])))
                    requirements.pop(requirement)
                elif DISPLAY_NET_INSTALL in display_mode:
                    _, whl = download(
                        url=f"{display_mode[len(DISPLAY_NET_INSTALL) + 1:]}",
                        file_name="")
                    # ToDo 看看要不要走find link，不清楚file_name能不能拿到

            # ToDo 剩下几个模式还没适配 DISPLAY_COPY,  , DISPLAY_LOCAL_INSTALL

        # 保存依赖至
        requirements_path = os.path.join(get_qpt_tmp_path(), "requirements_dev.txt")
        QPT_MEMORY.pip_tool.save_requirements_file(requirements, requirements_path)

        # 执行常规的安装
        super().__init__(requirements_file_path=requirements_path,
                         deploy_mode=deploy_mode)
        for pam in pre_add_module:
            self.add_ext_module(pam)


# 自动推理依赖时需要特殊处理的Module配置列表 格式{包名: (Module, Module参数字典)}
# version、deploy_mode 为必填字段
# ToDo 小心 DEFAULT_DEPLOY_MODE 不在mem中可能会有问题
SPECIAL_MODULE = {"paddlepaddle": (PaddlePaddlePackage, {"version": None,
                                                         "include_cuda": False,
                                                         "deploy_mode": DEFAULT_DEPLOY_MODE}),
                  "paddlepaddle-gpu": (PaddlePaddlePackage, {"version": None,
                                                             "include_cuda": True,
                                                             "deploy_mode": DEFAULT_DEPLOY_MODE}),
                  "paddleocr": (PaddleOCRPackage, {"version": None,
                                                   "deploy_mode": DEFAULT_DEPLOY_MODE})}
