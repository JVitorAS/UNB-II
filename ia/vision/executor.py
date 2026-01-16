import time
from controller.gamepad_emulator import send_action
from .mapping import ACTIONS

def execute_action(action_id, duration=0.1):
    action = ACTIONS.get(action_id, "idle")
    send_action(action, duration=duration)
