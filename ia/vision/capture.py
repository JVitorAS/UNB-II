import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import load_config
import cv2
import numpy as np
import mss

class Capture:
    def __init__(self):
        self.sct = mss.mss()
        self.cfg = load_config()
        self.monitor = self.cfg.get("monitor", None)

        if self.monitor is None:
            self.monitor = self.sct.monitors[1]
            print("[capture] Nenhum monitor definido no config.json — usando tela primária.")
        else:
            print(f"[capture] Usando monitor definido: {self.monitor}")

    def get_frame(self):
        """Captura o frame atual da tela"""
        sct_img = self.sct.grab(self.monitor)
        frame = np.array(sct_img)
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        return frame

    def get_region(self, rect):
        """Captura apenas a região retangular (x, y, w, h)"""
        frame = self.get_frame()
        x, y, w, h = rect
        return frame[y:y+h, x:x+w]

if __name__ == "__main__":
    cap = Capture()
    frame = cap.get_frame()
    cv2.imshow("Tela capturada", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
