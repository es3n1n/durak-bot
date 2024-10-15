from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.util.logger import logger


@durak.event(command='game')
def on_game(data: dict):
    ctx.reset()
    ctx.lobby.players_count = data['players']
    ctx.lobby.position = data['position']
    ctx.lobby.deck_size = data['deck']

    ctx.lobby.bet = data['bet']

    ctx.lobby.is_passing_enabled = data['sw']
    ctx.lobby.is_tricks_enabled = data['ch']
    ctx.lobby.is_draw_enabled = data['dr']
    ctx.lobby.is_fast = data['fast']
    logger.info(f'Updated the lobby info to {ctx.lobby}')
