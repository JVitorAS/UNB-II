import vgamepad as vg
import time

# Cria o gamepad virtual
gamepad = vg.VX360Gamepad()

# Mapeamento dos botões para Mortal Kombat 11
BUTTONS = {
    'light_punch': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,       # X
    'heavy_punch': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,       # Y
    'light_kick':  vg.XUSB_BUTTON.XUSB_GAMEPAD_A,       # A
    'heavy_kick':  vg.XUSB_BUTTON.XUSB_GAMEPAD_B,       # B
    'block':        vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,  # RB
    'grab':         vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,   # LB
    'pause':        vg.XUSB_BUTTON.XUSB_GAMEPAD_START,           # START
    'stance':       vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,            # BACK
}

def send_action(action, duration=0.1):
    button = BUTTONS.get(action)
    if button is None:
        print(f"[WARN] Ação desconhecida: {action}")
        return

    gamepad.press_button(button=button)
    gamepad.update()
    time.sleep(duration)
    gamepad.release_button(button=button)
    gamepad.update()

def move_direction(direction, x=0, y=0, duration=0.2):
    """
    Direção no analógico esquerdo
    Valores de x e y vão de -1.0 a 1.0
    """
    gamepad.left_joystick_float(x_value=x, y_value=y)
    gamepad.update()
    time.sleep(duration)
    gamepad.left_joystick_float(x_value=0, y_value=0)
    gamepad.update()
