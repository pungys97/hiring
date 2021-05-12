import logging

from django.conf import settings as s


def get_logger(name):
    logging.basicConfig(
        filename=s.LOG_FILE,
        level=s.LOGGING_LEVEL,
        format=s.LOGGING_FORMAT,
    )
    logger = logging.getLogger(name)
    if s.LOG_TO_CONSOLE:
        handler = logging.StreamHandler()
        handler.setLevel(s.LOGGING_LEVEL)
        logger.addHandler(handler)

    return logger