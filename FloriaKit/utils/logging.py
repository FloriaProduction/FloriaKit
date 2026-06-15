import typing as t
import logging
from logging import Logger

DEFAULT_TERMINAL_FORMAT: str = '[%(levelname)s]  %(asctime)s  %(name)s:\t%(message)s'

DEFAULT_FILE_FORMAT: str = '[%(levelname)s]  %(asctime)s  %(name)s:\t%(message)s'
DEFAULT_FILE_MODE: t.Literal['r', 'a'] = 'a'


logger_level_ann = t.Literal[
    'debug',
    'info',
    'warning',
    'error',
    'critical',
]

_logger_level_map: dict[logger_level_ann, int] = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


def create(
    name: str | object,
    level: int | logger_level_ann,
    terminal_format: logging.Formatter | str = DEFAULT_TERMINAL_FORMAT,
) -> logging.Logger:
    level_int = _logger_level_map[level] if isinstance(level, str) else level

    logger = logging.Logger(
        name if isinstance(name, str) else name.__class__.__name__, level_int
    )

    terminal_handler = logging.StreamHandler()
    terminal_handler.setLevel(level_int)
    terminal_handler.setFormatter(
        terminal_format
        if isinstance(terminal_format, logging.Formatter)
        else logging.Formatter(terminal_format)
    )

    logger.addHandler(terminal_handler)

    return logger


__all__ = [
    'DEFAULT_TERMINAL_FORMAT',
    #
    'create',
    'Logger',
]
