import cv2
import pytesseract


class TextDetector:
    def __init__(self):
        self.last_text = ""

        self.config_fight = '--psm 7 -c tessedit_char_whitelist=FGHIJKLMNOPQRSTUVWXYZ'
        self.config_finish = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ '
        self.config_win = '--psm 7'

    def extract_text(self, frame, config):
        text = pytesseract.image_to_string(frame, config=config)
        return text.upper().strip()

    def detect_fight(self, frame):
        text = self.extract_text(frame, self.config_fight)
        if "FIGHT" in text:
            return True
        return False

    def detect_finish(self, frame):
        text = self.extract_text(frame, self.config_finish)
        if "FINISH HIM" in text or "FINISH HER" in text:
            return True
        return False

    def detect_victory(self, frame):
        text = self.extract_text(frame, self.config_win)

        terms = ["WIN", "WINS", "VICTORY", "YOU WIN", "DEFEAT"]
        return any(t in text for t in terms)
