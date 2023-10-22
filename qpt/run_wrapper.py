# Author: Acer Zhang
# Datetime: 2022/5/9 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# run wrapper负责包装主程序在运行前预热动作

__COMPATIBLE_INPUT_START_FLAG = "---QPT COMPATIBLE_INPUT_START_FLAG---"  # 37
__COMPATIBLE_INPUT_END_FLAG = "---QPT COMPATIBLE_INPUT_END_FLAG---"  # 35
__COMPATIBLE_INPUT_SPLIT_FLAG = "---QPT COMPATIBLE_INPUT_SPLIT_FLAG---"  # 37


def __compatible_input():
    """
    对QPT中使用多进程启动Python程序做input的适配
    因input在subprocess.Popen中并不会显式向用户提供输入
    Warning: 该方案需要添加行缓冲环境变量
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
        # 向主进程抛出input信号
        print(__COMPATIBLE_INPUT_START_FLAG +
              _path +
              __COMPATIBLE_INPUT_SPLIT_FLAG +
              str(__prompt) +
              __COMPATIBLE_INPUT_END_FLAG)

        # 检测用户是否写入文件
        while True:
            if os.path.exists(_path):
                break
            else:
                time.sleep(0.2)

        # 读取用户的输入情况
        with open(_path, "rb") as f:
            raw = f.read().decode("utf-8")
        # 读完就扔
        os.remove(_path)
        return raw

    # 替换子进程默认的input()为我们特制的input()
    builtins.__dict__["input"] = _wrapper


def wrapper():
    # 替换默认输入流
    __compatible_input()


if __name__ == '__main__':
    wrapper()
    input("测试")
