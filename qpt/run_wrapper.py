# Author: Acer Zhang
# Datetime: 2022/5/9 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# run wrapper负责包装主程序在运行前预热动作

__COMPATIBLE_INPUT_START_FLAG = "---QPT COMPATIBLE_INPUT_START_FLAG---"  # 37
__COMPATIBLE_INPUT_END_FLAG = "---QPT COMPATIBLE_INPUT_END_FLAG---"  # 35


def __compatible_input():
    """
    对QPT中使用多进程启动Python程序做input的适配
    因input在subprocess.Popen中并不会显式向用户提供输入
    :return:
    """
    import builtins

    ori_input = builtins.__dict__["input"]

    def _wrapper(__prompt):
        print(__COMPATIBLE_INPUT_START_FLAG + str(__prompt) + __COMPATIBLE_INPUT_END_FLAG)
        raw = ori_input()
        return raw

    # ToDo https: // blog.csdn.net / qq_43395215 / article / details / 106409275
    builtins.__dict__["input"] = _wrapper


def wrapper():
    __compatible_input()


if __name__ == '__main__':
    wrapper()