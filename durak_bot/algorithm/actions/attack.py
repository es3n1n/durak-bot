from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.types.card import Card
from durak_bot.util.cards import card_with_lowest_strength
from durak_bot.util.logger import logger


def select_card_to_use_in_attack() -> Card:
    # 1. Prefer non trump cards to attack and always select the one with lowest strength
    # 2. If we are out of non-trump cards, select any trump card with lowest strength
    # Since we are sorting by the strength value, for both of these we could just pick card with lowest strength
    return card_with_lowest_strength(ctx.cards.our_hand)


def try_attack() -> bool:
    card = select_card_to_use_in_attack()

    logger.info(f'Attacking with {str(card)}')
    durak.game.turn(str(card))
    ctx.cards.push_unbeaten_card_on_table(card)
    ctx.cards.remove_from_our_hand(card)
    return True
