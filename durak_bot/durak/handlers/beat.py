from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.types.card import Card
from durak_bot.types.player_state import EPlayerState
from durak_bot.util.cards import can_beat
from durak_bot.util.logger import logger


@durak.event(command='b')
def on_beaten(data: dict):
    player_id: int = data['id']
    card_beaten = Card.parse(data['c'])
    card_used = Card.parse(data['b'])

    # Detect tricked cards
    if ctx.lobby.is_tricks_enabled and not can_beat(beat_by=card_used, to_beat=card_beaten):
        durak.game.report_trick(card=str(card_used), card_beaten=str(card_beaten))
        logger.warning(f'Nuh uh! Trick rejected, {card_used = }, {card_beaten = }')
        ctx.cards.got_tricked = True
        return

    # Update card number for player
    ctx.cards.dec_cards_count(player_id)

    # Mark card used as the one on table
    player_index = ctx.players.index_of(EPlayerState.DEFENDS)
    assert player_index is not None
    ctx.cards.card_beaten(card_beaten, card_used, player_index=player_index)
    logger.info(f'Card {card_beaten} has been beaten by {card_used}')
