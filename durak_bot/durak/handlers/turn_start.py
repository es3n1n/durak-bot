from durak_bot import ctx

from durak_bot.durak.instance import durak
from durak_bot.types.card import Card
from durak_bot.util.logger import logger
from durak_bot.types.player_state import EPlayerState


@durak.event(command='turn')
def on_turn(data: dict):
    ctx.cards.deck_left = data.get('deck', 0)
    ctx.cards.trump_card = Card.parse(data['trump'])
    ctx.cards.discarded_count = data['discard']

    taking_player_index = ctx.players.index_of(EPlayerState.TAKES)
    if taking_player_index is not None:
        # Update the cards counter if someone is taking cards
        ctx.cards.number_of_cards[taking_player_index] += len(ctx.cards.cards_on_table)

        # Mark cards as unseen
        if taking_player_index != ctx.lobby.position:
            for card in ctx.cards.cards_on_table:
                ctx.cards.mark_card_as_unseen(card)
                ctx.cards.push_known_card(card, player_index=taking_player_index)

    ctx.cards.clear_table()
    logger.info(
        f"Turn start. Deck left: {ctx.cards.deck_left}, "
        f"Discarded: {ctx.cards.discarded_count}, "
        f"Our hand: {', '.join(map(str, ctx.cards.our_hand))}, "
        f"Trump: {ctx.cards.trump_card} ({ctx.cards.trump_card_type})"
    )
