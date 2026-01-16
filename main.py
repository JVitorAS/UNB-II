from ia.vision.capture import Capture
from ia.vision.detect_hud import get_hp
from ia.policy_simple import choose_action
from controller.gamepad_emulator import send_action
from ia.utils.config import load_config
import time

def main():
    print("[INFO] IA MK11 iniciada...")

    config = load_config()
    cap = Capture()

    while True:
        frame = cap.get_frame()
        if frame is None:
            time.sleep(0.05)
            continue

        hp_player = get_hp(frame, config['hp_player_rect'], config['hp_hsv_lower'], config['hp_hsv_upper'])
        hp_enemy  = get_hp(frame, config['hp_enemy_rect'], config['hp_hsv_lower'], config['hp_hsv_upper'])

        hp_player = hp_player if hp_player is not None else 1.0
        hp_enemy  = hp_enemy  if hp_enemy is not None else 1.0

        action = choose_action({
            "hp_player": hp_player,
            "hp_enemy": hp_enemy
        })

        print(f"[MK11] HP_Player={hp_player:.2f} HP_Enemy={hp_enemy:.2f} Action={action}")
        send_action(action, duration=0.10)

        time.sleep(0.15)

if __name__ == "__main__":
    main()
