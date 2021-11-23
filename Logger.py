import logging
from colorlog import ColoredFormatter


def myLogger(name) -> logging:
    LOG_LEVEL = logging.DEBUG

    LOGFORMAT = "%(log_color)s%(name)s%(reset)s : %(log_color)s[%(levelname)-s]%(reset)s | %(log_color)s%(message)s%(reset)s"

    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOGFORMAT, log_colors={
        'DEBUG':    'white',
        'INFO':     'cyan',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red',
    })
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    log = logging.getLogger(name)
    log.setLevel(LOG_LEVEL)
    log.addHandler(stream)

    """log.debug("A quirky message only developers care about")
    log.info("Curious users might want to know this")
    log.warning("Something is wrong and any user should be informed")
    log.error("Serious stuff, this is red for a reason")
    log.critical("OH NO everything is on fire")"""

    return log
