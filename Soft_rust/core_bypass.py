import time

class ExternalCoreEngine:
    def __init__(self, config_vars):
        self.vars = config_vars
        self.last_target = None

    def process_combat(self, targets):
        if not self.vars["rage_active"].get() or not targets:
            self.last_target = None
            return

        # Находим ближайшую цель в радиусе FOV
        closest = min(targets, key=lambda t: t['dist'], default=None)
        if closest:
            self.last_target = closest
            # Если включен автовыстрел и цель в зоне поражения
            if self.vars["auto_shoot"].get():
                # Передача сигнала клика мыши в игровой драйвер
                pass