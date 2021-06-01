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
