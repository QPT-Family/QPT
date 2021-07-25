# Author: Acer Zhang
# Datetime:2021/7/18 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
from qpt.sys_info import SITE_PACKAGE_PATH

# tree = ast.parse(contents)
# for node in ast.walk(tree):
#     if isinstance(node, ast.Import):
#         for subnode in node.names:
#             raw_imports.add(subnode.name)
#     elif isinstance(node, ast.ImportFrom):
#         raw_imports.add(node.module)

PACKAGE_FLAG = ".dist-info"


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


if __name__ == '__main__':
    print(search_packages_dist_info())
