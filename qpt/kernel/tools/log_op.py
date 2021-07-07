import logging
import os

__all__ = ["Logging", "clean_stout", "TProgressBar", "set_logger_file"]

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger("qpt_logger")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

DEBUG_VAR = os.getenv("QPT_MODE")
if DEBUG_VAR == "Run":
    LEVEL = logging.INFO
elif DEBUG_VAR == "Debug":
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.DEBUG

logger.setLevel(LEVEL)
handler.setLevel(LEVEL)

# 设置标准输出流
logger.addHandler(handler)


def set_logger_file(file_path):
    f_handler = logging.FileHandler(file_path, "w", encoding="utf-8")
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)
    logger.addHandler(f_handler)


def clean_stout(name_list: list):
    headers = logging.root.handlers
    for header in list(headers):
        if header.name in name_list:
            logging.root.removeHandler(header)


class LoggingColor:
    @staticmethod
    def info(msg: str):
        logger.info("\033[34m" + msg + "\033[0m")

    @staticmethod
    def debug(msg: str):
        logger.debug("\033[35m" + msg + "\033[0m")

    @staticmethod
    def warning(msg: str):
        logger.warning("\033[33m" + msg + "\033[0m")

    @staticmethod
    def error(msg: str):
        logger.error("\033[41m" + msg + "\033[0m")


class LoggingNoneColor:
    @staticmethod
    def info(msg: str):
        logger.info(msg)

    @staticmethod
    def debug(msg: str):
        logger.debug(msg)

    @staticmethod
    def warning(msg: str):
        logger.warning(msg)

    @staticmethod
    def error(msg: str):
        logger.error(msg)


COLOR_VAR = os.getenv("QPT_COLOR")
if COLOR_VAR == "True" or COLOR_VAR is None:
    Logging = LoggingColor
else:
    Logging = LoggingNoneColor


class TProgressBar:
    def __init__(self,
                 msg: str = "",
                 max_len: int = 100):
        self.count = 0
        self.msg = msg
        self.max_len = max_len
        self.block = 20
        print("", flush=True)

    def step(self, add_start_info="", add_end_info=""):
        self.count += 1
        rate = self.count / self.max_len

        block_str = "".join(['■'] * int(rate * self.block)).ljust(self.block, "□")
        block = f"{block_str}"

        print("\r" + self.msg +
              f"{self.count}/{self.max_len} {add_start_info} {block} {rate * 100:.2f}% " +
              add_end_info,
              end="",
              flush=True)
