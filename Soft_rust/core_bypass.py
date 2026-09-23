import pyautogui

pyautogui.FAILSAFE = False


class ExternalCoreEngine:
    def __init__(self, config_vars):
        self.vars = config_vars
        self.last_target = None

    def process_combat(self, targets):
        """
        Только информационная обработка. Не управляет мышью и не кликает.
        Игрок сам управляет прицеливанием и стрельбой.
        """
        if not targets:
            self.last_target = None
            return

        # Находим ближайшую цель (с минимальной дистанцией)
        closest = None
        min_dist = float('inf')
        for target in targets:
            dist = target.get('dist', 999)
            if dist < min_dist:
                min_dist = dist
                closest = target

        self.last_target = closest

        # Никогда не двигаем мышь и не кликаем автоматически.
        # ESP уже показывает цели на оверлее - игрок сам прицеливается.
