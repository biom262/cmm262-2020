from datetime import datetime
from logging import FileHandler, Formatter, StreamHandler, getLogger


def initialize_logger(name):

    logger = getLogger(name)

    logger.setLevel(10)

    fh = FileHandler("/tmp/{}.{:%Y:%m:%d:%H:%M:%S}.log".format(name, datetime.now()))

    fh.setFormatter(Formatter("%(asctime)s|%(levelname)s: %(message)s\n", "%H%M%S"))

    logger.addHandler(fh)

    sh = StreamHandler()

    sh.setFormatter(Formatter("%(levelname)s: %(message)s\n"))

    logger.addHandler(sh)

    logger.info("Initialized {} logger.".format(name))

    return logger
