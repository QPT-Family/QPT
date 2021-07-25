import logging
import os

__all__ = ["Logging", "change_none_color", "clean_stout", "TProgressBar", "set_logger_file"]

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger("qpt_logger")
st_handler = logging.StreamHandler()
st_handler.setFormatter(formatter)

DEBUG_VAR = os.getenv("QPT_MODE")
if DEBUG_VAR == "Run":
    LEVEL = logging.INFO
elif DEBUG_VAR == "Debug":
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.DEBUG

logger.setLevel(LEVEL)
st_handler.setLevel(LEVEL)

# 设置标准输出流
logger.addHandler(st_handler)


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


WARNING_SUMMARY = list()
ERROR_SUMMARY = list()


class BaseLogging:
    @staticmethod
    def final():
        """
        用于打印当前收到的警告和报错情况
        :return: 是否包含报错或警告
        """
        Logging.info("-" * 10 + "WARNING SUMMARY" + "-" * 10)
        for msg in WARNING_SUMMARY:
            Logging.info(msg)
        Logging.info("-" * 10 + "ERROR SUMMARY  " + "-" * 10)
        for msg in ERROR_SUMMARY:
            Logging.info(msg)
        Logging.info("-" * 10 + f"生成状态WARNING:{len(WARNING_SUMMARY)} ERROR:{len(ERROR_SUMMARY)}" + "-" * 10)
        if WARNING_SUMMARY or ERROR_SUMMARY:
            return True
        else:
            return False

    @staticmethod
    def flush():
        st_handler.flush()


class LoggingColor(BaseLogging):
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


class LoggingNoneColor(BaseLogging):
    @staticmethod
    def info(msg: str):
        logger.info(msg)

    @staticmethod
    def debug(msg: str):
        logger.debug(msg)

    @staticmethod
    def warning(msg: str):
        logger.warning(msg)
        WARNING_SUMMARY.append(f"{len(WARNING_SUMMARY)}|{msg}\n")

    @staticmethod
    def error(msg: str):
        logger.error(msg)
        ERROR_SUMMARY.append(f"{len(WARNING_SUMMARY)}|{msg}\n")


def change_none_color():
    global Logging
    Logging = LoggingNoneColor


COLOR_VAR = os.getenv("QPT_COLOR")
if COLOR_VAR == "True" or COLOR_VAR is None:
    Logging = LoggingColor
else:
    change_none_color()


class TProgressBar:
    def __init__(self,
                 msg: str = "",
                 max_len: int = 100,
                 with_logging=True):
        self.count = 0
        self.msg = msg
        self.max_len = max_len
        self.block = 20
        self.with_logging = True
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
        if self.count == self.max_len:
            print("\n", end="", flush=True)
