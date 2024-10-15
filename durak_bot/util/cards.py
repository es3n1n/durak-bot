from durak_bot.const.cards import CARD_OVERALL_RANGE
from durak_bot.types.card import Card
from durak_bot import ctx


def get_card_strength(card: Card) -> int:
    is_trump = 1 if card.type == ctx.cards.trump_card_type else 0
    return is_trump * 100 + CARD_OVERALL_RANGE.index(card.value)


def can_beat(beat_by: Card, to_beat: Card) -> bool:
    if beat_by.type == to_beat.type:
        return CARD_OVERALL_RANGE.index(beat_by.value) > CARD_OVERALL_RANGE.index(to_beat.value)

    # If the beaten_by card is trump, it will always beat any other non-trump card
    return beat_by.type == ctx.cards.trump_card_type and to_beat.type != ctx.cards.trump_card_type


def sort_cards_by_strength(hand: list[Card]) -> list[Card]:
    return list(sorted(hand, key=get_card_strength))


def card_with_lowest_strength(cards: list[Card]) -> Card:
    return min(cards, key=get_card_strength)


def card_with_highest_strength(cards: list[Card]) -> Card:
    return max(cards, key=get_card_strength)
