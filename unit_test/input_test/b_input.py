# Author: Acer Zhang
# Datetime: 2022/5/11 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

__COMPATIBLE_INPUT_START_FLAG = "---QPT COMPATIBLE_INPUT_START_FLAG---"  # 37
__COMPATIBLE_INPUT_END_FLAG = "---QPT COMPATIBLE_INPUT_END_FLAG---"  # 35
__COMPATIBLE_INPUT_SPLIT_FLAG = "---QPT COMPATIBLE_INPUT_SPLIT_FLAG---"  # 37


def __compatible_input():
    """
    对QPT中使用多进程启动Python程序做input的适配
    因input在subprocess.Popen中并不会显式向用户提供输入
    :return:
    """
    import builtins
    import uuid
    import os
    import time
    from tempfile import gettempdir

    _path = os.path.join(gettempdir(), "Python_PIPE")
    os.makedirs(_path, exist_ok=True)
    _path = os.path.join(_path, str(uuid.uuid4()) + ".txt")

    def _wrapper(__prompt):
        print(__COMPATIBLE_INPUT_START_FLAG +
              _path +
              __COMPATIBLE_INPUT_SPLIT_FLAG +
              str(__prompt) +
              __COMPATIBLE_INPUT_END_FLAG)

        while True:
            if os.path.exists(_path):
                break
            else:
                time.sleep(0.2)
        with open(_path, "rb") as f:
            raw = f.read().decode("utf-8")
        return raw

    builtins.__dict__["input"] = _wrapper


def wrapper():
    __compatible_input()


wrapper()
print("开始")
x = input("请输入")
print(x)
