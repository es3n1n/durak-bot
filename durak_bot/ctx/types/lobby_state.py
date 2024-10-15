from dataclasses import dataclass
from durak_bot.ctx.types.base import BaseState


@dataclass
class LobbyState(BaseState):
    players_count: int = 0
    winners_count: int = 0

    position: int = 0
    deck_size: int = 0

    bet: int = 0

    is_passing_enabled: bool = False
    is_tricks_enabled: bool = False
    is_draw_enabled: bool = False
    is_fast: bool = False

    @property
    def is_transferring_enabled(self):
        return self.is_passing_enabled

    @property
    def is_forwarding_enabled(self) -> bool:
        return self.is_passing_enabled

    @property
    def next_player_id(self) -> int:
        result = self.position + 1
        if result >= self.players_count:
            result = 0
        return result


_lobby_state = LobbyState()
