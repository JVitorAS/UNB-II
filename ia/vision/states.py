from enum import Enum

class GameState(Enum):
    MENU = 0
    CHARACTER_SELECT = 1
    VERSUS = 2
    PRE_FIGHT = 3
    FIGHTING = 4
    FINISH = 5
    MATCH_END = 6
    UNKNOWN = 7
