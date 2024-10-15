from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.types.card import Card
from durak_bot.util.cards import sort_cards_by_strength
from durak_bot.util.logger import logger


@durak.event(command='hand')
def on_hand(data: dict):
    ctx.cards.our_hand = sort_cards_by_strength(
        [Card.parse(x) for x in data.get('cards', [])],
    )
    ctx.cards.ensure_hand_cards_are_seen()
    logger.info(f"Our hand: {', '.join(map(str, ctx.cards.our_hand))}")
