from enum import Enum, unique


@unique
class EGameResult(Enum):
    WIN = 'win'
    LOSE = 'lose'
    TIE = 'tie'

    @classmethod
    def all(cls) -> list['EGameResult']:
        return [
            cls.WIN,
            cls.LOSE,
            cls.TIE,
        ]
