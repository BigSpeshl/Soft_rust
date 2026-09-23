import tkinter as tk
from pynput import keyboard

class GameOverlay:
    def __init__(self, config_vars, parent_root=None):
        self.vars = config_vars
        self.root = tk.Toplevel(parent_root if parent_root else tk.Tk())
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")

        self.root.update_idletasks()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.is_active = True
        self.detected_targets = []
        self.detected_resources = []

        self.is_visible = True
        self._setup_hotkey()
        self.render_loop()

    def _setup_hotkey(self):
        try:
            self._listener = keyboard.Listener(on_press=self._on_key_press)
            self._listener.start()
        except:
            pass

    def _on_key_press(self, key):
        try:
            if key == keyboard.Key.insert:
                self.root.after(0, self._toggle_overlay)
        except:
            pass

    def _toggle_overlay(self):
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
        else:
            self.root.deiconify()
            self.root.lift()
            self.is_visible = True

    def render_loop(self):
        if not self.is_active:
            return

        self.canvas.delete("all")
        cx, cy = self.screen_width // 2, self.screen_height // 2

        # 1. Silent FOV
        if self.vars["draw_silent_fov"].get() and self.vars["rage_active"].get():
            fov_radius = self.vars["silent_fov_size"].get()
            self.canvas.create_oval(cx - fov_radius, cy - fov_radius, cx + fov_radius, cy + fov_radius, outline="#00ffcc", width=2)

        # 2. ESP Игроков
        if self.vars["wallhack_esp"].get():
            for target in self.detected_targets:
                x, y, w, h, dist = target['x'], target['y'], target['w'], target['h'], target['dist']
                if self.vars["esp_boxes"].get():
                    self.canvas.create_rectangle(x, y, x + w, y + h, outline="#ff007f", width=2)
                if self.vars["esp_distance"].get():
                    self.canvas.create_text(x, y - 15, text=f"[DIST: {dist}m]", fill="#00ff99", font=("Consolas", 8, "bold"), anchor="nw")

            # 3. ESP Ресурсов
            if self.vars["esp_loot"].get():
                for res in self.detected_resources:
                    rx, ry, rdist, rname = res['x'], res['y'], res['dist'], res['name']
                    self.canvas.create_oval(rx - 3, ry - 3, rx + 3, ry + 3, fill="#ffcc00", outline="")
                    self.canvas.create_text(rx + 8, ry - 5, text=f"{rname} [{rdist}m]", fill="#ffcc00", font=("Consolas", 7, "bold"), anchor="nw")

        self.root.after(15, self.render_loop)

    def update_esp_data(self, targets, resources):
        self.detected_targets = targets
        self.detected_resources = resources

    def close(self):
        self.is_active = False
        try:
            self._listener.stop()
            self.root.destroy()
        except:
            pass