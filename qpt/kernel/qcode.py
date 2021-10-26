# Author: Acer Zhang
# Datetime:2021/7/18
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import ast
from typing import Optional, List, Container

# 对pip低版本做兼容
try:
    from pip._internal.utils.misc import Distribution, cast
    def get_installed_distributions(
            local_only=True,  # type: bool
            include_editables=True,  # type: bool
            editables_only=False,  # type: bool
            user_only=False,  # type: bool
            paths=None,  # type: Optional[List[str]]
    ):
        # type: (...) -> List[Distribution]
        """Return a list of installed Distribution objects.
        Left for compatibility until direct pkg_resources uses are refactored out.
        """
        from pip._internal.metadata import get_default_environment, get_environment
        from pip._internal.metadata.pkg_resources import Distribution as _Dist

        if paths is None:
            env = get_default_environment()
        else:
            env = get_environment(paths)
        dists = env.iter_installed_distributions(
            local_only=local_only,
            skip={"python", "wsgiref", "argparse"},
            include_editables=include_editables,
            editables_only=editables_only,
            user_only=user_only,
        )
        return [cast(_Dist, dist)._dist for dist in dists]
except ImportError:
    from pip._internal.utils.misc import get_installed_distributions

from qpt.memory import QPT_MEMORY, PYTHON_IGNORE_DIRS, IGNORE_PACKAGES
from qpt.kernel.qlog import TProgressBar

PACKAGE_FLAG = ".dist-info"


# 字典尽量用get，都是泪
# 尽量统一lower依赖a


class PythonPackages:
    def __init__(self):
        pass

    @staticmethod
    def search_packages_dist_info(site_package_path=None):
        """
        获取对应site_package_path下所有Python包的版本号以及TopName
        :param site_package_path:检索的路径
        :return:所有包名与包版本字典、所有包import名与包名字典、所有包与其依赖的包版本字典所构成的字典
        """
        # 获取依赖列表
        dep_pkg_dict = PythonPackages.search_dep()

        # 获取当前环境下安装的文件列表
        if site_package_path is None:
            site_package_path = QPT_MEMORY.site_packages_path
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
                # 修复~的情况
                if "~" == name[:1]:
                    metadata = os.path.join(site_package_path, package_dist, "METADATA")
                    if os.path.exists(metadata):
                        with open(metadata, "r", encoding="utf-8") as metadata:
                            for metadata_line in metadata.readlines():
                                if "Name: " == metadata_line[:6]:
                                    name = metadata_line.strip("Name: ").strip("\n")
                                    break

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
        """
        获取当前已安装的包以及其依赖
        :return: 所有包与其依赖的包版本字典所构成的字典
        """
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

    @staticmethod
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
                import_module = PythonPackages.search_import_in_text(f.read())
                if import_module:
                    if lower:
                        import_module = set([ipm.lower() for ipm in import_module])
                    import_modules = import_modules.union(import_module)
                tpb.step(add_end_info=f"对应文件:{file_path}")
        return import_modules

    @staticmethod
    def intelligent_analysis(path, return_all_info=False):
        """
        分析对应目录下所使用的Python包情况
        :param path: 对应目录
        :param return_all_info: 是否返回所有信息，默认只返回包名与包版本字典，为True后返回包名与依赖名+版本号的字典以及被忽略的Top依赖包
        """
        # ToDo 以后加个参数，兼容非当前环境下的智能分析
        install_dict, top_dict, dep = PythonPackages.search_packages_dist_info()
        package_import = PythonPackages.search_import_in_dir(path)

        # 整合包名，避免~的情况
        for inp_name, package_name in top_dict.copy().items():
            if "~" == inp_name[:1]:
                for package in package_import:
                    if inp_name[1:] in package:
                        top_dict.pop(inp_name)
                        top_dict[package] = package_name
                        break
        for inp_name, package_name in top_dict.copy().items():
            if "~" == inp_name[:1]:
                for package in package_import:
                    if inp_name[1:] in package:
                        top_dict.pop(inp_name)
                        top_dict[package] = package_name
                        break

        # 提取显式的依赖项
        sub_requires = dict()
        for package in package_import:
            if package in top_dict and package not in IGNORE_PACKAGES:
                p_name = top_dict[package]
                if package in top_dict:
                    p_v = dep.get(p_name) if isinstance(dep.get(p_name), str) else install_dict.get(p_name)
                else:
                    p_v = install_dict.get(p_name)
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

        if return_all_info:
            # 搜索非子依赖且pip中有安装的Python包
            ignore_packages = dict()
            top_dep_flatten = set(IGNORE_PACKAGES)
            for top_dep in top_deps.values():
                top_dep_flatten = top_dep_flatten.union(top_dep)
            for install_package in install_dict:
                # 若安装的Python包不在搜索结果中，且不属于子依赖，则加入返回列表
                if install_package not in requires and install_package not in top_dep_flatten:
                    ignore_packages[install_package] = install_dict[install_package]

            return requires, dep, ignore_packages
        else:
            return requires


if __name__ == '__main__':
    _test_workdir = "./"
    print("------当前环境下包安装情况以及对应表------")
    for _i in PythonPackages.search_packages_dist_info():
        print("TEST_A", _i)
    print("------当前环境下包依赖情况------")
    for _i in PythonPackages.search_dep():
        print("TEST_B", _i)
    print("------测试场景的依赖搜索情况------")
    for _i in PythonPackages.search_import_in_dir(_test_workdir, True):
        print("TEST_C", _i)

    print("------最终结果------")
    for _i in PythonPackages.intelligent_analysis(_test_workdir):
        print(_i)
