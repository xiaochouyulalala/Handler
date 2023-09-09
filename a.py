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

# 示例：模拟按下和释放键盘按键（例如，模拟按下并释放空格键）
press_key('space')
sleep(1)  # 延迟1秒钟
release_key('space')

# 示例：模拟键盘输入（例如，输入文本）
type_text('Hello, World!')

# 示例：模拟组合键（例如，同时按下Control和C键复制文本）
press_key('ctrl')
press_key('c')
sleep(1)  # 延迟1秒钟
release_key('c')
release_key('ctrl')
