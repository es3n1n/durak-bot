from durak_bot import ctx
from durak_bot.types.card import Card
from durak_bot.algorithm.actions.defense import get_defense_strategy, should_take_cards


def test_defend_1():
    ctx.reset()
    ctx.cards.our_hand = [
        Card(type='♦', value='10'),
        Card(type='♦', value='J'),
        Card(type='♦', value='Q'),
        Card(type='♥', value='Q'),
        Card(type='♠', value='9'),
        Card(type='♠', value='10'),
        Card(type='♠', value='Q'),
        Card(type='♠', value='K'),
        Card(type='♠', value='A'),
    ]
    ctx.cards.trump_card = Card.parse('♠')
    ctx.cards.push_unbeaten_card_on_table(Card.parse('♦J'))
    result = get_defense_strategy()

    assert result is not None


def test_defend_2():
    ctx.reset()
    ctx.cards.our_hand = [
        Card(type='♠', value='9'),
        Card(type='♠', value='J'),
        Card(type='♠', value='Q'),
        Card(type='♦', value='K'),
        Card(type='♥', value='Q'),
    ]
    ctx.cards.trump_card = Card.parse('♣10')
    ctx.cards.push_unbeaten_card_on_table(Card.parse('♣A'))
    ctx.cards.push_unbeaten_card_on_table(Card.parse('♠A'))
    result = get_defense_strategy()

    assert result is None


def test_defend_3():
    ctx.reset()
    ctx.cards.our_hand = [
        Card(type='♠', value='Q'),
        Card(type='♠', value='A'),
        Card(type='♣', value='A'),
    ]
    ctx.cards.trump_card = Card.parse('♣10')
    ctx.cards.push_unbeaten_card_on_table(Card.parse('♥J'))
    result = get_defense_strategy()

    assert result is not None


def test_defend_4():
    ctx.reset()
    ctx.cards.our_hand = [
        Card(type='♠', value='9'),
        Card(type='♠', value='Q'),
        Card(type='♠', value='A'),
        Card(type='♦', value='9'),
        Card(type='♥', value='J'),
        Card(type='♣', value='A'),
    ]
    ctx.cards.trump_card = Card.parse('♣10')
    ctx.cards.push_unbeaten_card_on_table(Card.parse('♦J'))
    result = get_defense_strategy()

    assert result is not None


def test_defend_5():
    ctx.reset()
    ctx.cards.our_hand = [
        Card(type='♠', value='10'),
        Card(type='♠', value='K'),
        Card(type='♥', value='A'),
    ]
    ctx.cards.trump_card = Card.parse('♦9')
    ctx.cards.push_unbeaten_card_on_table(Card.parse('♣Q'))
    result = get_defense_strategy()

    assert result is None


# def test_should_take_cards_too_many_trumps():
#     ctx.reset()
#     ctx.cards.beaten_cards_on_table = [Card.parse('♠6'), Card.parse('♥7')]
#     ctx.cards.unbeaten_cards_on_table = [
#         Card.parse('♠8'),
#         Card.parse('♠9'),
#         Card.parse('♦10'),
#     ]
#     ctx.cards.trump_card = Card.parse('♠')
#
#     assert should_take_cards()


def test_should_take_cards_few_trumps():
    ctx.reset()
    ctx.cards.deck_left = 5
    ctx.cards.beaten_cards_on_table = [Card.parse('♥6'), Card.parse('♦7')]
    ctx.cards.unbeaten_cards_on_table = [
        Card.parse('♥8'),
        Card.parse('♦9'),
        Card.parse('♠10'),
    ]
    ctx.cards.trump_card = Card.parse('♠')

    assert not should_take_cards()


# def test_should_take_cards_end_game_with_trump():
#     ctx.reset()
#     ctx.cards.beaten_cards_on_table = [Card.parse('♥6'), Card.parse('♦7')]
#     ctx.cards.unbeaten_cards_on_table = [Card.parse('♥8'), Card.parse('♠9')]
#     ctx.cards.trump_card = Card.parse('♠')
#     ctx.cards.deck_left = 4
#
#     assert should_take_cards()


def test_should_take_cards_end_game_no_trump():
    ctx.reset()
    ctx.cards.beaten_cards_on_table = [Card.parse('♥6'), Card.parse('♦7')]
    ctx.cards.unbeaten_cards_on_table = [Card.parse('♥8'), Card.parse('♦9')]
    ctx.cards.trump_card = Card.parse('♠')
    ctx.cards.deck_left = 4

    assert not should_take_cards()


def test_should_take_cards_mid_game_with_trump():
    ctx.reset()
    ctx.cards.beaten_cards_on_table = [Card.parse('♥6'), Card.parse('♦7')]
    ctx.cards.unbeaten_cards_on_table = [Card.parse('♥8'), Card.parse('♠9')]
    ctx.cards.trump_card = Card.parse('♠')
    ctx.cards.deck_left = 10

    assert not should_take_cards()


def test_should_take_cards_edge_case_empty_table():
    ctx.reset()
    ctx.cards.beaten_cards_on_table = []
    ctx.cards.unbeaten_cards_on_table = []
    ctx.cards.trump_card = Card.parse('♠')
    ctx.cards.deck_left = 10

    assert not should_take_cards()


# def test_should_take_cards_edge_case_all_trumps():
#     ctx.reset()
#     ctx.cards.beaten_cards_on_table = [Card.parse('♠6'), Card.parse('♠7')]
#     ctx.cards.unbeaten_cards_on_table = [
#         Card.parse('♠8'),
#         Card.parse('♠9'),
#         Card.parse('♠10'),
#     ]
#     ctx.cards.trump_card = Card.parse('♠')
#
#     assert should_take_cards()
