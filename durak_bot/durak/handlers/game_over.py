from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.const.smiles import SMILE_SAD


@durak.event(command='game_over')
def on_game_ready(data: dict):
    # fixme: we should reset this somewhere else
    ctx.lobby.winners_count = 0

    if ctx.lobby.position not in data['players']:
        return

    ctx.stats.inc_loses()
    durak.game.send_smile(SMILE_SAD)
