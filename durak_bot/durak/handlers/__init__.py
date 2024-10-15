from pathlib import Path
from importlib import import_module

from durak_bot.util.logger import logger


def init_handlers() -> int:
    count = 0

    for item in Path(__file__).parent.iterdir():
        if item.stem in ('__item__',):
            continue

        logger.debug(f'Loading handlers from {item.stem}')
        import_module(f'durak_bot.durak.handlers.{item.stem}')
        count += 1

    return count


# todo - game_start
