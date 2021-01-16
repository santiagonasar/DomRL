from enum import Enum


class CardType(Enum):
    VICTORY = 1
    TREASURE = 2
    ACTION = 3
    REACTION = 4
    ATTACK = 5
    CURSE = 6
    DURATION = 7
    NIGHT = 8


class TurnPhase(Enum):
    ACTION_PHASE = 1
    TREASURE_PHASE = 2
    BUY_PHASE = 3
    END_PHASE = 4


class ChoiceType(Enum):
    END_TURN = 0
    ACTION = 1
    TREASURE = 2
    BUY = 3
    DISCARD = 4
    TRASH = 5
    GAIN = 6
    GAIN_TO_HAND = 7
    TOPDECK = 8
    LIBRARY = 9
    THRONE = 10
