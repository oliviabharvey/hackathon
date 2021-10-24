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

class Sides(Enum):
    """
    Defines all possible side possibilities
    """
    NONE = 0
    LEFT = 1
    RIGHT = 2

class ClickTypes(Enum):
    """
    Defines all possible click types
    """
    NONE = 0
    GOOD = 1
    BAD = 2

class TimeStamps(Enum):
    """
    Defines all possible time stamps for data manager"
    """
    DISPLAY = 0
    TOUCH = 1
    FEED = 2
    EAT = 3
