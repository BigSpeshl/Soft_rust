import time
import pyautogui

pyautogui.FAILSAFE = False


class ExternalCoreEngine:
    def __init__(self, config_vars):
        self.vars = config_vars

    def process_combat(self, targets):
        # 1. Rage Aimbot Logic
        if self.vars["rage_active"].get() and targets:
            target = targets[0]  # Берем ближайшую цель
            target_center_x = target['x'] + target['w'] // 2
            target_center_y = target['y'] + target['h'] // 3  # Наводка на голову/корпус

            screen_cx = pyautogui.size().width // 2
            screen_cy = pyautogui.size().height // 2

            # Вычисление смещения
            offset_x = (target_center_x - screen_cx) / 3.5  # Сглаживание аимбота
            offset_y = (target_center_y - screen_cy) / 3.5

            try:
                pyautogui.moveRel(offset_x, offset_y, duration=0.01)
            except:
                pass

            # 2. Automatic Shoot Logic
            if self.vars["auto_shoot"].get():
                try:
                    pyautogui.click()
                except:
                    pass

        # 3. FlyHack Engine Logic
        if self.vars["flyhack"].get():
            speed = self.vars["flyhack_speed"].get()
            time.sleep(0.002 * speed)
        else:
            time.sleep(0.01)