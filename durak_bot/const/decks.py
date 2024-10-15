from durak_bot.types.card import Card
from durak_bot.const.cards import CARD_TYPES, CARD_RANGES

CARDS_FOR_DECK: dict[int, set[Card]] = {
    deck_size: {Card.parse(f'{card_type}{value}') for value in values for card_type in CARD_TYPES}
    for deck_size, values in CARD_RANGES.items()
}

for k, v in CARDS_FOR_DECK.items():
    assert len(v) == k
