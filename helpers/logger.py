import logging


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s | %(name)s [%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    s_h = logging.StreamHandler()
    s_h.setLevel(logging.INFO)
    s_h.setFormatter(CustomFormatter())
    logger.addHandler(s_h)

    logname = r'logs\bot.log'
    f_h = logging.FileHandler(logname, )
    f_h.setLevel(logging.DEBUG)
    f_h.setFormatter(logging.Formatter("%(asctime)s | %(name)s [%(levelname)s] %(message)s"))
    f_h.encoding = "utf-8"
    logger.addHandler(f_h)

    return logger