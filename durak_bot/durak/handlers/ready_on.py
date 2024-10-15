from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.util.logger import logger


@durak.event(command='ready_on')
def on_ready_on(_: dict) -> None:
    logger.info('Ready on, resetting cards')
    ctx.cards.reload_cards()
