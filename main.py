from ia.vision.capture import Capture
from ia.vision.detect_hud import get_hp
from ia.actions.executor import execute_action
from ia.states.state_machine import StateMachine
from ia.states.states import State
from ia.memory.memory import MemoryJSON
from ia.env.mk11_env import MK11Env

def main():

    memory = MemoryJSON()
    state_machine = StateMachine()
    cap = Capture()

    def _get_state():
        return state_machine.current

    def _get_hp():
        frame = cap.get_frame()
        return get_hp(frame)

    env = MK11Env(
        get_state_fn=_get_state,
        get_hp_fn=_get_hp,
        do_action_fn=execute_action
    )

    print("[IA] Rodando...")

    obs, _ = env.reset()

    while True:
        # por enquanto só escolhe idle
        action = 0
        obs, reward, terminated, truncated, _ = env.step(action)
