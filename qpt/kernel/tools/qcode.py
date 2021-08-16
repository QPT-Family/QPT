# Author: Acer Zhang
# Datetime:2021/7/18
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import ast
from pip._internal.utils.misc import get_installed_distributions

from qpt.sys_info import SITE_PACKAGE_PATH, get_ignore_dirs
from qpt.kernel.tools.qlog import Logging, TProgressBar

PACKAGE_FLAG = ".dist-info"


# 字典尽量用get，都是泪
# 尽量统一lower依赖

class PythonPackages:
    def __init__(self):
        pass

    @staticmethod
    def search_packages_dist_info(site_package_path=None):
        # 获取依赖列表
        dep_pkg_dict = PythonPackages.search_dep()

        # 获取当前环境下安装的文件列表
        if site_package_path is None:
            site_package_path = SITE_PACKAGE_PATH
        packages_dir_list = os.listdir(site_package_path)
        packages_dist = dict()
        tops_dist = dict()
        for package_dist in packages_dir_list:
            if PACKAGE_FLAG == package_dist[-len(PACKAGE_FLAG):]:
                package = package_dist[:-len(PACKAGE_FLAG)]
                name = package[:package.rfind("-")].lower()
                # 对name修复可能的下划线情况
                if name.replace("_", "-") in dep_pkg_dict:
                    name = name.replace("_", "-")

                version = package[package.rfind("-") + 1:]
                top_file_path = os.path.join(site_package_path, package_dist, "top_level.txt")
                if os.path.exists(top_file_path):
                    with open(top_file_path, "r", encoding="utf-8") as top_file:
                        tops = top_file.readlines()

                    for top in tops:
                        # 避免路径导入
                        if "\\" in top:
                            top = top.split("\\")[-1]
                        # 兼容Linux
                        if "/" in top:
                            top = top.split("/")[-1]
                        tops_dist[top.strip("\n").lower()] = name
                packages_dist[name] = version
        return packages_dist, tops_dist, dep_pkg_dict

    @staticmethod
    def search_dep():
        pkgs = get_installed_distributions()
        pkg_dict = dict()
        for pkg in pkgs:
            dep = pkg.requires()
            if dep:
                dep_dict = dict()
                for d in dep:
                    d_name, _, d_version = d.hashCmp[:3]
                    d_name = d_name.lower()
                    f_version = str(d_version)
                    if f_version:
                        dep_dict[d_name] = f_version
                    else:
                        dep_dict[d_name] = None
                pkg_dict[pkg.project_name.lower()] = dep_dict
            else:
                pkg_dict[pkg.project_name.lower()] = None
        return pkg_dict

    @staticmethod
    def search_import_in_text(contents):
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

    @staticmethod
    def search_import_in_dir(path, lower=True):
        import_modules = set()
        file_path_list = list()
        for root, dirs, files in os.walk(path):
            if not (os.path.basename(root) in get_ignore_dirs() or "site-packages" in root):
                for file in files:
                    if os.path.splitext(file)[-1] == ".py":
                        file_path = os.path.join(root, file)
                        file_path_list.append(file_path)

        tpb = TProgressBar("正在搜索依赖", max_len=len(file_path_list))
        for file_path in file_path_list:
            with open(file_path, "r", encoding="utf-8") as f:
                import_module = PythonPackages.search_import_in_text(f.read())
                if import_module:
                    if lower:
                        import_module = set([ipm.lower() for ipm in import_module])
                    import_modules = import_modules.union(import_module)
                tpb.step(add_end_info=f"对应文件:{file_path}")
        return import_modules

    @staticmethod
    def intelligent_analysis(path, return_dep=False):
        # ToDo 以后加个参数，兼容非当前环境下的智能分析
        install_dict, package_dict, dep = PythonPackages.search_packages_dist_info()
        package_import = PythonPackages.search_import_in_dir(path)

        # 提取显式的依赖项
        sub_requires = dict()
        for package in package_import:
            if package in package_dict and package not in ["virtualenv", "pip", "setuptools"]:
                p_name = package_dict[package]
                if package in ["virtualenv", "pip", "setuptools", "cpython"]:
                    continue
                if package in package_dict:
                    p_v = dep[p_name] if isinstance(dep[p_name], str) else install_dict[p_name]
                else:
                    p_v = install_dict[p_name]
                sub_requires[p_name] = p_v

        # 向顶部依赖进化
        top_deps = dict([(d_k, d_v) for d_k, d_v in dep.items() if d_v])
        requires = dict(sub_requires)
        # 遍历所有带有子依赖的节点
        for top_d in top_deps:
            # 遍历所有已经得到的显式依赖
            for sub_require in sub_requires:
                # 如果显式依赖存在子依赖中
                if sub_require in top_deps.get(top_d) and sub_require in requires:
                    # 删除该显式依赖
                    requires.pop(sub_require)
                    # 上升为主依赖并得到当前安装的版本号
                    requires[top_d] = install_dict.get(top_d)
        if return_dep:
            return requires
        else:
            return requires, dep


if __name__ == '__main__':
    _test_dir = "./../../../unit_test/sandbox_qt_paddle"
    print("当前环境下包安装情况以及对应表", PythonPackages.search_packages_dist_info())
    print("当前环境下包依赖情况", PythonPackages.search_dep())
    print("测试场景的依赖搜索情况", PythonPackages.search_import_in_dir(_test_dir))
    print("最终搜索到的依赖情况：", PythonPackages.intelligent_analysis(_test_dir))
