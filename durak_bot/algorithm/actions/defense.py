from time import sleep

from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.types.card import Card
from durak_bot.util.cards import card_with_lowest_strength, can_beat
from durak_bot.util.logger import logger


def find_best_card_to_beat(card: Card, hand: list[Card]) -> Card | None:
    available_cards = [c for c in hand if can_beat(to_beat=card, beat_by=c)]
    if not available_cards:
        return None
    return card_with_lowest_strength(available_cards)


def get_defense_strategy() -> dict[Card, Card] | None:
    to_beat: dict[Card, Card] = dict()
    # Our hands are already sorted by strength at this point, no need for re-sorting
    hand = ctx.cards.our_hand.copy()

    for card_on_table in ctx.cards.unbeaten_cards_on_table:
        beating_with = find_best_card_to_beat(card_on_table, hand)
        if not beating_with:
            logger.warning(
                f'Unable to beat {card_on_table}, '
                f'Our hand: {ctx.cards.our_hand}, '
                f'Trump: {ctx.cards.trump_card} ({ctx.cards.trump_card_type}), '
                f'Unbeaten cards: {ctx.cards.unbeaten_cards_on_table}'
            )
            return None

        to_beat[card_on_table] = beating_with
        hand.remove(beating_with)
        logger.debug(f'Will beat card {card_on_table} with {beating_with}')

    return to_beat


def should_take_cards() -> bool:
    # # Beaten + unbeaten, excluding the cards that were used to beat them
    # cards_on_table = [
    #     *ctx.cards.beaten_cards_on_table,
    #     *ctx.cards.unbeaten_cards_on_table,
    # ]
    #
    # # If we are using too many trump cards to defend, might be better to take
    # trumps = sum(1 for card in cards_on_table if card.type == ctx.cards.trump_card_type)
    # trumps_threshold = len(ctx.cards.unbeaten_cards_on_table) // 2
    # if trumps > trumps_threshold:
    #     logger.warning(
    #         f"Taking cards because of trumps({trumps}) > threshold({trumps_threshold})"
    #     )
    #     return True

    # We might want to take trump cards if we're near the end of the game
    # deck_threshold = 5
    # if ctx.cards.deck_left < deck_threshold and any(
    #     c.type == ctx.cards.trump_card_type for c in cards_on_table
    # ):
    #     logger.warning(
    #         f"Taking cards because of deck({ctx.cards.deck_left}) < {deck_threshold} && has_trump"
    #     )
    #     return True

    return False


def try_transfer() -> bool:
    # Transfers/forwards are not enabled
    if not ctx.lobby.is_passing_enabled:
        return False

    # Can not transfer if there's already beaten cards
    if ctx.cards.beaten_cards_on_table:
        return False

    # Our opponent doesnt have enough cards
    if ctx.cards.number_of_cards[ctx.lobby.next_player_id] < len(ctx.cards.unbeaten_cards_on_table) + 1:
        return False

    # Try to find something we can use to forward, ignore trumps if needed
    table_values = ctx.cards.table_values
    possible_cards = [
        c
        for c in ctx.cards.our_hand
        if (not ctx.cards.should_ignore_trumps or c.type != ctx.cards.trump_card_type) and c.value in table_values
    ]

    # Can't forward
    if not possible_cards:
        return False

    # Forward
    forwarding_with = possible_cards[0]
    logger.info(f'Forwarding/transferring with the card {str(forwarding_with)}')

    # fixme: Kostil
    ctx.cards.forwarding = True

    # Server will reject our card unless we sleep for a few seconds, :clueless:
    sleep(0.75)
    durak.game.forward_card(str(forwarding_with))
    ctx.cards.remove_from_our_hand(card=forwarding_with)
    ctx.cards.push_unbeaten_card_on_table(card=forwarding_with)
    return True


def try_defend() -> bool:
    # 1. Take cards if needed
    if should_take_cards():
        return False

    # 2. Forward cards if we can
    if try_transfer():
        return True

    # 3. Beat
    to_beat = get_defense_strategy()
    if to_beat is None:
        return False

    for k, v in to_beat.items():
        logger.info(f'Sending batch to beat {k} with {v}')
        durak.game.beat(card_to_beat=str(k), card=str(v))
        ctx.cards.card_beaten(card=k, beaten_by=v)
        ctx.cards.remove_from_our_hand(card=v)

    return True
