import logging
import sys


# from fortmatic.config import LOGGER_NAME


LOGGER_NAME = 'magic'

LOG_LEVEl = 'debug'

logger = logging.getLogger(LOGGER_NAME)


def _magic_log_level():
    if LOG_LEVEl == 'debug':
        return LOG_LEVEl


def format_log(message, **kwargs):
    return dict(
        {'message': message},
        log_level=LOG_LEVEl,
        serverice=LOGGER_NAME,
        **kwargs,
    )


def log_debug(message, **kwargs):
    log_line = format_log(message, **kwargs)

    if _magic_log_level() == 'debug':
        print(log_line, file=sys.stderr)

    logger.debug(log_line)


def log_info(message, **kwargs):
    log_line = format_log(message, **kwargs)

    if _magic_log_level() == 'debug':
        print(log_line, file=sys.stderr)

    logger.info(log_line)
