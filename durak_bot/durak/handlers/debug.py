import json

from durak_bot.durak.instance import durak
from durak_bot.util.logger import logger


@durak.event(command='all')
def log_event(data: dict):
    logger.debug(json.dumps(data))
