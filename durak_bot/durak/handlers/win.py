from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.const.smiles import SMILE_SUNGLASSES, SMILE_WTF
from durak_bot.util.logger import logger


@durak.event(command='win')
def on_end_turn(data: dict):
    winner_id: int = data['id']
    value: int = data['value']
    if value < 0:
        return

    ctx.lobby.winners_count += 1
    if winner_id != ctx.lobby.position:
        return

    logger.info(f'Winner #{ctx.lobby.winners_count} is {winner_id}')

    if ctx.lobby.winners_count == 1:
        ctx.stats.inc_wins()
        durak.game.send_smile(SMILE_SUNGLASSES)
        return

    ctx.stats.inc_ties()
    durak.game.send_smile(SMILE_WTF)
