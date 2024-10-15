import sys
from loguru import logger
from pprint import pformat

from durak_bot.core.config import config


def pprint(function=logger.info, *args, **kwargs) -> None:
    for line in pformat(*args, **kwargs).split('\n'):
        function(line)


def debug_pprint(*args, **kwargs) -> None:
    pprint(logger.debug, *args, **kwargs)


def info_pprint(*args, **kwargs) -> None:
    pprint(logger.info, *args, **kwargs)


def _filter_min_level(record: dict) -> bool:
    current_level_name: str = 'DEBUG' if config.is_dev_env else 'INFO'
    current_level: int = logger.level(current_level_name).no
    return record['level'].no >= current_level


def _filter_stderr(record: dict) -> bool:
    return _filter_min_level(record)


def _filter_stdout(record: dict) -> bool:
    record_no: int = record['level'].no
    error_no: int = logger.level('ERROR').no
    return _filter_min_level(record) and record_no != error_no


def init() -> None:
    fmt = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <red>|</red> '
        '<level>{level: <8}</level> <red>|</red> '
        '<cyan>{name}</cyan><red>:</red><cyan>{function}</cyan><red>:</red><cyan>{line}</cyan> <red>-</red> '
        '<level>{message}</level>'
    )

    logger.remove()
    logger.configure(
        handlers=[
            {
                'sink': sys.stderr,
                'level': 'ERROR',
                'format': fmt,
                'filter': _filter_stderr,
            },
            {'sink': sys.stdout, 'format': fmt, 'filter': _filter_stdout},
        ]
    )


init()
