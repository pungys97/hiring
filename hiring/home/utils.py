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


def verify_signature(signed_signature: str):
    signer = Signer()
    try:
        original_timestamp, seed = signer.unsign(signed_signature).split(";")
    except BadSignature:
        original_timestamp, seed = None, None
    return original_timestamp, seed
