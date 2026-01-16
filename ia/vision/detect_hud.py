import os
import cv2
import time
import numpy as np

from ia.utils.config import load_config
from ia.vision.capture import Capture


def draw_hud(frame, fps, hp_p1, hp_p2):
    """
    Overlay de debug no MK11
    """
    h, w, _ = frame.shape
    overlay = frame.copy()

    cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.55, frame, 0.45, 0)

    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.putText(frame, f"P1 HP: {hp_p1:.2f}", (10, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.putText(frame, f"P2 HP: {hp_p2:.2f}", (w - 160, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return frame


def get_hp(frame, rect, hsv_lower, hsv_upper):
    """
    Calcula porcentagem de HP do MK11 via máscara HSV
    """
    x, y, w, h = rect
    roi = frame[y:y+h, x:x+w]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(hsv_lower), np.array(hsv_upper))

    ratio = cv2.countNonZero(mask) / (w * h)
    return ratio


class MK11HUD:
    """
    Classe limpa para leitura do HUD com integração futura
    """
    def __init__(self):
        self.config = load_config()
        self.capture = Capture()
        self.last_time = time.time()

    def read(self):
        """
        Retorna HP dos dois jogadores + FPS
        """
        frame = self.capture.get_frame()
        if frame is None:
            return None, None, 0

        now = time.time()
        fps = 1 / (now - self.last_time)
        self.last_time = now

        hp_p1 = get_hp(frame,
                       self.config['hp_player_rect'],
                       self.config['hp_hsv_lower'],
                       self.config['hp_hsv_upper'])

        hp_p2 = get_hp(frame,
                       self.config['hp_enemy_rect'],
                       self.config['hp_hsv_lower'],
                       self.config['hp_hsv_upper'])

        # Segurança se falhar
        hp_p1 = hp_p1 if hp_p1 is not None else 1.0
        hp_p2 = hp_p2 if hp_p2 is not None else 1.0

        return hp_p1, hp_p2, fps

    def debug(self):
        """
        Loop somente para debug visual
        """
        print("[MK11] HUD Debug Viewer iniciado...")
        while True:
            frame = self.capture.get_frame()
            if frame is None:
                continue

            hp_p1, hp_p2, fps = self.read()

            frame = draw_hud(frame, fps, hp_p1, hp_p2)
            cv2.imshow("MK11 HUD", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    MK11HUD().debug()
