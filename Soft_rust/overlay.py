import tkinter as tk
import threading
from pynput import keyboard


class GameOverlay:
    def __init__(self, config_vars, parent_root=None):
        self.vars = config_vars
        self.root = tk.Toplevel(parent_root if parent_root else tk.Tk())
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")

        # Обновляем окно, чтобы получить корректные размеры экрана
        self.root.update_idletasks()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, bg="black",
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.is_active = True
        self.detected_targets = []

        # Горячая клавиша - Insert для сворачивания/разворачивания оверлея
        self.is_visible = True
        self._setup_hotkey()

        self.render_loop()

    def _setup_hotkey(self):
        """Настраивает глобальную горячую клавишу Insert для сворачивания/разворачивания оверлея"""
        try:
            self._listener = keyboard.Listener(on_press=self._on_key_press)
            self._listener.start()
        except Exception as e:
            print(f"Hotkey setup error: {e}")

    def _on_key_press(self, key):
        """Обработчик нажатия клавиш"""
        try:
            # Insert key code на pynput
            if key == keyboard.Key.insert:
                self.root.after(0, self._toggle_overlay)
        except Exception as e:
            print(f"Key press error: {e}")

    def _toggle_overlay(self):
        """Сворачивает/разворачивает оверлей"""
        if self.is_visible:
            # Сворачиваем - делаем окно невидимым
            self.root.withdraw()
            self.is_visible = False
        else:
            # Разворачиваем - показываем окно
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.is_visible = True

    def render_loop(self):
        if not self.is_active:
            return

        self.canvas.delete("all")

        cx, cy = self.screen_width // 2, self.screen_height // 2

        # 1. Отрисовка Silent FOV
        if self.vars["draw_silent_fov"].get() and self.vars["rage_active"].get():
            fov_radius = self.vars["silent_fov_size"].get()
            self.canvas.create_oval(
                cx - fov_radius, cy - fov_radius,
                cx + fov_radius, cy + fov_radius,
                outline="#00ffcc", width=2
            )
            self.canvas.create_line(cx - 4, cy, cx + 4, cy, fill="#00ffcc", width=1)
            self.canvas.create_line(cx, cy - 4, cx, cy + 4, fill="#00ffcc", width=1)

        # 2. Отрисовка активного ESP (Боксы, Скелеты, Дистанция поверх экрана)
        if self.vars["wallhack_esp"].get():
            targets = getattr(self, "detected_targets", [])
            for target in targets:
                x, y, w, h, dist = target['x'], target['y'], target['w'], target['h'], target['dist']

                # 3D/2D Boxes
                if self.vars["esp_boxes"].get():
                    self.canvas.create_rectangle(x, y, x + w, y + h, outline="#ff007f", width=2)

                # Skeletons
                if self.vars["esp_skeletons"].get():
                    head_x, head_y = x + w // 2, y + 15
                    chest_x, chest_y = x + w // 2, y + h // 3
                    self.canvas.create_line(head_x, head_y, chest_x, chest_y, fill="#00ffcc", width=2)
                    self.canvas.create_line(chest_x, chest_y, x + w // 4, y + h // 2, fill="#00ffcc", width=2)
                    self.canvas.create_line(chest_x, chest_y, x + (w * 3) // 4, y + h // 2, fill="#00ffcc", width=2)

                # Distance & HP
                if self.vars["esp_distance"].get():
                    self.canvas.create_text(x, y - 15, text=f"[DIST: {dist}m]", fill="#00ff99",
                                            font=("Consolas", 8, "bold"), anchor="nw")

        self.root.after(15, self.render_loop)

    def update_esp_data(self, targets):
        self.detected_targets = targets

    def close(self):
        self.is_active = False
        try:
            if hasattr(self, '_listener') and self._listener:
                self._listener.stop()
            self.root.destroy()
        except:
            pass
