# Author: Acer Zhang
# Datetime: 2022/5/7 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import copy
from pip._internal.metadata.pkg_resources import Distribution

# 对pip低版本做兼容
try:
    from pip._internal.utils.misc import get_installed_distributions
except ImportError:
    from pip._internal.utils.misc import cast


    def get_installed_distributions(
            local_only=True,
            include_editables=True,
            editables_only=False,
            user_only=False,
            paths=None):
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

from qpt.memory import QPT_MEMORY

PACKAGE_FLAG = ".dist-info"


class WhlDict:
    def __init__(self, iterable: dict = None):
        self.dict = dict([(k.replace("-", "_").lower(), v) for k, v in iterable.items()]) if iterable else dict()

    @staticmethod
    def norm_name(name):
        return name.replace("-", "_").lower()

    def pop(self, key):
        self.dict.pop(self.norm_name(key))

    def values(self):
        return self.dict.values()

    def keys(self):
        return self.dict.keys()

    def items(self):
        return self.dict.items()

    def copy(self):
        return copy.copy(self)

    def __setitem__(self, key, value):
        self.dict[self.norm_name(key)] = value

    def __getitem__(self, key):
        return self.dict[self.norm_name(key)]

    def __contains__(self, key):
        return True if self.norm_name(key) in self.dict else False

    def __repr__(self):
        return str(self.dict)


def search_dep():
    """
    获取当前已安装的包以及其依赖
    :return: 所有包与其依赖的包版本字典所构成的字典{package1: {sub_package: version}, ...}
    """
    pkgs = get_installed_distributions()
    pkg_dict = WhlDict()
    for pkg in pkgs:
        dep = pkg.requires()
        if dep:
            dep_dict = WhlDict()
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


def search_packages_dist_info(site_package_path=None):
    """
    获取对应site_package_path下所有Python包的版本号以及TopName
    :param site_package_path:检索的路径
    :return:所有包名与包版本字典、所有包import名与包名字典、所有包与其依赖的包版本字典所构成的字典
    """
    # 获取依赖列表
    dep_pkg_dict = search_dep()

    # 获取当前环境下安装的文件列表
    if site_package_path is None:
        site_package_path = QPT_MEMORY.site_packages_path
    packages_dir_list = os.listdir(site_package_path)
    packages_dist = WhlDict()
    tops_dist = WhlDict()
    for package_dist in packages_dir_list:
        if package_dist.endswith(PACKAGE_FLAG):
            metadata = Distribution.from_directory(os.path.join(site_package_path, package_dist))
            name = metadata.raw_name
            version = metadata.version.base_version

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
                    tops_dist[top.strip("\n")] = name

            packages_dist[name] = version

    return packages_dist, tops_dist, dep_pkg_dict


def get_package_all_file(package, site_package_path=None):
    """
    获取对应包所包含的所有文件
    :param package: 包名
    :param site_package_path: 环境文件夹
    :return: 文件列表
    """
    if site_package_path is None:
        site_package_path = QPT_MEMORY.site_packages_path
    packages_dir_list = os.listdir(site_package_path)

    record_path = None
    for package_dist in packages_dir_list:
        # 判断是否是目标文件夹
        if package in package_dist and PACKAGE_FLAG.endswith(PACKAGE_FLAG):
            record_path = os.path.join(site_package_path, package_dist, "RECORD")
            if not os.path.exists(record_path):
                record_path = None

    assert record_path is not None, f"{package} RECORD信息读取失败，" \
                                    f"请在requirement.txt中取消对该依赖的#$QPT_FLAG$ copy特殊操作指令"
    resource_list = list()
    with open(record_path, "r", encoding="utf-8") as records:
        data = records.readlines()
        for record in data:
            relative_path = record.strip("\n").split(",")[0]
            resource_list.append(relative_path)
    return resource_list


if __name__ == '__main__':
    print("------当前环境下包安装情况以及对应表------")
    for _i in search_packages_dist_info():
        print("TEST_A", _i)


