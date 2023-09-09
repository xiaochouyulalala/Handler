import pyautogui
import time

# 模拟按下和释放键盘按键
def press_key(key):
    pyautogui.keyDown(key)

def release_key(key):
    pyautogui.keyUp(key)

# 模拟键盘输入
def type_text(text):
    pyautogui.write(text)

# 间隔一段时间
def sleep(seconds):
    time.sleep(seconds)


def gamepad_Control(signal):
    angle = signal["Angle"]
    if signal["up"] and not signal["bark"]:
        press_key("w")
        # print("前进")
        if angle>0:
            press_key("d")
            sleep(0.1/(1+angle))
            release_key("d")
        elif angle < 0:
            press_key("a")
            sleep(0.1/(1-angle))
            release_key("a")
        release_key("w")
    elif signal["bark"]:
        press_key("s")
        sleep(2/(1+angle))
        # print("后退")
        if angle>0:
            press_key("d")
            sleep(0.01/(1+angle))
            release_key("d")
        elif angle < 0:
            press_key("a")
            sleep(0.01/(1-angle))
            release_key("a")
        release_key("s")
    elif not signal["up"] and not signal["bark"]:
        if angle>0:
            press_key("d")
            sleep(0.01/(1+angle))
            release_key("d")
        elif angle < 0:
            press_key("a")
            sleep(0.01/(1-angle))
            release_key("a")

    return