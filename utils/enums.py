from enum import Enum

class DisplayPatterns(Enum):
    """
    Defines all possible types of touch screen displays
    """
    NONE = 0
    FIND_THE_SQUARE = 1
    LEFT_OR_RIGHT = 2
    LEFT_OR_RIGHT_WITH_RANDOMNESS = 3

class States(Enum):
    """
    Defines all possible states
    """
    EAT_AND_EXIT = 1
    IR_BREAK = 2
    RESET_DELAY = 3
    TOUCH_OR_DELAY = 4
    TOUCH = 5
    PUNISH_DELAY = 6
