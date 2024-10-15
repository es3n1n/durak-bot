from durak_bot.algorithm.actions.attack import select_card_to_use_in_attack
from durak_bot.types.card import Card
from durak_bot import ctx


def test_attack_lowest_non_trump():
    ctx.reset()
    ctx.cards.trump_card = Card.parse('♥')
    ctx.cards.our_hand = [
        Card.parse('♦10'),
        Card.parse('♦A'),
        Card.parse('♣7'),
    ]
    assert select_card_to_use_in_attack() == Card.parse('♣7')


def test_attack_lowest_trump_when_only_trumps():
    ctx.reset()
    ctx.cards.trump_card = Card.parse('♥')
    ctx.cards.our_hand = [
        Card.parse('♥6'),
        Card.parse('♥10'),
        Card.parse('♥A'),
    ]
    assert select_card_to_use_in_attack() == Card.parse('♥6')


def test_attack_lowest_non_trump_with_mixed_hand():
    ctx.reset()
    ctx.cards.trump_card = Card.parse('♠')
    ctx.cards.our_hand = [
        Card.parse('♥K'),
        Card.parse('♦8'),
        Card.parse('♠J'),
        Card.parse('♣9'),
    ]
    assert select_card_to_use_in_attack() == Card.parse('♦8')


def test_attack_with_single_card():
    ctx.reset()
    ctx.cards.trump_card = Card.parse('♥')
    ctx.cards.our_hand = [Card.parse('♠A')]
    assert select_card_to_use_in_attack() == Card.parse('♠A')


def test_attack_lowest_strength_among_equal_suits():
    ctx.reset()
    ctx.cards.trump_card = Card.parse('♥')
    ctx.cards.our_hand = [
        Card.parse('♦7'),
        Card.parse('♦9'),
        Card.parse('♣8'),
        Card.parse('♣Q'),
    ]
    assert select_card_to_use_in_attack() == Card.parse('♦7')
