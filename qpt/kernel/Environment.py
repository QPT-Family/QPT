# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# 全局变量 - 还没确定是否要做全局变量管理器，若不做则提供预设文件供开发者使用，若做则需要增加大量的判断
configs = {"MODE": None}


@property
def mode():
    return configs["MODE"]


def set_configs(item: dict):
    configs.update(item)
