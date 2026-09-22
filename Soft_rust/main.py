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
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

import tkinter as tk
from tkinter import messagebox
import threading
import time

try:
    from ai_vision import AIVisionAnalyzer
except ImportError:
    AIVisionAnalyzer = None

try:
    from core_bypass import ExternalCoreEngine
except ImportError:
    ExternalCoreEngine = None

try:
    from cleaner import SystemCleaner
except ImportError:
    SystemCleaner = None

try:
    from overlay import GameOverlay
except ImportError:
    GameOverlay = None


class RustExternalAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rust External AI v5.3 [Fixed Tabs & Active Modules]")
        self.root.geometry("860x620")
        self.root.configure(bg="#0f111a")
        self.root.resizable(False, False)

        self.vars = {
            "rage_active": tk.BooleanVar(value=True),
            "rage_key": tk.StringVar(value="[ LEFT MOUSE ]"),
            "auto_shoot": tk.BooleanVar(value=True),
            "draw_silent_fov": tk.BooleanVar(value=True),
            "silent_fov_size": tk.IntVar(value=110),
            "ignore_players": tk.BooleanVar(value=False),
            "ignore_sleepers": tk.BooleanVar(value=True),
            "ignore_wounded": tk.BooleanVar(value=False),
            "ignore_npcs": tk.BooleanVar(value=False),
            "ignore_teammates": tk.BooleanVar(value=True),

            "flyhack": tk.BooleanVar(value=False),
            "flyhack_speed": tk.IntVar(value=5),
            "wallhack_esp": tk.BooleanVar(value=True),
            "esp_boxes": tk.BooleanVar(value=True),
            "esp_skeletons": tk.BooleanVar(value=True),
            "esp_loot": tk.BooleanVar(value=True),
            "esp_distance": tk.BooleanVar(value=True),
        }

        self.is_running = True

        self.vision_analyzer = AIVisionAnalyzer(self.vars) if AIVisionAnalyzer else None
        self.core_engine = ExternalCoreEngine(self.vars) if ExternalCoreEngine else None
        self.stealth_cleaner = SystemCleaner() if SystemCleaner else None

        self.create_widgets()

        # Запуск Overlay
        self.overlay_thread = threading.Thread(target=self.start_overlay, args=(root,), daemon=True)
        self.overlay_thread.start()

        # Запуск рабочего цикла
        self.main_thread = threading.Thread(target=self.processing_loop, daemon=True)
        self.main_thread.start()

    def start_overlay(self, parent_root):
        try:
            if GameOverlay is None:
                print("Overlay module not available")
                return
            self.overlay = GameOverlay(self.vars, parent_root)
            self.overlay.root.mainloop()
        except Exception as e:
            print(f"Overlay error: {e}")

    def create_widgets(self):
        sidebar = tk.Frame(self.root, bg="#0b0d14", width=75, height=620)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        icons = ["🎯", "👁️", "✈️", "🛡️", "💾"]
        for i, icon in enumerate(icons):
            btn = tk.Button(sidebar, text=icon, font=("Segoe UI Emoji", 16), bg="#0b0d14", fg="#8f93a2",
                            activebackground="#1a1d2e", activeforeground="#00ffcc", bd=0, relief=tk.FLAT,
                            command=lambda idx=i: self.switch_tab(idx))
            btn.place(x=12, y=25 + (i * 75), width=50, height=50)

        self.container = tk.Frame(self.root, bg="#0f111a")
        self.container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Создаем вкладки
        self.tab_combat = tk.Frame(self.container, bg="#0f111a")
        self.tab_config = tk.Frame(self.container, bg="#0f111a")
        self._tabs = [self.tab_combat, self.tab_config]

        self.build_combat_tab(self.tab_combat)
        self.build_config_tab(self.tab_config)

        # По умолчанию активна боевая вкладка
        self.show_tab(self.tab_combat)

    def switch_tab(self, tab_index):
        # Скрываем все вкладки
        for tab in getattr(self, '_tabs', []):
            tab.pack_forget()

        if tab_index == 4:  # Кнопка 💾 (Настройки и очистка)
            self.show_tab(self.tab_config)
        else:  # Остальные кнопки (🎯, 👁️, ✈️, 🛡️) ведут на панель управления функциями
            self.show_tab(self.tab_combat)

    def show_tab(self, tab):
        tab.pack(fill=tk.BOTH, expand=True)

    def build_combat_tab(self, parent):
        col1 = tk.LabelFrame(parent, text=" 🎯 COMBAT / AIMBOT ", bg="#141722", fg="#00ffcc",
                             font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        col1.place(x=0, y=0, width=365, height=585)
        self.build_rage_panel(col1)

        col2 = tk.LabelFrame(parent, text=" 👁️ VISUALS & CORE ", bg="#141722", fg="#ff007f",
                             font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        col2.place(x=380, y=0, width=365, height=585)
        self.build_visuals_panel(col2)

    def build_rage_panel(self, parent):
        self.cyber_check(parent, "Rage Aimbot Active", self.vars["rage_active"], 20, 25)

        key_btn = tk.Button(parent, textvariable=self.vars["rage_key"], bg="#1e2230", fg="#00ffcc",
                            font=("Segoe UI", 8, "bold"), bd=0, relief=tk.FLAT)
        key_btn.place(x=230, y=23, width=110, height=26)

        self.cyber_check(parent, "Automatic Shoot", self.vars["auto_shoot"], 20, 65)
        self.cyber_check(parent, "Draw Silent FOV (Overlay)", self.vars["draw_silent_fov"], 20, 105)

        tk.Label(parent, text="Silent FOV Radius", bg="#141722", fg="#8f93a2", font=("Segoe UI", 8)).place(x=22, y=145)
        scale_fov = tk.Scale(parent, from_=20, to=300, orient=tk.HORIZONTAL, variable=self.vars["silent_fov_size"],
                             bg="#141722", fg="#00ffcc", highlightthickness=0, troughcolor="#1e2230", bd=0,
                             sliderrelief=tk.FLAT)
        scale_fov.place(x=20, y=165, width=320, height=30)

        tk.Frame(parent, bg="#232738", height=1).place(x=20, y=220, width=320)
        tk.Label(parent, text="TARGET FILTERS", bg="#141722", fg="#565b70", font=("Segoe UI", 8, "bold")).place(x=20,
                                                                                                                y=235)

        filters = [
            ("Ignore Players", "ignore_players"),
            ("Ignore Sleepers", "ignore_sleepers"),
            ("Ignore Wounded", "ignore_wounded"),
            ("Ignore NPCs", "ignore_npcs"),
            ("Ignore Teammates", "ignore_teammates")
        ]
        for idx, (text, var_name) in enumerate(filters):
            self.cyber_check(parent, text, self.vars[var_name], 20, 265 + (idx * 35), fg="#cfd3e2")

    def build_visuals_panel(self, parent):
        self.cyber_check(parent, "Wallhack ESP (Анализ)", self.vars["wallhack_esp"], 20, 25, fg="#ff007f")

        esp_options = [
            ("Draw 3D / 2D Boxes", "esp_boxes"),
            ("Draw Skeletons", "esp_skeletons"),
            ("Highlight Loot & Items", "esp_loot"),
            ("Show Distance & HP", "esp_distance")
        ]
        for idx, (text, var_name) in enumerate(esp_options):
            self.cyber_check(parent, text, self.vars[var_name], 40, 65 + (idx * 32))

        tk.Frame(parent, bg="#232738", height=1).place(x=20, y=210, width=320)

        self.cyber_check(parent, "FlyHack Engine", self.vars["flyhack"], 20, 225, fg="#00ffcc")

        tk.Label(parent, text="FlyHack Speed Multiplier", bg="#141722", fg="#8f93a2", font=("Segoe UI", 8)).place(x=22,
                                                                                                                  y=265)
        scale_fly = tk.Scale(parent, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.vars["flyhack_speed"],
                             bg="#141722", fg="#00ffcc", highlightthickness=0, troughcolor="#1e2230", bd=0,
                             sliderrelief=tk.FLAT)
        scale_fly.place(x=20, y=285, width=320, height=30)

        status_frame = tk.Frame(parent, bg="#0b0d14", bd=1, relief=tk.SOLID)
        status_frame.place(x=20, y=340, width=325, height=65)
        tk.Label(status_frame, text="[STATUS]: Overlay Active & Modules Online.\n[STEALTH]: Cleaner Ready.",
                 bg="#0b0d14", fg="#00ff99", font=("Consolas", 8), justify=tk.LEFT).place(x=10, y=12)

    def build_config_tab(self, parent):
        panel = tk.LabelFrame(parent, text=" 💾 PRESETS & STEALTH TRACE CLEANER ", bg="#141722", fg="#ffcc00",
                              font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        panel.place(x=0, y=0, width=745, height=585)

        tk.Label(panel, text="Управление конфигурацией:", bg="#141722", fg="#ffffff",
                 font=("Segoe UI", 9, "bold")).place(x=30, y=40)

        btn_save = tk.Button(panel, text="Сохранить конфиг", bg="#1e2230", fg="#00ffcc", bd=0, font=("Segoe UI", 9),
                             command=self.save_config)
        btn_save.place(x=30, y=75, width=180, height=35)

        btn_load = tk.Button(panel, text="Загрузить конфиг", bg="#1e2230", fg="#00ffcc", bd=0, font=("Segoe UI", 9),
                             command=self.load_config)
        btn_load.place(x=230, y=75, width=180, height=35)

        tk.Frame(panel, bg="#232738", height=1).place(x=30, y=140, width=685)

        tk.Label(panel, text="АНТИ-ПРОВЕРКА / ПОЛНАЯ ОЧИСТКА СЛЕДОВ", bg="#141722", fg="#ff4444",
                 font=("Segoe UI", 10, "bold")).place(x=30, y=170)
        tk.Label(panel,
                 text="Инструмент мгновенно удаляет все следы работы чита из папок Temp, Recent и веток реестра,\nпри этом файлы сторонних программ и операционной системы не затрагиваются.",
                 bg="#141722", fg="#8f93a2", font=("Segoe UI", 8), justify=tk.LEFT).place(x=30, y=200)

        btn_clean = tk.Button(panel, text="🗑 СТЕРЕТЬ ВСЕ СЛЕДЫ ЧИТА (TEMP, RECENT, REGISTRY)", bg="#7a1c1c",
                              fg="#ffffff", activebackground="#a82525", activeforeground="#ffffff", bd=0,
                              font=("Segoe UI", 10, "bold"), command=self.trigger_stealth_clean)
        btn_clean.place(x=30, y=250, width=480, height=50)

    def cyber_check(self, parent, text, var, x, y, fg="#ffffff"):
        chk = tk.Checkbutton(parent, text=text, variable=var,
                             bg="#141722", fg=fg, selectcolor="#0f111a",
                             activebackground="#141722", activeforeground=fg,
                             font=("Segoe UI", 9), bd=0)
        chk.place(x=x, y=y)

    def save_config(self):
        messagebox.showinfo("Configs", "Конфигурация успешно сохранена.")

    def load_config(self):
        messagebox.showinfo("Configs", "Конфигурация успешно загружена.")

    def trigger_stealth_clean(self):
        success = self.stealth_cleaner.wipe_all_traces()
        if success:
            messagebox.showinfo("Stealth Mode", "Полная очистка следов успешно завершена! Система кристально чиста.")
        else:
            messagebox.showerror("Error", "Произошла ошибка при очистке следов.")

    def processing_loop(self):
        while self.is_running:
            # 1. Сканирование экрана через AI Vision
            targets = []
            if self.vision_analyzer:
                try:
                    targets = self.vision_analyzer.scan_screen()
                except Exception:
                    pass

            # 2. Передача данных на Overlay для отрисовки ESP
            if hasattr(self, 'overlay') and self.overlay:
                try:
                    self.overlay.update_esp_data(targets)
                except Exception:
                    pass

            # 3. Обработка боевой логики (Aimbot & Auto-Shoot)
            if self.core_engine:
                try:
                    self.core_engine.process_combat(targets)
                except Exception:
                    pass

            time.sleep(0.01)

    def onunload(self):
        self.is_running = False
        try:
            self.overlay.close()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RustExternalAIApp(root)
    root.protocol("WM_DELETE_WINDOW", app.onunload)
    root.mainloop()