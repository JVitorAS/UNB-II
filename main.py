import time
from ia.vision.capture import Capture
from ia.vision.detect_hud import get_hp
from controller.gamepad_emulator import send_action
from ia.policy_simple import choose_action
from ia.utils.config import load_config

def main():
    print("[INFO] Iniciando IA UNIB-II REAL para Mortal Kombat 11...")

    # Carrega config da HUD e parâmetros
    config = load_config()

    # Inicializa captura de tela
    cap = Capture()

    # Loop principal da IA
    while True:
        frame = cap.get_frame()
        if frame is None:
            print("[WARN] Frame não capturado — ignorando ciclo")
            time.sleep(0.05)
            continue

        # Detecta as barras de HP do MK11
        hp_player = get_hp(
            frame,
            config['hp_player_rect'],
            config['hp_hsv_lower'],
            config['hp_hsv_upper']
        )

        hp_enemy = get_hp(
            frame,
            config['hp_enemy_rect'],
            config['hp_hsv_lower'],
            config['hp_hsv_upper']
        )

        # Segurança: se falhar, assume 100%
        hp_player = hp_player if hp_player is not None else 1.0
        hp_enemy = hp_enemy if hp_enemy is not None else 1.0

        # Estado que a IA usa para decidir a ação
        state = {
            'hp_player': hp_player,
            'hp_enemy': hp_enemy
        }

        # Escolhe ação baseada no estado do MK11
        action = choose_action(state)

        print(
            f"[MK11 DEBUG] HP Player: {hp_player:.2f} | "
            f"HP Enemy: {hp_enemy:.2f} | Action: {action}"
        )

        # Envia ação para o gamepad virtual
        send_action(action, duration=0.10)

        # Delay para não saturar o jogo
        time.sleep(0.15)

if __name__ == "__main__":
    main()
