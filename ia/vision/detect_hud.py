import os, cv2, sys, numpy as np, time

# Ajusta o path para imports internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config import load_config
from vision.capture import Capture


def draw_hud(frame, fps, hp_player=1.0, hp_enemy=1.0):
    """
    Desenha overlay informativo para debug no MK11.
    """
    h, w, _ = frame.shape

    # Barra semi-transparente
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.55, frame, 0.45, 0)

    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.putText(frame, f"P1 HP: {hp_player:.2f}", (10, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.putText(frame, f"P2 HP: {hp_enemy:.2f}", (w - 160, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return frame


def get_hp(frame, rect, hsv_lower, hsv_upper):
    """
    Calcula a porcentagem da barra de HP do MK11 dentro de uma região específica.
    HP = (pixels coloridos da barra / total da região)
    """
    x, y, w, h = rect
    roi = frame[y:y+h, x:x+w]

    # Conversão pro MK11 (HUD usa verde/amarelo dependendo do char)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(hsv_lower), np.array(hsv_upper))

    ratio = cv2.countNonZero(mask) / (w * h)
    return ratio


def run_mk11_detection():
    print("[MK11] Iniciando detecção de HUD...")
    config = load_config()
    cap = Capture()

    last_time = time.time()

    while True:
        frame = cap.get_frame()
        if frame is None:
            print("[WARN] Frame não recebido, ignorando...")
            time.sleep(0.05)
            continue

        # FPS mais estável
        now = time.time()
        fps = 1 / (now - last_time)
        last_time = now

        hp_player = get_hp(frame,
            config['hp_player_rect'],
            config['hp_hsv_lower'],
            config['hp_hsv_upper']
        )

        hp_enemy = get_hp(frame,
            config['hp_enemy_rect'],
            config['hp_hsv_lower'],
            config['hp_hsv_upper']
        )

        # Overlay debug
        frame = draw_hud(frame, fps, hp_player, hp_enemy)

        cv2.imshow("MK11 - HUD Detection", frame)

        # ESC para sair
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_mk11_detection()
