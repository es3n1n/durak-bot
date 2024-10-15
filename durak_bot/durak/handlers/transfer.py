from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.types.card import Card
from durak_bot.util.logger import logger


@durak.event(command='s')
def on_s(data: dict):
    player_id: int = data['id']
    card: Card = Card.parse(data['c'])

    ctx.cards.push_unbeaten_card_on_table(card, player_index=player_id)
    ctx.cards.number_of_cards[player_id] -= 1
    logger.info(f"Card has been transferred, cards on the table: {', '.join(map(str, ctx.cards.cards_on_table))}")
