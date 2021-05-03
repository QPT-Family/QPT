import logging

__all__ = ["Logging"]
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:   \t%(message)s')


class Logging:

    @staticmethod
    def info(msg: str):
        return logging.info("\033[34m" + msg + "\033[0m")

    @staticmethod
    def debug(msg: str):
        logging.debug("\033[35m" + msg + "\033[0m")

    @staticmethod
    def warning(msg: str):
        logging.warning("\033[33m" + msg + "\033[0m")

    @staticmethod
    def error(msg: str):
        logging.error("\033[41m" + msg + "\033[0m")
