# Author: Acer Zhang
# Datetime:2021/7/18 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import ast
from pip._internal.utils.misc import get_installed_distributions

from qpt.sys_info import SITE_PACKAGE_PATH
from qpt.sys_info import get_ignore_dirs

PACKAGE_FLAG = ".dist-info"


# 字典尽量用get，都是泪

class PythonPackages:
    def __init__(self):
        pass

    @staticmethod
    def search_packages_dist_info(site_package_path=None):
        if site_package_path is None:
            site_package_path = SITE_PACKAGE_PATH
        packages_dir_list = os.listdir(site_package_path)
        packages_dist = dict()
        tops_dist = dict()
        for package_dist in packages_dir_list:
            if PACKAGE_FLAG == package_dist[-len(PACKAGE_FLAG):]:
                package = package_dist[:-len(PACKAGE_FLAG)]
                name = package[:package.rfind("-")]
                version = package[package.rfind("-") + 1:]
                top_file_path = os.path.join(site_package_path, package_dist, "top_level.txt")
                if os.path.exists(top_file_path):
                    with open(top_file_path, "r", encoding="utf-8") as top_file:
                        tops = top_file.readlines()
                    for top in tops:
                        if "\\" in top:
                            top = top.split("\\")[-1]
                        tops_dist[top.strip("\n")] = name
                packages_dist[name] = version
        return packages_dist, tops_dist
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
                    f_version = str(d_version)
                    if f_version:
                        dep_dict[d_name] = f_version
                    else:
                        dep_dict[d_name] = None
                pkg_dict[pkg.project_name] = dep_dict
            else:
                pkg_dict[pkg.project_name] = None
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
    def search_import_in_dir(path):
        import_modules = set()
        for root, dirs, files in os.walk(path):
            if not (os.path.basename(root) in get_ignore_dirs() or "site-packages" in root):
                for file in files:
                    if os.path.splitext(file)[-1] == ".py":
                        file_path = os.path.join(root, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            import_module = PythonPackages.search_import_in_text(f.read())
                            if import_module:
                                import_modules = import_modules.union(import_module)
        return import_modules

    @staticmethod
    def intelligent_analysis(path):
        # ToDo 以后加个参数，兼容非当前环境下的智能分析
        install_dict, package_dict = PythonPackages.search_packages_dist_info()
        dep = PythonPackages.search_dep()
        package_import = PythonPackages.search_import_in_dir(path)

        # 提取显式的依赖项
        sub_requires = dict()
        for package in package_import:
            if package in package_dict:
                p_name = package_dict[package]
                # ToDo 此处的get仅检验到3.7~3.9版本，更新的Python版本需要检查
                if package in dep and dep.get(p_name):
                    p_v = dep[p_name]
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
                if sub_require in top_deps.get(top_d):
                    # 删除该显式依赖
                    requires.pop(sub_require)
                    # 上升为主依赖并得到当前安装的版本号
                    requires[top_d] = install_dict.get(top_d)
        pass


if __name__ == '__main__':
    print("当前环境下包安装情况以及对应表", PythonPackages.search_packages_dist_info())
    print("当前环境下包依赖情况", PythonPackages.search_dep())
    print("测试场景的依赖搜索情况", PythonPackages.search_import_in_dir("./../../../unit_test/sandbox_qt_paddle"))
    PythonPackages.intelligent_analysis("./../../../unit_test/sandbox_qt_paddle")
