from durak_bot import ctx
from durak_bot.algorithm.actions.add_card import get_add_strategy
from durak_bot.types.card import Card


def test_get_add_strategy_basic():
    ctx.cards.our_hand = [
        Card.parse('♠6'),
        Card.parse('♥7'),
        Card.parse('♦8'),
        Card.parse('♣9'),
        Card.parse('♠10'),
        Card.parse('♥J'),
    ]
    ctx.cards.cards_on_table = [Card.parse('♦7'), Card.parse('♣8')]
    ctx.cards.trump_card = Card.parse('♠')

    result = get_add_strategy()
    assert len(result) == 2
    assert Card.parse('♥7') in result
    assert Card.parse('♦8') in result


def test_get_add_strategy_no_matches():
    ctx.cards.our_hand = [
        Card.parse('♠6'),
        Card.parse('♥7'),
        Card.parse('♦8'),
        Card.parse('♣9'),
        Card.parse('♠10'),
        Card.parse('♥J'),
    ]
    ctx.cards.cards_on_table = [Card.parse('♦Q'), Card.parse('♣K')]
    ctx.cards.trump_card = Card.parse('♠')

    result = get_add_strategy()
    assert len(result) == 0


def test_get_add_strategy_only_trump_matches():
    ctx.cards.our_hand = [
        Card.parse('♠6'),
        Card.parse('♥7'),
        Card.parse('♦8'),
        Card.parse('♣9'),
        Card.parse('♠10'),
        Card.parse('♥J'),
    ]
    ctx.cards.cards_on_table = [Card.parse('♦6'), Card.parse('♣10')]
    ctx.cards.trump_card = Card.parse('♠')

    result = get_add_strategy()
    assert len(result) == 0


def test_get_add_strategy_multiple_matches():
    ctx.cards.our_hand = [
        Card.parse('♠6'),
        Card.parse('♥7'),
        Card.parse('♦7'),
        Card.parse('♣7'),
        Card.parse('♠10'),
        Card.parse('♥J'),
    ]
    ctx.cards.cards_on_table = [Card.parse('♦7'), Card.parse('♠7')]
    ctx.cards.trump_card = Card.parse('♠')

    result = get_add_strategy()
    assert len(result) == 3
    assert Card.parse('♥7') in result
    assert Card.parse('♦7') in result
    assert Card.parse('♣7') in result


def test_get_add_strategy_empty_hand():
    ctx.cards.our_hand = []
    ctx.cards.cards_on_table = [Card.parse('♦7'), Card.parse('♣8')]
    ctx.cards.trump_card = Card.parse('♠')

    result = get_add_strategy()
    assert len(result) == 0


def test_get_add_strategy_empty_table():
    ctx.cards.our_hand = [
        Card.parse('♠6'),
        Card.parse('♥7'),
        Card.parse('♦8'),
        Card.parse('♣9'),
        Card.parse('♠10'),
        Card.parse('♥J'),
    ]
    ctx.cards.cards_on_table = []
    ctx.cards.trump_card = Card.parse('♠')

    result = get_add_strategy()
    assert len(result) == 0


def test_get_add_strategy_all_trumps_in_hand():
    ctx.cards.our_hand = [
        Card.parse('♠6'),
        Card.parse('♠7'),
        Card.parse('♠8'),
        Card.parse('♠9'),
        Card.parse('♠10'),
        Card.parse('♠J'),
    ]
    ctx.cards.cards_on_table = [Card.parse('♦6'), Card.parse('♣7')]
    ctx.cards.trump_card = Card.parse('♠')

    result = get_add_strategy()
    assert len(result) == 0
