import pyautogui

pyautogui.PAUSE = 0.25

for reg in pyautogui.locateAllOnScreen('./images/play.png', grayscale=False, confidence=0.8):
    print(reg)
    pyautogui.moveTo(*pyautogui.center(reg))