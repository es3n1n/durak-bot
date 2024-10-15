from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.util.logger import logger


@durak.event(command='game_ready')
def on_game_ready(_: dict):
    durak.game.ready()
    logger.info('We are ready')
    ctx.cards.reload_cards()
