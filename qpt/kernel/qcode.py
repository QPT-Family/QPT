# Author: Acer Zhang
# Datetime:2021/7/18
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import ast
import os

from qpt.kernel.qlog import TProgressBar
from qpt.kernel.qpackage import WhlDict, search_packages_dist_info, search_dep
from qpt.memory import PYTHON_IGNORE_DIRS, IGNORE_PACKAGES


def search_import_in_text(contents):
    """
    搜索对应文本中有那些符合的Import名
    :param contents: 文本
    :return: 模块名集合
    """
    import_module = set()
    tree = ast.parse(contents)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for sub_node in node.names:
                import_module.add(sub_node.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                import_module.add(node.module.split(".")[0])
    return import_module


def search_import_in_dir(path, lower=True):
    """
    在对应目录中搜索所有导入的Python模块
    :param path: 路径
    :param lower: 统一小写模块搜索结果
    :return: 模块名集合
    """
    import_modules = set()
    file_path_list = list()
    for root, dirs, files in os.walk(path):
        if not (os.path.basename(root) in PYTHON_IGNORE_DIRS or "site-packages" in root):
            for file in files:
                if os.path.splitext(file)[-1] == ".py":
                    file_path = os.path.join(root, file)
                    file_path_list.append(file_path)

    tpb = TProgressBar("正在搜索依赖", max_len=len(file_path_list))
    for file_path in file_path_list:
        with open(file_path, "r", encoding="utf-8") as f:
            import_module = search_import_in_text(f.read())
            if import_module:
                if lower:
                    import_module = set([ipm.lower() for ipm in import_module])
                import_modules = import_modules.union(import_module)
            tpb.step(add_end_info=f"对应文件:{file_path}")
    return import_modules


def intelligent_analysis(path, return_all_info=False):
    """
    分析对应目录下所使用的Python包情况
    :param path: 对应目录
    :param return_all_info: 是否返回所有信息，默认只返回包名与包版本字典，为True后返回包名与依赖名+版本号的字典以及被忽略的Top依赖包
    """
    # ToDo 以后加个参数，兼容非当前环境下的智能分析
    install_dict, top_dict = search_packages_dist_info()
    dep = search_dep()
    package_import = search_import_in_dir(path)

    # 整合包名，避免~的情况
    for inp_name, package_name in top_dict.copy().items():
        if "~" == inp_name[:1]:
            for package in package_import:
                if inp_name[1:] in package:
                    top_dict.pop(inp_name)
                    top_dict[package] = package_name
                    break

    # 提取显式的依赖项
    sub_requires = WhlDict()
    for package in package_import:
        if package in top_dict and package not in IGNORE_PACKAGES:
            p_name = top_dict[package]
            if package in top_dict:
                p_v = dep[p_name] if isinstance(dep[p_name], str) else install_dict[p_name]
            else:
                p_v = install_dict[p_name]
            sub_requires[p_name] = p_v

    # 向顶部依赖进化
    top_deps = WhlDict(dict([(d_k, d_v) for d_k, d_v in dep.items() if d_v]))
    requires = WhlDict(dict(sub_requires))
    # 遍历所有带有子依赖的节点
    for top_d in top_deps.keys():
        # 遍历所有已经得到的显式依赖
        for sub_require in sub_requires.keys():
            # 如果显式依赖存在子依赖中
            if sub_require in top_deps[top_d] and sub_require in requires:
                # 删除该显式依赖
                requires.pop(sub_require)
                # 上升为主依赖并得到当前安装的版本号
                requires[top_d] = install_dict[top_d]

    if return_all_info:
        # 搜索非子依赖且pip中有安装的Python包
        ignore_packages = dict()
        top_dep_flatten = set(IGNORE_PACKAGES)
        for top_dep in top_deps.values():
            top_dep_flatten = top_dep_flatten.union(top_dep.keys())
        for install_package in install_dict.keys():
            # 若安装的Python包不在搜索结果中，且不属于子依赖，则加入返回列表
            if install_package not in requires and install_package not in top_dep_flatten:
                ignore_packages[install_package] = install_dict[install_package]

        return requires, dep, ignore_packages
    else:
        return requires


if __name__ == '__main__':
    _test_workdir = "./../../unit_test/sandbox_qt_paddle"
    print("------测试场景的依赖搜索情况------")
    for _i in search_import_in_dir(_test_workdir, True):
        print("TEST_C", _i)

    print("------最终结果------")
    print(intelligent_analysis(_test_workdir))
