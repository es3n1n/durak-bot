from typing import Callable

from durak_bot import ctx
from durak_bot.const.smiles import SMILE_FLOWERS
from durak_bot.durak.instance import durak
from durak_bot.types.card import Card
from durak_bot.types.player_state import EPlayerState
from durak_bot.util.logger import logger


def get_add_strategy() -> list[Card]:
    # Get all the possible cards to add, excluding the trump cards.
    table_values = ctx.cards.table_values
    possible_cards = [
        c
        for c in ctx.cards.our_hand
        if c.value in table_values and (not ctx.cards.should_ignore_trumps or c.type != ctx.cards.trump_card_type)
    ]

    # Reversed so that we'll first add cards with higher value
    return list(reversed(possible_cards))


def try_add_cards() -> bool:
    possible_cards_to_add = get_add_strategy()
    logger.debug(
        f'Adding cards {possible_cards_to_add = }, '
        f'Our hand: {ctx.cards.our_hand}, '
        f'Trump: {ctx.cards.trump_card} ({ctx.cards.trump_card_type}), '
        f'Unbeaten cards: {ctx.cards.unbeaten_cards_on_table}, '
        f'Beaten cards: {ctx.cards.beaten_cards_on_table}, '
    )
    if not possible_cards_to_add:
        return False

    # fixme: We can add only one card for some reason, others will be rejected
    card_to_add = possible_cards_to_add[0]
    ctx.cards.push_unbeaten_card_on_table(card_to_add)
    ctx.cards.remove_from_our_hand(card_to_add)

    # When someone takes cards we should feed them cards instead of making turns
    attack_type: str = 'turn'
    attack_fn: Callable[[str], None] = durak.game.turn
    if ctx.players.is_someone(EPlayerState.TAKES):
        attack_type = 'feed'
        attack_fn = durak.game.feed

    attack_fn(str(card_to_add))
    logger.info(f'Added card {card_to_add} via {attack_type}')
    durak.game.send_smile(smile_id=SMILE_FLOWERS)
    return True
