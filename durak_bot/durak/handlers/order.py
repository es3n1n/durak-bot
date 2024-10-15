from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.util.logger import debug_pprint, logger


@durak.event(command='order')
def on_order(data: dict):
    for player_id in data['ids']:
        ctx.cards.inc_cards_count(player_id)

    logger.debug('Updated cards count:')
    debug_pprint(ctx.cards.number_of_cards)
