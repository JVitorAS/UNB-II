# ia/vision/mk11_detector.py

import cv2
import pytesseract
from ultralytics import YOLO
from .ia.vision.states import State

class MK11Detector:
    def __init__(self, model_path="data/mk11_yolo.pt"):
        self.model = YOLO(model_path)
        self.state = State.UNKNOWN
        self.trigger_fight = False

    def _detect_fight_text(self, frame):
        # ROI vai depender da resolução, ajustável
        config = '--psm 7 -c tessedit_char_whitelist=FGHIJKLMNOPQRSTUVWXYZ'
        text = pytesseract.image_to_string(frame, config=config)
        return "FIGHT" in text.upper()

    def process(self, frame):
        results = self.model(frame)[0]
        labels = [results.names[int(c)] for c in results.boxes.cls]

        # -----------------------
        # STATE LOGIC
        # -----------------------

        if "character_select" in labels:
            self.state = State.CHARACTER_SELECT
            self.trigger_fight = False
            return self.state

        if "versus_screen" in labels:
            self.state = State.VERSUS
            self.trigger_fight = False
            return self.state

        if "health_bar" in labels:
            # tenta detectar "FIGHT"
            roi = frame[200:600, 300:1600]  # ajuste depois
            if self._detect_fight_text(roi):
                self.trigger_fight = True
                self.state = State.FIGHTING
                return self.state
            else:
                self.state = State.PRE_FIGHT
                return self.state

        if "round_end" in labels:
            self.state = State.ROUND_END
            return self.state

        if "match_end" in labels:
            self.state = State.MATCH_END
            return self.state

        return self.state
