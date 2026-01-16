from .text_detector import TextDetector
from .game_state import GameState

class StateMachine:
    def __init__(self):
        self.text = TextDetector()
        self.state = GameState.UNKNOWN
        self.trigger_fight = False

    def update(self, frame, detected_labels):
        # seleção de personagem
        if "character_select" in detected_labels:
            self.state = GameState.CHARACTER_SELECT
            self.trigger_fight = False
            return self.state

        # tela versus
        if "versus_screen" in detected_labels:
            self.state = GameState.VERSUS
            self.trigger_fight = False
            return self.state

        # HUD detectada → antes do FIGHT
        if "health_bar" in detected_labels:
            if self.text.detect_fight(frame):
                self.state = GameState.FIGHTING
                self.trigger_fight = True
                return self.state
            else:
                self.state = GameState.PRE_FIGHT
                return self.state

        # FINISH HIM detectado
        if self.text.detect_finish(frame):
            self.state = GameState.FINISH
            self.trigger_fight = False
            return self.state

        # vitória / derrota
        if self.text.detect_victory(frame):
            self.state = GameState.MATCH_END
            self.trigger_fight = False
            return self.state

        return self.state
