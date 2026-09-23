import sys
import subprocess
import os

required_packages = {"mss": "mss", "cv2": "opencv-python", "pyautogui": "pyautogui", "numpy": "numpy",
                     "pynput": "pynput"}
for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

import tkinter as tk
from tkinter import messagebox
import threading
import time

from ai_vision import AIVisionAnalyzer
from core_bypass import ExternalCoreEngine
from cleaner import SystemCleaner
from overlay import GameOverlay
from core_inject import GameInjector


class RustExternalAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rust Internal/External GodMode Suite v5.4 [All Tabs Fixed & Injected]")
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
        self.injector = GameInjector()
        self.vision_analyzer = AIVisionAnalyzer(self.vars, self.injector)
        self.core_engine = ExternalCoreEngine(self.vars)
        self.stealth_cleaner = SystemCleaner() if SystemCleaner else None

        self.create_widgets()

        self.overlay_thread = threading.Thread(target=self.start_overlay, args=(root,), daemon=True)
        self.overlay_thread.start()

        self.main_thread = threading.Thread(target=self.processing_loop, daemon=True)
        self.main_thread.start()

    def start_overlay(self, parent_root):
        try:
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

        # Создаем все 5 раздельных вкладок для полной работоспособности
        self.tab_combat = tk.Frame(self.container, bg="#0f111a")
        self.tab_visuals = tk.Frame(self.container, bg="#0f111a")
        self.tab_movement = tk.Frame(self.container, bg="#0f111a")
        self.tab_protection = tk.Frame(self.container, bg="#0f111a")
        self.tab_config = tk.Frame(self.container, bg="#0f111a")

        self._tabs = [self.tab_combat, self.tab_visuals, self.tab_movement, self.tab_protection, self.tab_config]

        self.build_combat_tab(self.tab_combat)
        self.build_visuals_tab(self.tab_visuals)
        self.build_movement_tab(self.tab_movement)
        self.build_protection_tab(self.tab_protection)
        self.build_config_tab(self.tab_config)

        self.show_tab(self.tab_combat)

    def switch_tab(self, tab_index):
        for tab in self._tabs:
            tab.pack_forget()
        self.show_tab(self._tabs[tab_index])

    def show_tab(self, tab):
        tab.pack(fill=tk.BOTH, expand=True)

    def build_combat_tab(self, parent):
        panel = tk.LabelFrame(parent, text=" 🎯 COMBAT / AIMBOT & SILENT FOV ", bg="#141722", fg="#00ffcc",
                              font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        panel.place(x=0, y=0, width=745, height=585)

        self.cyber_check(panel, "Rage Aimbot Active", self.vars["rage_active"], 30, 30)
        self.cyber_check(panel, "Automatic Shoot", self.vars["auto_shoot"], 30, 70)
        self.cyber_check(panel, "Draw Silent FOV (Overlay)", self.vars["draw_silent_fov"], 30, 110)

        tk.Label(panel, text="Silent FOV Radius", bg="#141722", fg="#8f93a2", font=("Segoe UI", 9)).place(x=32, y=160)
        scale_fov = tk.Scale(panel, from_=20, to=300, orient=tk.HORIZONTAL, variable=self.vars["silent_fov_size"],
                             bg="#141722", fg="#00ffcc", highlightthickness=0, troughcolor="#1e2230", bd=0)
        scale_fov.place(x=30, y=185, width=400, height=35)

    def build_visuals_tab(self, parent):
        panel = tk.LabelFrame(parent, text=" 👁️ ESP & RESOURCE TRACKING ", bg="#141722", fg="#ff007f",
                              font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        panel.place(x=0, y=0, width=745, height=585)

        self.cyber_check(panel, "Wallhack ESP (Players & Entities)", self.vars["wallhack_esp"], 30, 30, fg="#ff007f")
        self.cyber_check(panel, "Draw 3D / 2D Boxes", self.vars["esp_boxes"], 50, 75)
        self.cyber_check(panel, "Draw Skeletons", self.vars["esp_skeletons"], 50, 115)
        self.cyber_check(panel, "Highlight Loot & Resources (Nodes, Sulfur, Stone)", self.vars["esp_loot"], 50, 155,
                         fg="#ffcc00")
        self.cyber_check(panel, "Show Distance & HP", self.vars["esp_distance"], 50, 195)

    def build_movement_tab(self, parent):
        panel = tk.LabelFrame(parent, text=" ✈️ MOVEMENT & EXPLOITS ", bg="#141722", fg="#00ffcc",
                              font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        panel.place(x=0, y=0, width=745, height=585)

        self.cyber_check(panel, "FlyHack Engine (Speedhack)", self.vars["flyhack"], 30, 30, fg="#00ffcc")
        tk.Label(panel, text="FlyHack Speed Multiplier", bg="#141722", fg="#8f93a2", font=("Segoe UI", 9)).place(x=32,
                                                                                                                 y=80)
        scale_fly = tk.Scale(panel, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.vars["flyhack_speed"],
                             bg="#141722", fg="#00ffcc", highlightthickness=0, troughcolor="#1e2230", bd=0)
        scale_fly.place(x=30, y=105, width=400, height=35)

    def build_protection_tab(self, parent):
        panel = tk.LabelFrame(parent, text=" 🛡️ ANTI-CHEAT PROTECTION & INJECTION ", bg="#141722", fg="#ff4444",
                              font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        panel.place(x=0, y=0, width=745, height=585)

        tk.Label(panel, text="Инжекция в rust.exe с обходом EasyAntiCheat (EAC):", bg="#141722", fg="#ffffff",
                 font=("Segoe UI", 10, "bold")).place(x=30, y=40)

        btn_inject = tk.Button(panel, text="⚡ ВЫПОЛНИТЬ ИНЖЕКЦИЮ В RUST.EXE", bg="#1c577a", fg="#ffffff",
                               font=("Segoe UI", 10, "bold"), bd=0, command=self.trigger_injection)
        btn_inject.place(x=30, y=85, width=380, height=45)

        self.inject_status_lbl = tk.Label(panel, text="[STATUS]: Ожидание запуска игры и инжекции...", bg="#141722",
                                          fg="#8f93a2", font=("Consolas", 9))
        self.inject_status_lbl.place(x=30, y=145)

    def build_config_tab(self, parent):
        panel = tk.LabelFrame(parent, text=" 💾 PRESETS & STEALTH TRACE CLEANER ", bg="#141722", fg="#ffcc00",
                              font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        panel.place(x=0, y=0, width=745, height=585)

        btn_clean = tk.Button(panel, text="🗑 СТЕРЕТЬ ВСЕ СЛЕДЫ ЧИТА (TEMP, RECENT, REGISTRY)", bg="#7a1c1c",
                              fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, command=self.trigger_stealth_clean)
        btn_clean.place(x=30, y=50, width=450, height=45)

    def cyber_check(self, parent, text, var, x, y, fg="#ffffff"):
        chk = tk.Checkbutton(parent, text=text, variable=var, bg="#141722", fg=fg, selectcolor="#0f111a",
                             activebackground="#141722", activeforeground=fg, font=("Segoe UI", 9), bd=0)
        chk.place(x=x, y=y)

    def trigger_injection(self):
        success, msg = self.injector.bypass_eac_and_inject()
        if success:
            self.inject_status_lbl.config(text=f"[SUCCESS]: {msg}", fg="#00ff99")
            messagebox.showinfo("Injection", msg)
        else:
            self.inject_status_lbl.config(text=f"[ERROR]: {msg}", fg="#ff4444")
            messagebox.showerror("Injection Error", msg)

    def trigger_stealth_clean(self):
        if self.stealth_cleaner and self.stealth_cleaner.wipe_all_traces():
            messagebox.showinfo("Stealth Mode", "Полная очистка следов успешно завершена!")
        else:
            messagebox.showerror("Error", "Ошибка при очистке следов.")

    def processing_loop(self):
        while self.is_running:
            targets, resources = [], []
            if self.vision_analyzer:
                try:
                    targets, resources = self.vision_analyzer.scan_screen()
                except:
                    pass

            if hasattr(self, 'overlay') and self.overlay:
                try:
                    self.overlay.update_esp_data(targets, resources)
                except:
                    pass

            if self.core_engine:
                try:
                    self.core_engine.process_combat(targets)
                except:
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