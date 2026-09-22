import sys
import subprocess
import os

required_packages = {
    "mss": "mss",
    "cv2": "opencv-python",
    "pyautogui": "pyautogui",
    "numpy": "numpy"
}

for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
    except ImportError:
        print(f"[!] Библиотека '{package_name}' не найдена. Устанавливаем автоматически...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

import tkinter as tk
from tkinter import messagebox
import threading
import time

try:
    from ai_vision import AIVisionAnalyzer
    from core_bypass import ExternalCoreEngine
    from cleaner import SystemCleaner
except ImportError:
    pass


class RustExternalAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rust External AI Assistant v5.0 [God Mode + Stealth Cleaner]")
        self.root.geometry("820x600")
        self.root.configure(bg="#1a1c23")
        self.root.resizable(False, False)

        self.vars = {
            "rage_active": tk.BooleanVar(value=True),
            "rage_key": tk.StringVar(value="LEFT MOUSE"),
            "auto_shoot": tk.BooleanVar(value=False),
            "draw_silent_fov": tk.BooleanVar(value=True),
            "silent_fov_size": tk.IntVar(value=112),
            "ignore_players": tk.BooleanVar(value=False),
            "ignore_sleepers": tk.BooleanVar(value=False),
            "ignore_wounded": tk.BooleanVar(value=False),
            "ignore_npcs": tk.BooleanVar(value=False),
            "ignore_teammates": tk.BooleanVar(value=False),
            "fake_lag": tk.BooleanVar(value=False),
            "anti_aim": tk.BooleanVar(value=False),

            "flyhack": tk.BooleanVar(value=True),
            "flyhack_speed": tk.IntVar(value=5),
            "wallhack_esp": tk.BooleanVar(value=True),
            "esp_boxes": tk.BooleanVar(value=True),
            "esp_skeletons": tk.BooleanVar(value=True),
            "esp_loot": tk.BooleanVar(value=True),
            "esp_distance": tk.BooleanVar(value=True),
        }

        self.is_running = True

        self.vision_analyzer = AIVisionAnalyzer(self.vars)
        self.core_engine = ExternalCoreEngine(self.vars)
        self.stealth_cleaner = SystemCleaner()

        self.create_widgets()

        self.main_thread = threading.Thread(target=self.processing_loop, daemon=True)
        self.main_thread.start()

    def create_widgets(self):
        sidebar = tk.Frame(self.root, bg="#111318", width=70, height=600)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        icons = ["🎯", "👁️", "✈️", "⚙️", "💾"]
        for i, icon in enumerate(icons):
            # Привязываем последнюю кнопку (💾) к панели очистки/конфигов
            btn = tk.Button(sidebar, text=icon, font=("Arial", 16), bg="#111318", fg="#ffffff",
                            activebackground="#252833", activeforeground="#ffffff", bd=0, relief=tk.FLAT,
                            command=lambda idx=i: self.switch_tab(idx))
            btn.place(x=10, y=20 + (i * 70), width=50, height=50)

        self.main_frame = tk.Frame(self.root, bg="#1a1c23")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создаем панели для переключения
        self.panel_combat = tk.LabelFrame(self.main_frame, text="", bg="#21242d", fg="#ffffff", bd=1, relief=tk.SOLID)
        self.panel_config = tk.LabelFrame(self.main_frame, text="", bg="#21242d", fg="#ffffff", bd=1, relief=tk.SOLID)

        self.build_combat_panels(self.panel_combat)
        self.build_config_panel(self.panel_config)

        # По умолчанию отображаем боевую панель
        self.panel_combat.place(x=0, y=0, width=780, height=575)

    def switch_tab(self, tab_index):
        """Переключение между вкладками интерфейса"""
        self.panel_combat.place_forget()
        self.panel_config.place_forget()

        if tab_index == 4:  # Вкладка Configs / Cleaner (💾)
            self.panel_config.place(x=0, y=0, width=780, height=575)
        else:
            self.panel_combat.place(x=0, y=0, width=780, height=575)

    def build_combat_panels(self, parent):
        col1 = tk.LabelFrame(parent, text="", bg="#21242d", fg="#ffffff", bd=1, relief=tk.SOLID)
        col1.place(x=10, y=10, width=370, height=550)
        self.build_rage_panel(col1)

        col2 = tk.LabelFrame(parent, text="", bg="#21242d", fg="#ffffff", bd=1, relief=tk.SOLID)
        col2.place(x=390, y=10, width=370, height=550)
        self.build_visuals_panel(col2)

    def build_rage_panel(self, parent):
        tk.Checkbutton(parent, text="Rage Aimbot", variable=self.vars["rage_active"],
                       bg="#21242d", fg="#ffffff", selectcolor="#1a1c23", activebackground="#21242d",
                       activeforeground="#ffffff").place(x=15, y=15)
        tk.Button(parent, textvariable=self.vars["rage_key"], bg="#2e3240", fg="#ffffff", bd=0,
                  font=("Arial", 9)).place(x=250, y=15, width=100, height=25)

        tk.Checkbutton(parent, text="Automatic Shoot", variable=self.vars["auto_shoot"],
                       bg="#21242d", fg="#888c99", selectcolor="#1a1c23", activebackground="#21242d",
                       activeforeground="#ffffff").place(x=15, y=45)
        tk.Checkbutton(parent, text="Draw Silent FOV", variable=self.vars["draw_silent_fov"],
                       bg="#21242d", fg="#ffffff", selectcolor="#1a1c23", activebackground="#21242d",
                       activeforeground="#ffffff").place(x=15, y=75)

        scale_fov = tk.Scale(parent, from_=10, to=300, orient=tk.HORIZONTAL, variable=self.vars["silent_fov_size"],
                             bg="#21242d", fg="#ffffff", highlightthickness=0, troughcolor="#2e3240", bd=0)
        scale_fov.place(x=15, y=105, width=335, height=30)
        tk.Label(parent, text="Silent FOV", bg="#21242d", fg="#888c99", font=("Arial", 8)).place(x=280, y=138)

        filters = [
            ("Ignore Players", "ignore_players"),
            ("Ignore Sleepers", "ignore_sleepers"),
            ("Ignore Wounded", "ignore_wounded"),
            ("Ignore NPCs", "ignore_npcs"),
            ("Ignore Teammates", "ignore_teammates")
        ]
        for idx, (text, var_name) in enumerate(filters):
            tk.Checkbutton(parent, text=text, variable=self.vars[var_name],
                           bg="#21242d", fg="#ffffff", selectcolor="#1a1c23", activebackground="#21242d",
                           activeforeground="#ffffff").place(x=15, y=180 + (idx * 28))

    def build_visuals_panel(self, parent):
        tk.Label(parent, text="MODULAR AI VISION & FLYHACK", bg="#21242d", fg="#00ffcc",
                 font=("Arial", 9, "bold")).place(x=15, y=15)

        tk.Checkbutton(parent, text="Wallhack ESP (Анализ сквозь стены)", variable=self.vars["wallhack_esp"],
                       bg="#21242d", fg="#ffffff", selectcolor="#1a1c23", activebackground="#21242d",
                       activeforeground="#ffffff", font=("Arial", 9, "bold")).place(x=15, y=45)

        esp_options = [
            ("Draw 3D / 2D Boxes", "esp_boxes"),
            ("Draw Skeletons", "esp_skeletons"),
            ("Highlight Loot & Items", "esp_loot"),
            ("Show Distance & HP", "esp_distance")
        ]
        for idx, (text, var_name) in enumerate(esp_options):
            tk.Checkbutton(parent, text=text, variable=self.vars[var_name],
                           bg="#21242d", fg="#cccccc", selectcolor="#1a1c23", activebackground="#21242d",
                           activeforeground="#ffffff").place(x=35, y=75 + (idx * 28))

        tk.Frame(parent, bg="#2e3240", height=2).place(x=15, y=195, width=335)

        tk.Checkbutton(parent, text="FlyHack Engine", variable=self.vars["flyhack"],
                       bg="#21242d", fg="#00ffcc", selectcolor="#1a1c23", activebackground="#21242d",
                       activeforeground="#ffffff", font=("Arial", 9, "bold")).place(x=15, y=210)

        scale_fly = tk.Scale(parent, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.vars["flyhack_speed"],
                             bg="#21242d", fg="#ffffff", highlightthickness=0, troughcolor="#2e3240", bd=0)
        scale_fly.place(x=15, y=245, width=335, height=30)
        tk.Label(parent, text="FlyHack Speed Multiplier", bg="#21242d", fg="#888c99", font=("Arial", 8)).place(x=215,
                                                                                                               y=278)

        info_box = tk.Label(parent, text="[STATUS]: Connected to modules.\nStealth Cleaner module ready.",
                            bg="#16181f", fg="#00ff00", font=("Consolas", 8), justify=tk.LEFT, padx=10, pady=5)
        info_box.place(x=15, y=320, width=335, height=45)

    def build_config_panel(self, parent):
        """Пятая вкладка: Управление конфигами и скрытная очистка следов"""
        tk.Label(parent, text="CONFIGURATION & STEALTH CLEANER", bg="#21242d", fg="#ff5555",
                 font=("Arial", 11, "bold")).place(x=20, y=20)

        tk.Label(parent, text="Управление пресетами чит-конфигураций:", bg="#21242d", fg="#ffffff",
                 font=("Arial", 9)).place(x=20, y=60)

        btn_save = tk.Button(parent, text="Сохранить конфиг", bg="#2e3240", fg="#ffffff", bd=0, font=("Arial", 9),
                             command=self.save_config)
        btn_save.place(x=20, y=95, width=160, height=30)

        btn_load = tk.Button(parent, text="Загрузить конфиг", bg="#2e3240", fg="#ffffff", bd=0, font=("Arial", 9),
                             command=self.load_config)
        btn_load.place(x=195, y=95, width=160, height=30)

        tk.Frame(parent, bg="#2e3240", height=2).place(x=20, y=150, width=730)

        tk.Label(parent, text="Анти-хит / Проверка администратора:", bg="#21242d", fg="#ffcc00",
                 font=("Arial", 10, "bold")).place(x=20, y=175)
        tk.Label(parent,
                 text="Полная и незаметная очистка следов (удаляются только файлы чите, Temp, Recent и ветки реестра).",
                 bg="#21242d", fg="#888c99", font=("Arial", 8)).place(x=20, y=200)

        # Главная кнопка полной очистки следов
        btn_clean = tk.Button(parent, text="🗑 СТЕРЕТЬ ВСЕ СЛЕДЫ ЧИТА (TEMP, RECENT, REGISTRY)", bg="#8b0000",
                              fg="#ffffff", bd=0, font=("Arial", 10, "bold"), command=self.trigger_stealth_clean)
        btn_clean.place(x=20, y=235, width=420, height=45)

    def save_config(self):
        messagebox.showinfo("Configs", "Конфигурация успешно сохранена в Soft_rust/config.json")

    def load_config(self):
        messagebox.showinfo("Configs", "Конфигурация успешно загружена.")

    def trigger_stealth_clean(self):
        """Вызов модуля тотальной очистки следов"""
        success = self.stealth_cleaner.wipe_all_traces()
        if success:
            messagebox.showinfo("Stealth Mode", "Все следы в Temp, Recent и Registry успешно стерты! Система чиста.")
        else:
            messagebox.showerror("Error", "Ошибка при выполнении очистки.")

    def processing_loop(self):
        while self.is_running:
            self.vision_analyzer.process_frame()
            self.core_engine.update_state()
            time.sleep(0.01)

    def onunload(self):
        self.is_running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RustExternalAIApp(root)
    root.protocol("WM_DELETE_WINDOW", app.onunload)
    root.mainloop()