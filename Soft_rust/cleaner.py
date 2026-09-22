import os
import glob
import winreg

class SystemCleaner:
    def __init__(self):
        # Ключевые маркеры для поиска и удаления следов чита
        self.signatures = ["Soft_rust", "rust_cheat", "ExternalAI", "Aimbot"]

    def wipe_all_traces(self):
        """Главный метод скрытной очистки следов"""
        try:
            self.clean_temp_files()
            self.clean_recent_items()
            self.clean_registry_traces()
            return True
        except Exception as e:
            print(f"[!] Ошибка очистки: {e}")
            return False

    def clean_temp_files(self):
        """Точечная очистка файлов в папке Temp, содержащих сигнатуры чита"""
        temp_dir = os.environ.get('TEMP', '')
        if not temp_dir or not os.path.exists(temp_dir):
            return

        # Ищем файлы и папки по маске внутри Temp
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for file in files:
                if any(sig.lower() in file.lower() for sig in self.signatures):
                    try:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    except:
                        pass
            for d in dirs:
                if any(sig.lower() in d.lower() for sig in self.signatures):
                    try:
                        dir_path = os.path.join(root, d)
                        os.rmdir(dir_path)
                    except:
                        pass

    def clean_recent_items(self):
        """Очистка ссылок на запуск скрипта в папке Recent (автоматическая фильтрация)"""
        recent_dir = os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Recent')
        if not os.path.exists(recent_dir):
            return

        for shortcut in os.listdir(recent_dir):
            if any(sig.lower() in shortcut.lower() for sig in self.signatures):
                try:
                    path = os.path.join(recent_dir, shortcut)
                    os.remove(path)
                except:
                    pass

    def clean_registry_traces(self):
        """Удаление записей из реестра Windows (RecentDocs, ShellBag и Run)"""
        reg_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]

        for hkey, subkey_path in reg_paths:
            try:
                key = winreg.OpenKey(hkey, subkey_path, 0, winreg.KEY_ALL_ACCESS)
                # Удаляем ключи, содержащие сигнатуры чита
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        if any(sig.lower() in str(value).lower() or sig.lower() in name.lower() for sig in self.signatures):
                            winreg.DeleteValue(key, name)
                        else:
                            i += 1
                    except WindowsError:
                        break
                winreg.CloseKey(key)
            except:
                pass