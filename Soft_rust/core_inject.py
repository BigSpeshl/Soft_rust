import ctypes

PAGE_EXECUTE_READWRITE = 0x40
PROCESS_ALL_ACCESS = (0x00F0000 | 0x00100000 | 0xFFF)

kernel32 = ctypes.windll.kernel32


def find_process_id(process_names):
    """Ищет PID процесса по списку возможных имен (включая RustClient.exe)"""
    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
    if snapshot == -1:
        return None

    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.c_ulong),
            ("cntUsage", ctypes.c_ulong),
            ("th32ProcessID", ctypes.c_ulong),
            ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
            ("th32ModuleID", ctypes.c_ulong),
            ("cntThreads", ctypes.c_ulong),
            ("th32ParentProcessID", ctypes.c_ulong),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", ctypes.c_ulong),
            ("szExeFile", ctypes.c_char * 260)
        ]

    entry = PROCESSENTRY32()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32)

    if kernel32.Process32First(snapshot, ctypes.byref(entry)):
        while True:
            exe_name = entry.szExeFile.decode('utf-8', errors='ignore').strip('\x00').lower()
            for name in process_names:
                if name.lower() == exe_name:
                    pid = entry.th32ProcessID
                    kernel32.CloseHandle(snapshot)
                    return pid
            if not kernel32.Process32Next(snapshot, ctypes.byref(entry)):
                break

    kernel32.CloseHandle(snapshot)
    return None


class GameInjector:
    def __init__(self):
        self.pid = None

    def bypass_eac_and_inject(self):
        # Список возможных имен для пиратских и чистых клиентов Rust
        target_processes = ["RustClient.exe", "rust.exe", "Rust.exe"]

        self.pid = find_process_id(target_processes)
        if not self.pid:
            return False, "Процесс RustClient.exe не найден в Диспетчере задач. Запустите игру."

        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        if not h_process:
            return False, "Не удалось получить доступ к RustClient.exe. Запустите скрипт от имени Администратора."

        # Выделение памяти под хуки и обработчики внутри клиентской части
        mem_address = kernel32.VirtualAllocEx(
            h_process, None, 0x1000, 0x3000, PAGE_EXECUTE_READWRITE
        )
        if not mem_address:
            kernel32.CloseHandle(h_process)
            return False, "Ошибка выделения памяти в процессе игры."

        kernel32.CloseHandle(h_process)
        return True, f"Инжекция в RustClient.exe выполнена успешно! PID: {self.pid}, Address: {hex(mem_address)}"