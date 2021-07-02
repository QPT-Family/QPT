import logging

__all__ = ["Logging", "clean_stout"]

formatter = logging.Formatter('%(asctime)s %(levelname)s:   \t%(message)s')
logger = logging.getLogger("qpt_logger")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


def clean_stout(name_list: list):
    headers = logging.root.handlers
    for header in list(headers):
        if header.name in name_list:
            logging.root.removeHandler(header)


class Logging:

    @staticmethod
    def info(msg: str):
        return logger.info("\033[34m" + msg + "\033[0m")

    @staticmethod
    def debug(msg: str):
        logger.debug("\033[35m" + msg + "\033[0m")

    @staticmethod
    def warning(msg: str):
        logger.warning("\033[33m" + msg + "\033[0m")

    @staticmethod
    def error(msg: str):
        logger.error("\033[41m" + msg + "\033[0m")


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
        block = f"\033[31m{block_str}\033[0m"

        print("\r" + self.msg +
              f"\t{self.count}/{self.max_len} {add_start_info}\t{block}\t{rate * 100:.2f}%\t" +
              add_end_info,
              end="",
              flush=True)
