import vgamepad as vg

gamepad = vg.VX360Gamepad()


def gamepad_Control(signal):
    gamepad.reset()
    angle = signal["Angle"]
    if signal["up"] and not signal["bark"]:
        gamepad.right_trigger_float(value_float=0.7)
        gamepad.left_joystick_float(x_value_float=angle, y_value_float=0.5)
        # print("前进")
    elif signal["bark"]:
        gamepad.left_trigger_float(value_float=0.8)
        gamepad.left_joystick_float(x_value_float=angle, y_value_float=-0.5)
        # print("后退")
    elif not signal["up"] and not signal["bark"]:
        gamepad.left_joystick_float(x_value_float=angle, y_value_float=0.5)

    gamepad.update()

    return