from durak_bot.ctx.types.cards_state import _cards_state as cards
from durak_bot.ctx.types.lobby_state import _lobby_state as lobby
from durak_bot.ctx.types.players_state import _players_state as players
from durak_bot.ctx.types.stats_state import _stats_state as stats


__all__ = (
    'cards',
    'lobby',
    'players',
    'stats',
    'reset',
)


def reset():
    # Stats is intentionally never resets
    cards.reset()
    lobby.reset()
    players.reset()
