# Author: Acer Zhang
# Datetime: 2021/5/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import psutil
import pynvml


class SubCMD:
    """
    在Python中调用Windows终端
    """

    def __init__(self):
        self.sub_cmd = subprocess.Popen("cmd.exe",
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        stdin=subprocess.PIPE,
                                        shell=True)

    def shell(self, shell: str, to_print=True):
        # 命令中添加执行状态标识符
        self.sub_cmd.stdin.write((shell + "&&echo GACT:DONE!||echo GACT:ERROR!\r\n").encode("gbk"))
        self.sub_cmd.stdin.flush()
        if to_print:
            self.shell_print2method(print)

    def shell_print2method(self, act):
        """
        获取输出信息流
        :param act: 外部输出函数
        Example:
        > xxx.yyy("abc")
        abc

        > get_shell_stdout(act = xxx.yyy)
        stdout1
        stdout2
        stdout3
        ...
        """
        while True:
            line = self.sub_cmd.stdout.readline()
            if not line:
                break
            if line == b'GACT:DONE!\r\n':
                if self.debug:
                    act("成功执行该命令!")
            elif line == b'GACT:ERROR!\r\n':
                if self.debug:
                    act("命令执行失败!")
            result = line.decode('gbk').strip("b'").strip("\n")
            act(result)

    def get_out(self):
        return self.sub_cmd.stdout.read()

    def get_stdout(self):
        return self.sub_cmd.stdout.readline()

    def exit(self):
        self.sub_cmd.terminate()


def format2gb(dig):
    """
    将获取到的单位格式化为GB
    """
    dig = (dig // ((1024 ** 3) / 100)) / 100
    return dig


class SysInfo:
    # 初始化GPU信息
    gpu_info = pynvml.nvmlInit()
    # 定义GPU等级
    GTX_GPU_LEVEL = {"1050": 0, "1060": 1, "1070": 2, "1080": 3,
                     "1650": 0, "1660": 1,
                     "2060": 2, "2070": 3, "2080": 4,
                     "3060": 3, "3070": 3, "3080": 4, "3090": 5,
                     "Titan": 3}

    @staticmethod
    def req_memory(to_print=False):
        mem = psutil.virtual_memory()
        # 兼用旧版环境的保留小数点计算方法
        free = format2gb(mem.free)
        used = format2gb(mem.used)
        if to_print:
            Logging.info(f"当前内存已使用{used}GB, 空闲{free}GB")
        return free

    @staticmethod
    def req_gpu_count():
        return pynvml.nvmlDeviceGetCount()

    @staticmethod
    def req_all_gpu_info():
        device_count = pynvml.nvmlDeviceGetCount()
        info = list()
        for device_idx in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(device_idx)
            gpu_name = pynvml.nvmlDeviceGetName(handle)
            info.append(str(gpu_name)[2:-1])
        return info

    @staticmethod
    def req_gpu_level(idx: int = 0):
        """
        获取显卡等级 0~2 2最优
        :param idx: 第idx块显卡
        """
        handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        mem = format2gb(mem.free)
        Logging.info("GPU: " + str(gpu_name)[2:-1])
        Logging.info(f"GPU空闲显存: {mem}GB")
        level = int(mem)
        # ！待完善此处可以细分等级
        if level < 3:
            # Logging.warning("当前计算机可用于深度学习的默认显卡GPU显存极低，将不足以完成中型及以上任务")
            return 0
        if level < 8:
            # Logging.warning("当前计算机的默认显卡GPU显存过低")
            return 1
        return 2
