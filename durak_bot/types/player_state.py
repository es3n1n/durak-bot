from enum import unique, IntEnum


@unique
class EPlayerState(IntEnum):
    CAN_ADD_MORE_CARDS = 0
    SHOULD_MOVE = 1
    IDLING_WAITING_FOR_DEFENCE = 2
    PASSED = 3
    IDLING_PASS_PRESSED = 4
    FINISHED = 5
    IDLING = 6
    TAKES = 7
    WILL_DEFEND = 8
    DEFENDS = 9
