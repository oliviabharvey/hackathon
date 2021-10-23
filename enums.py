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
    RESET_DELAY = 2
    TOUCH_OR_DELAY = 3