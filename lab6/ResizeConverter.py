import numpy as np
from math import floor, sin, pi
from copy import deepcopy

from PIL import Image

from lab1.managers.pgm_manager import PgmManager
from lab1.managers.ppm_manager import PpmManager


class ResizeConverter:
    @staticmethod
    def closest_neighbour(data: np.ndarray, new_height: int, new_width: int) -> np.ndarray:
        h_coef = len(data) / new_height
        w_coef = len(data[0]) / new_width

        new_data = np.zeros((new_height, new_width))

        for i in range(new_height):
            for j in range(new_width):
                new_data[i][j] = data[floor(i * h_coef)][floor(j * w_coef)]

        return new_data

    @staticmethod
    def interpolate(width, height, A, B, C, D):
        A *= (1 - width) * (1 - height)
        B *= width * (1 - height)
        C *= (1 - width) * height
        D *= width * height

        result = A + B + C + D
        if result > 255:
            result = 255
        elif result < 0:
            result = 0

        return result

    @staticmethod
    def bilinear(old_data: np.ndarray, height: int, width: int):
        data: np.ndarray = deepcopy(old_data) * 255

        old_height, old_width = len(data), len(data[0])

        h_coef = len(data) / height
        w_coef = len(data[0]) / width

        new_data = np.zeros((height, width))

        for i in range(height):
            for j in range(width):
                old_x, old_y = floor(j * w_coef), floor(i * h_coef)
                diff_x, diff_y = j * w_coef - old_x, i * h_coef - old_y
                A = data[old_y][old_x]

                if old_x + 1 < old_width:
                    B = data[old_y][old_x + 1]
                else:
                    B = data[old_y][old_x]

                if old_y + 1 < old_height:
                    C = data[old_y + 1][old_x]
                else:
                    C = data[old_y][old_x]

                if old_x + 1 < old_width and old_y + 1 < old_height:
                    D = data[old_y + 1][old_x + 1]
                elif old_x + 1 < old_width:
                    D = data[old_y][old_x + 1]
                elif old_y + 1 < old_height:
                    D = data[old_y + 1][old_x]
                else:
                    D = data[old_y][old_x]

                new_data[i, j] = ResizeConverter.interpolate(diff_x, diff_y, A, B, C, D)

        return (new_data / 255).astype(np.double)

    @staticmethod
    def lanczos_kernel(x: np.double) -> np.double:
        if x == 0:
            return 1.0
        elif -3 <= x <= 3:
            return (3 * sin(pi * x) * sin(pi * x / 3)) / ((pi ** 2) * (x ** 2))
        else:
            return .0

    @staticmethod
    def lanczos(old_data: np.ndarray, height: int, width: int):
        data: np.ndarray = deepcopy(old_data) * 255
        old_width, old_height = len(data[0]), len(data)

        new_data = np.zeros((height, width))

        h_coef = old_height / height
        w_coef = old_width / width
        a = 3

        for i in range(height):
            for j in range(width):
                res = 0

                for k in range(int(i * h_coef) - a, int(i * h_coef) + a + 1):
                    for z in range(int(j * w_coef) - a, int(j * w_coef) + a + 1):
                        dx, dy = z, k

                        if dx >= old_width:
                            dx = old_width - 1
                        if dy >= old_height:
                            dy = old_height - 1
                        if dx < 0:
                            dx = 0
                        if dy < 0:
                            dy = 0

                        Lx = ResizeConverter.lanczos_kernel(j * w_coef - z)
                        Ly = ResizeConverter.lanczos_kernel(i * h_coef - k)

                        res += data[dy][dx] * Lx * Ly

                if res > 255:
                    res = 255
                elif res < 0:
                    res = 0

                new_data[i][j] = res

        return (new_data / 255).astype(np.double)

    @staticmethod
    def bc_filter(x, b, c):
        res = 0
        if abs(x) < 1:
            res = (12 - 9 * b - 6 * c) * (abs(x) ** 3) + (-18 + 12 * b + 6 * c) * (abs(x) ** 2) + (6 - 2 * b)
        elif 1 <= abs(x) < 2:
            res = (-b - 6 * c) * (abs(x) ** 3) + (6 * b + 30 * c) * (abs(x) ** 2) + (-12 * b - 48 * c) * abs(x) + (
                    8 * b + 24 * c)

        res *= 1 / 6
        return res

    @staticmethod
    def bc_splines(old_data: np.ndarray, height: int, width: int, b=0.0, c=0.5):
        data: np.ndarray = deepcopy(old_data) * 255
        old_height, old_width = len(data), len(data[0])

        h_coef = old_height / height
        w_coef = old_width / width
        temp = np.zeros((height, width))

        new_data = np.zeros((height, width))

        for i in np.arange(0, height, 1 / h_coef):
            for j in range(width):
                res = 0

                for k in np.arange(-5 / w_coef, old_width + 5 / w_coef):
                    dk = int(k)
                    if dk < 0:
                        dk = 0
                    elif dk >= old_width:
                        dk = old_width - 1

                    k_x = ResizeConverter.bc_filter(j * w_coef - k, b, c)

                    if k_x == 0:
                        continue

                    res += data[int(round(i * h_coef))][dk] * k_x
                if res < 0:
                    res = 0
                elif res > 255:
                    res = 255

                temp[floor(i)][j] = res

        for i in range(width):
            for j in range(height):
                res = 0

                for k in np.arange(-5 / h_coef, height + 5 / h_coef, 1 / h_coef):
                    dk = int(k)
                    if dk < 0:
                        dk = 0
                    elif dk >= height:
                        dk = height - 1 / h_coef

                    k_y = ResizeConverter.bc_filter((j - k) * h_coef, b, c)

                    if k_y == 0:
                        continue

                    res += temp[floor(dk)][i] * k_y

                if res < 0:
                    res = 0
                elif res > 255:
                    res = 255

                new_data[j][i] = res
        return (np.array(new_data) / 255).astype(np.double)


def test():
    manager = PgmManager()
    pgm_data = manager.read_p5(
        "C:\\Users\\sword\\PycharmProjects\\cg22-project-Kikoriki\\lab1\\gradient.pgm")
    pgm = Image.fromarray((ResizeConverter.bilinear(pgm_data, 100, 100) * 255).astype(np.uint8), "L")
    # img = Image.fromarray((np.array(img_data) * 255).astype(np.uint8))

    # manager2 = PpmManager()
    # ppm_data = manager2.read_p6(
    #     "C:\\Users\\komra\\PycharmProjects\\cg22-project-Kikoriki\\cg22-project-Kikoriki\\lab1\\sample.ppm")
    # ppm = Image.fromarray((ResizeConverter.closest_neighbour(ppm_data, 500, 1000) * 255).astype(np.uint8), "L")

    pgm.show()
