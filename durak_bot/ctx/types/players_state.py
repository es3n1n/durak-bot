from dataclasses import dataclass, field
from durak_bot.ctx.types.base import BaseState
from durak_bot.types.player_state import EPlayerState
from durak_bot.ctx.types.lobby_state import _lobby_state


@dataclass
class PlayersState(BaseState):
    player_states: list[EPlayerState] = field(default_factory=list)

    def is_someone(self, state: EPlayerState) -> bool:
        return any(x == state for x in self.player_states)

    def are_we(self, *states: EPlayerState) -> bool:
        return self.player_states[_lobby_state.position] in states

    def index_of(self, state: EPlayerState) -> int | None:
        try:
            return self.player_states.index(state)
        except ValueError:
            return None


_players_state = PlayersState()
