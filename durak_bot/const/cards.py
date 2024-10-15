CARD_TYPES: list[str] = [
    '♣',
    '♠',
    '♦',
    '♥',
]
CARD_TYPES_SET: set[str] = set(CARD_TYPES)

CARD_OVERALL_RANGE: list[str] = [
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    'J',
    'Q',
    'K',
    'A',
]
CARD_OVERALL_RANGE_SET: set[str] = set(CARD_OVERALL_RANGE)

CARD_RANGES: dict[int, set[str]] = {
    24: {
        '9',
        '10',
        'J',
        'Q',
        'K',
        'A',
    },
    36: {
        '6',
        '7',
        '8',
        '9',
        '10',
        'J',
        'Q',
        'K',
        'A',
    },
    52: {
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        'J',
        'Q',
        'K',
        'A',
    },
}
