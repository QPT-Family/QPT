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
st_handler.terminator = ""

# 设置标准输出流
logger.addHandler(st_handler)


def set_logger_file(file_path):
    f_handler = logging.FileHandler(file_path, "w", encoding="utf-8")
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)
    f_handler.terminator = ""
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
    def final(clear=True):
        """
        用于打印当前收到的警告和报错情况
        :return: 是否包含报错或警告
        """
        Logging.info("-" * 10 + "WARNING SUMMARY")
        for msg in WARNING_SUMMARY:
            Logging.info(msg)
        Logging.info("-" * 10 + "ERROR SUMMARY  ")
        for msg in ERROR_SUMMARY:
            Logging.info(msg)
        Logging.info("-" * 10 + f"生成状态WARNING:{len(WARNING_SUMMARY)} ERROR:{len(ERROR_SUMMARY)}")
        flag = ERROR_SUMMARY.copy()
        if clear:
            WARNING_SUMMARY.clear()
            ERROR_SUMMARY.clear()
        if len(flag) > 0:
            return True
        else:
            return False

    @staticmethod
    def flush():
        st_handler.flush()


class LoggingColor(BaseLogging):
    @staticmethod
    def info(msg: str, line_feed=True):
        msg = "\033[34m" + msg + "\033[0m"
        if line_feed:
            msg += "\n"
        logger.info(msg)

    @staticmethod
    def debug(msg: str, line_feed=True):
        msg = "\033[35m" + msg + "\033[0m"
        if line_feed:
            msg += "\n"
        logger.debug(msg)

    @staticmethod
    def warning(msg: str, line_feed=True):
        msg = "\033[33m" + msg + "\033[0m"
        WARNING_SUMMARY.append(f"{len(WARNING_SUMMARY)}|{msg}")
        if line_feed:
            msg += "\n"
        logger.warning(msg)

    @staticmethod
    def error(msg: str, line_feed=True):
        msg = "\033[41m" + msg + "\033[0m"
        ERROR_SUMMARY.append(f"{len(WARNING_SUMMARY)}|{msg}")
        if line_feed:
            msg += "\n"
        logger.error(msg)


class LoggingNoneColor(BaseLogging):
    @staticmethod
    def info(msg: str, line_feed=True):
        if line_feed:
            msg += "\n"
        logger.info(msg)

    @staticmethod
    def debug(msg: str, line_feed=True):
        if line_feed:
            msg += "\n"
        logger.debug(msg)

    @staticmethod
    def warning(msg: str, line_feed=True):
        if line_feed:
            msg += "\n"
        logger.warning(msg)
        WARNING_SUMMARY.append(f"{len(WARNING_SUMMARY)}|{msg}\n")

    @staticmethod
    def error(msg: str, line_feed=True):
        if line_feed:
            msg += "\n"
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
                 max_len: int = 100):
        self.count = 0
        self.msg = msg
        self.max_len = max_len - 1
        self.block = 20
        self.with_logging = True
        Logging.info("", line_feed=False)
        Logging.flush()

    def step(self, add_start_info="", add_end_info=""):
        self.count += 1
        if self.max_len == 0:
            block_str = "|" + "".join(['█'] * int(self.block)).ljust(self.block, " ") + "|"
            Logging.info("\r" +
                         self.msg +
                         f"\r1/1 {add_start_info} {block_str} {100:.2f}% " +
                         add_end_info,
                         line_feed=False)
        else:
            rate = self.count / self.max_len

            block_str = "|" + "".join(['█'] * int(rate * self.block)).ljust(self.block, " ") + "|"
            block = f"{block_str}"
            Logging.info("\r" +
                         self.msg +
                         f"\t{self.count}/{self.max_len} {add_start_info} {block} {rate * 100:.2f}% " +
                         add_end_info,
                         line_feed=False)
        Logging.flush()
        if self.count == self.max_len:
            Logging.info("", line_feed=True)
            Logging.flush()
