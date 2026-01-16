# ia/vision/mk11_states.py

from enum import Enum

class State(Enum):
    UNKNOWN = 0
    MENU = 1
    CHARACTER_SELECT = 2
    VERSUS = 3
    PRE_FIGHT = 4
    FIGHTING = 5
    ROUND_END = 6
    MATCH_END = 7
