from dataclasses import dataclass

from durak_bot.const.cards import (
    CARD_TYPES_SET,
    CARD_OVERALL_RANGE_SET,
)


@dataclass(frozen=True)
class Card:
    type: str
    value: str

    @classmethod
    def parse(cls, value: str) -> 'Card':
        assert len(value) > 0

        card_type = value[0]
        card_value = value[1:]

        # Once deck is empty, the trump card would be just ♦ instead of ♦A
        assert not card_value or card_value in CARD_OVERALL_RANGE_SET
        assert card_type in CARD_TYPES_SET
        return cls(
            type=card_type,
            value=card_value,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Card):
            return self.type == other.type and self.value == other.value
        raise NotImplementedError

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Card):
            return self.type != other.type or self.value != other.value
        raise NotImplementedError

    def __ge__(self, other: 'Card') -> bool:
        raise NotImplementedError

    def __le__(self, other: 'Card') -> bool:
        raise NotImplementedError

    def __str__(self) -> str:
        return f'{self.type}{self.value}'
