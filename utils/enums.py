from enum import Enum

class ScreenTypes(Enum):
    """
    Defines all possible types of touch screen displays
    """
    NONE = 0
    TWO_SQUARES = 1

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
