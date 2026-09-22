import time

class ExternalCoreEngine:
    def __init__(self, config_vars):
        self.vars = config_vars

    def update_state(self):
        if self.vars["flyhack"].get():
            speed_multiplier = self.vars["flyhack_speed"].get()
            time.sleep(0.005 * speed_multiplier)