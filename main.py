import pyautogui
import time

def main():
    # Параметры
    pyautogui.PAUSE = 0.6
    # Время движения мышью
    duration = 0.5
    img_path = './images'

    # Попыток найти модификацию
    max_tries = 3
    # Расстояние от константы до выхода к которому её будем подключать
    place_offset = 200
    # Битовая маска подключаемая на выход
    out_values = (1, 0)

    width, height = pyautogui.size()

    # Открытие и создание проекта
    x, y = pyautogui.locateCenterOnScreen(f'{img_path}/taskbar_OL.png', confidence=0.8)
    pyautogui.click(x=x, y=y, duration=duration)
    time.sleep(2)
    x, y = pyautogui.locateCenterOnScreen(f'{img_path}/new.png', confidence=0.9)
    pyautogui.click(x=x, y=y, duration=duration)
    time.sleep(1)

    x, y = pyautogui.locateCenterOnScreen(f'{img_path}/pr200.png', region=(0, 0, int(width/2), int(height/2)), confidence=0.95)
    pyautogui.click(x=x, y=y, duration=duration)
    
    pyautogui.moveRel(500, 500, duration)
    modification_found = False
    tries = 0
    while not modification_found:
        if tries >= max_tries:
            pyautogui.alert('Модификация ПР не найдена')
            exit()
        try:
            x, y = pyautogui.locateCenterOnScreen(f'{img_path}/pr_model.png', region=(0, int(height/3), int(width/2), int(2*height/3)), confidence=0.95)
            pyautogui.doubleClick(x = x, y = y, duration = duration)
            modification_found = True
            time.sleep(1)
        except pyautogui.ImageNotFoundException:
            pyautogui.scroll(-1)
            pyautogui.scroll(-1)
            tries += 1

    const_button_point = pyautogui.locateCenterOnScreen(f'{img_path}/const.png')

    # Задаём битовую маску на выходе вытаскивая блоки контанты
    # openCV необходим для задания confidence при поиске in.png, out.png. При больших значениях confidence не все выходы/входы распознаются
    for i, q_in_region in enumerate(pyautogui.locateAllOnScreen(f'{img_path}/in.png', confidence=0.8, limit=len(out_values))):
        if out_values[i] is None:
            continue

        q_in_point = pyautogui.center(q_in_region)
        pyautogui.click(*const_button_point, duration=duration)
        pyautogui.click(x = q_in_point.x - place_offset, y = q_in_point.y, duration = duration)
        pyautogui.doubleClick()
        pyautogui.write(str(out_values[i]))
        pyautogui.press('enter')

        cur_x, cur_y = pyautogui.position()
        pyautogui.moveTo(*pyautogui.locateCenterOnScreen(f'{img_path}/out.png', region=(cur_x, cur_y - 50, 300, 300), confidence=0.8))

        pyautogui.mouseDown()
        pyautogui.dragTo(*q_in_point, duration=duration, mouseDownUp=False)
        pyautogui.mouseUp()

    btn_center = pyautogui.locateCenterOnScreen(f'{img_path}/play.png', grayscale=False, confidence=0.9, limit=2)
    pyautogui.click(*btn_center, duration=duration)
    pyautogui.press('F6') # Пуск симуляции

    pyautogui.alert('Конец программы')


if __name__ == '__main__':
    main()