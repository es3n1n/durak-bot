from durak_bot import ctx
from durak_bot.types.card import Card
from durak_bot.util.cards import sort_cards_by_strength, can_beat


def test_card_comparing():
    assert can_beat(Card.parse('♣5'), Card.parse('♣2'))
    assert not can_beat(Card.parse('♣5'), Card.parse('♥2'))

    ctx.cards.trump_card = Card.parse('♣')
    assert can_beat(Card.parse('♣5'), Card.parse('♥2'))


def test_card_sorting():
    cards = [
        Card.parse('♣5'),
        Card.parse('♣2'),
        Card.parse('♦2'),
        Card.parse('♣A'),
        Card.parse('♥J'),
    ]

    ctx.cards.trump_card = Card.parse('♦')
    sorted_cards = sort_cards_by_strength(cards)

    assert len(cards) == len(sorted_cards)
    assert sorted_cards[0] == Card.parse('♣2')
    assert sorted_cards[1] == Card.parse('♣5')
    assert sorted_cards[2] == Card.parse('♥J')
    assert sorted_cards[3] == Card.parse('♣A')
    assert sorted_cards[4] == Card.parse('♦2')
