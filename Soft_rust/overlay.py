import tkinter as tk


class GameOverlay:
    def __init__(self, config_vars):
        self.vars = config_vars
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")

        # На весь экран
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, bg="black",
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.is_active = True
        self.render_loop()

    def render_loop(self):
        if not self.is_active:
            return

        self.canvas.delete("all")

        # Отрисовка Silent FOV круга по центру экрана
        if self.vars["draw_silent_fov"].get() and self.vars["rage_active"].get():
            fov_radius = self.vars["silent_fov_size"].get()
            cx, cy = self.screen_width // 2, self.screen_height // 2

            # Неоновый контур FOV
            self.canvas.create_oval(
                cx - fov_radius, cy - fov_radius,
                cx + fov_radius, cy + fov_radius,
                outline="#00ffcc", width=2
            )
            # Перекрестие центра
            self.canvas.create_line(cx - 5, cy, cx + 5, cy, fill="#00ffcc", width=1)
            self.canvas.create_line(cx, cy - 5, cx, cy + 5, fill="#00ffcc", width=1)

        self.root.after(15, self.render_loop)

    def close(self):
        self.is_active = False
        try:
            self.root.destroy()
        except:
            pass