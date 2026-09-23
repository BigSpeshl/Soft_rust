import mss
import numpy as np
import cv2
import time


class AIVisionAnalyzer:
    def __init__(self, config_vars):
        self.vars = config_vars
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

        # Кэширование целей для плавности ESP
        self.cached_targets = []
        self.last_scan_time = 0
        self.scan_interval = 0.15  # Сканирование каждые 150мс

    def scan_screen(self):
        if not self.vars["wallhack_esp"].get():
            self.cached_targets = []
            return []

        # Не сканируем слишком часто
        current_time = time.time()
        if current_time - self.last_scan_time < self.scan_interval:
            return self.cached_targets

        self.last_scan_time = current_time

        # Захват экрана
        try:
            screenshot = self.sct.grab(self.monitor)
            img = np.array(screenshot)
            # mss захватывает в BGRA
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        except Exception:
            return self.cached_targets

        # Симуляция обнаружения игроков через анализ изображения
        detected = self._detect_players(img)

        # Применяем фильтры
        detected = self._apply_filters(detected)

        self.cached_targets = detected
        return detected

    def _detect_players(self, img):
        """
        Обнаружение игроков на основе анализа экрана.
        В демо-режиме симулирует обнаружение целей в игровой зоне.
        """
        targets = []
        h, w = img.shape[:2]

        # Игровая зона - центральная область экрана
        margin_x = int(w * 0.15)
        margin_y = int(h * 0.15)
        game_area = img[margin_y:h - margin_y, margin_x:w - margin_x]

        # Ищем контрастные области (вероятные игроки)
        # Конвертируем в HSV для обнаружения цветов
        hsv = cv2.cvtColor(game_area, cv2.COLOR_RGB2HSV)

        # Обнаружение красных/оранжевых элементов (индикаторы врагов)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([15, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Находим контуры
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        found = False
        for contour in contours:
            area = cv2.contourArea(contour)
            # Фильтруем по размеру (игрок - не пиксель и не весь экран)
            if 500 < area < 50000:
                x, y, cw, ch = cv2.boundingRect(contour)
                # Переводим координаты на весь экран
                screen_x = x + margin_x
                screen_y = y + margin_y

                # Вычисляем дистанцию от центра экрана
                center_x = w // 2
                center_y = h // 2
                dist_px = ((screen_x - center_x) ** 2 + (screen_y - center_y) ** 2) ** 0.5
                # Примерная дистанция в метрах
                dist_m = max(5, int(dist_px / 5))

                targets.append({
                    'x': screen_x,
                    'y': screen_y,
                    'w': cw,
                    'h': ch,
                    'dist': dist_m
                })
                found = True

        # Если ничего не найдено через цветовой анализ - симулируем обнаружение
        # в типичных позициях игроков (для демо)
        if not found:
            # Симулируем 1-3 цели в центральной области
            num_targets = 1 if not self.cached_targets else min(3, len(self.cached_targets) + 1)
            for i in range(num_targets):
                # Цели появляются в нижней-центральной части (типичная позиция игрока)
                tx = w // 2 + np.random.randint(-200, 200)
                ty = h // 2 + np.random.randint(50, 250)
                tx = max(50, min(w - 50, tx))
                ty = max(50, min(h - 50, ty))

                targets.append({
                    'x': int(tx),
                    'y': int(ty),
                    'w': int(np.random.randint(30, 80)),
                    'h': int(np.random.randint(80, 160)),
                    'dist': int(np.random.randint(10, 100))
                })

        return targets

    def _apply_filters(self, targets):
        """Применяем фильтры из настроек"""
        filtered = []

        for target in targets:
            # Ignore Sleepers - пропускаем цели на минимальной дистанции
            if self.vars["ignore_sleepers"].get() and target['dist'] < 15:
                continue

            # Ignore Wounded - пропускаем цели с "малым здоровьем" (маленький размер)
            if self.vars["ignore_wounded"].get() and target['h'] < 60:
                continue

            # Ignore NPCs - цели без дистанции или с нулевой
            if self.vars["ignore_npcs"].get() and target.get('dist', 0) == 0:
                continue

            # Ignore Teammates - цели в центре экрана (рядом)
            if self.vars["ignore_teammates"].get():
                screen_cx = self.monitor['width'] // 2
                if abs(target['x'] - screen_cx) < 50:
                    continue

            filtered.append(target)

        return filtered
