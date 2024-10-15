from dataclasses import dataclass

from durak_bot.database import db, EGameResult
from durak_bot.ctx.types.base import BaseState
from durak_bot.util.logger import logger


@dataclass
class StatsState(BaseState):
    initial_balance: int | None = None
    last_balance: int | None = None

    @staticmethod
    def print() -> None:
        stats = db.get_game_stats()
        total = sum(stats.values())

        logger.info(
            'Stats: '
            f'wins {stats.get(EGameResult.WIN)} / '
            f'ties {stats.get(EGameResult.TIE)} / '
            f'loses {stats.get(EGameResult.LOSE)} / '
            f'total {total}'
        )

    @classmethod
    def inc_wins(cls) -> None:
        db.record_game_result(EGameResult.WIN)
        cls.print()

    @classmethod
    def inc_ties(cls) -> None:
        db.record_game_result(EGameResult.TIE)
        cls.print()

    @classmethod
    def inc_loses(cls) -> None:
        db.record_game_result(EGameResult.LOSE)
        cls.print()


_stats_state = StatsState()
