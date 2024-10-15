from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.types.card import Card
from durak_bot.util.logger import logger


@durak.event(command='rct')
def on_card_withdrawal(data: dict):
    player_num: int = data['p']
    card: Card = Card.parse(data['c'])

    ctx.cards.inc_cards_count(player_num)
    ctx.cards.remove_card_from_table(card)
    ctx.cards.push_known_card(card, player_index=player_num)
    logger.info(f'Player {player_num} withdrew the card {card}')
