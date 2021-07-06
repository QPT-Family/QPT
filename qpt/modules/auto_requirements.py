# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os

from qpt.kernel.tools.interpreter import PIP
from qpt.kernel.tools.log_op import Logging
from qpt.kernel.tools.os_op import get_qpt_tmp_path
from qpt.modules.package import _RequirementsPackage, DEFAULT_DEPLOY_MODE
from qpt.modules.paddle_family import PaddlePaddlePackage


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
        :param module_list: Module callback
        :param deploy_mode: 部署模式
        """
        if os.path.isfile(path):
            requirements = PIP.analyze_requirements_file(path)
        else:
            Logging.info(f"[Auto]正在分析{os.path.abspath(path)}下的依赖情况...")
            requirements = PIP.analyze_dependence(path, return_path=False)

        # module_name_list = [m.name for m in module_list]
        # 对特殊包进行过滤和特殊化
        pre_add_module = list()
        for requirement in dict(requirements):
            if requirement in SPECIAL_MODULE:
                special_module, parameter = SPECIAL_MODULE[requirement]
                parameter["version"] = requirements[requirement]
                parameter["deploy_mode"] = deploy_mode
                module = special_module(**parameter)
                # # 如果开发者没有定义这个Module，那么则添加Module - ToDo 等自定义算子出了再考虑，可以在执行时候考虑
                # if module.name not in module_name_list:
                #     module_list.append(module)
                pre_add_module.append(module)
                requirements.pop(requirement)

        # 保存依赖至
        requirements_path = os.path.join(get_qpt_tmp_path(), "requirements_dev.txt")
        PIP.save_requirements_file(requirements, requirements_path)

        # 执行常规的安装
        super().__init__(requirements_file_path=requirements_path,
                         deploy_mode=deploy_mode)
        for pam in pre_add_module:
            self.add_ext_module(pam)


SPECIAL_MODULE = {"paddlepaddle": (PaddlePaddlePackage, {"version": None,
                                                         "include_cuda": False,
                                                         "deploy_mode": DEFAULT_DEPLOY_MODE}),
                  "paddlepaddle-gpu": (PaddlePaddlePackage, {"version": None,
                                                             "include_cuda": True,
                                                             "deploy_mode": DEFAULT_DEPLOY_MODE})}
