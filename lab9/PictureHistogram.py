from copy import deepcopy

import numpy as np


class PictureHistogram:

    @staticmethod
    def create_histogram(data: np.ndarray):
        """:return: массив красных пикселей, если картинка черно-белая /
        массив красных + зеленых + синий пикселей, если картинка цветная
        """
        is_gray = True
        red, green, blue = [], [], []

        for row in data:
            for rgb in row:
                r, g, b = rgb[0], rgb[1], rgb[2]
                red.append(r)
                green.append(g)
                blue.append(b)

                if red != green or red != blue:
                    is_gray = False

        if is_gray:
            return red
        else:
            return red, green, blue

    @staticmethod
    def check_color(color):
        """
        Проверка, что пиксель не вылезает за [0; 255]
        :param color: пиксель
        """
        if color < 0:
            return 0

        if color > 255:
            return 255

        return color

    def equalize_histogram(self, data: np.ndarray, ignored_pixels_ratio: float):
        """
        Выравнивание гистограммы
        :param data: изображение
        :param ignored_pixels_ratio: доля игнорируемых пикселей
        :return: массив пикселей - изображение
        """

        # Проверка, что доля игнорируемых пикселей указана корректно
        if ignored_pixels_ratio < 0 or ignored_pixels_ratio >= 0.5:
            raise AttributeError("Pixel ratio must be in range: [0; 0.5)")

        # Массив частот для каждого уровня яркости
        frequency = [0] * 256

        # Подсчёт частоты встречаемости каждого уровня яркости
        for row in data:
            for rgb in row:
                r, g, b = rgb[0], rgb[1], rgb[2]
                intensity = (0.299 * r + 0.587 * g + 0.114 * b)
                frequency[intensity] += 1

        # Подсчёт кумулятивной частоты
        cumulative_frequency = [0] * 256
        cumulative_frequency[0] = frequency[0]
        for i in range(1, 256, 1):
            cumulative_frequency[i] = cumulative_frequency[i - 1] + frequency[i]

        height = len(data)
        width = len(data[0])
        # Подсчёт новых значений яркости
        equalized_intensity = [0] * 256
        total_pixels = height * width
        for i in range(256):
            equalized_intensity[i] = round(cumulative_frequency[i] * 255 / total_pixels)

        # Определение минимального и максимального значений яркости в каждом канале, учитывая игнорируемые пиксели
        min_red, min_green, min_blue = 0, 0, 0
        max_red, max_green, max_blue = 255, 255, 255
        ignored_pixels_count = round(total_pixels * ignored_pixels_ratio)

        for i in range(256):
            if cumulative_frequency[i] > ignored_pixels_count:
                min_red, min_green, min_blue = i, i, i
                break

        for i in range(255, -1, -1):
            if cumulative_frequency[i] < total_pixels - ignored_pixels_count:
                max_red, max_green, max_blue = i, i, i
                break

        new_data: np.ndarray
        new_data = deepcopy(data)
        i = 0
        j = 0
        # Применение новых значений яркости к изображению
        for row in data:
            i += 1
            for rgb in row:
                j += 1
                r, g, b = rgb[0], rgb[1], rgb[2]
                new_red = equalized_intensity[r]
                new_green = equalized_intensity[g]
                new_blue = equalized_intensity[b]

                new_red = round((new_red - min_red) / (max_red - min_red) * 255)
                new_green = round((new_green - min_green) / (max_green - min_green) * 255)
                new_blue = round((new_blue - min_blue) / (max_blue - min_blue) * 255)

                new_red = self.check_color(new_red)
                new_green = self.check_color(new_green)
                new_blue = self.check_color(new_blue)

                new_data[i][j][0] = new_red
                new_data[i][j][1] = new_green
                new_data[i][j][2] = new_blue

        return new_data
