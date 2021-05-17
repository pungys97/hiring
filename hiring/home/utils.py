import logging

from django.conf import settings as s
from django.core.signing import Signer, BadSignature


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


def verify_timestamp(signed_timestamp: str):
    signer = Signer()
    try:
        original_timestamp = signer.unsign(signed_timestamp)
    except BadSignature:
        original_timestamp = None
    return original_timestamp
