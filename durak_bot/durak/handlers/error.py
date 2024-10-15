from durak_bot.util.logger import logger
from durak_bot.durak.instance import durak


@durak.error()
def on_error(e: Exception):
    logger.opt(exception=e).warning('Unhandled exception')
