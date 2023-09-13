import numpy as np
from random import random
from lab1.managers.pgm_manager import PgmManager
from PIL import Image
from copy import deepcopy


class Ditherer:
    def __init__(self):
        self.ordered_matrix = [
            [0.0, 48.0 / 64.0, 12.0 / 64.0, 60.0 / 64.0, 3.0 / 64.0, 51.0 / 64.0, 15.0 / 64.0, 63.0 / 64.0],
            [32.0 / 64.0, 16.0 / 64.0, 44.0 / 64.0, 28.0 / 64.0, 35.0 / 64.0, 19.0 / 64.0, 47.0 / 64.0, 31.0 / 64.0],
            [8.0 / 64.0, 56.0 / 64.0, 4.0 / 64.0, 52.0 / 64.0, 11.0 / 64.0, 59.0 / 64.0, 7.0 / 64.0, 55.0 / 64.0],
            [40.0 / 64.0, 24.0 / 64.0, 36.0 / 64.0, 20.0 / 64.0, 43.0 / 64.0, 27.0 / 64.0, 39.0 / 64.0, 23.0 / 64.0],
            [2.0 / 64.0, 50.0 / 64.0, 14.0 / 64.0, 62.0 / 64.0, 1.0 / 64.0, 49.0 / 64.0, 13.0 / 64.0, 61.0 / 64.0],
            [34.0 / 64.0, 18.0 / 64.0, 46.0 / 64.0, 30.0 / 64.0, 33.0 / 64.0, 17.0 / 64.0, 45.0 / 64.0, 29.0 / 64.0],
            [10.0 / 64.0, 58.0 / 64.0, 6.0 / 64.0, 54.0 / 64.0, 9.0 / 64.0, 57.0 / 64.0, 5.0 / 64.0, 53.0 / 64.0],
            [42.0 / 64.0, 26.0 / 64.0, 38.0 / 64.0, 22.0 / 64.0, 41.0 / 64.0, 25.0 / 64.0, 37.0 / 64.0, 21.0 / 64.0]]
        self.bytes = [
            [0, 255],
            [0, 85, 170, 255],
            [0, 36, 72, 108, 144, 180, 216, 255],
            [0, 17, 34, 51, 68, 85, 102, 119, 136, 153, 170, 187, 204, 221, 238, 255],
            [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184,
             192, 200, 208, 216, 224, 232, 240, 255],
            [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104,
             108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 148, 152, 156, 160, 164, 168, 172, 176, 180, 184, 188,
             192, 196, 200, 204, 208, 212, 216, 220, 224, 228, 232, 236, 240, 244, 248, 255],
            [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54,
             56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106,
             108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148,
             150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190,
             192, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232,
             234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 255],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
             29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
             56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82,
             83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
             108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
             129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149,
             150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170,
             171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191,
             192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212,
             213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233,
             234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254,
             255]
        ]

    def ordered(self, data: np.ndarray, byte: int = 8) -> np.ndarray:
        bitness = self.bytes[byte - 1]
        new_data = []
        for i in range(len(data)):
            new_row = []
            row = data[i]
            for j in range(len(row)):
                pixel = row[j]
                left, right = 0, -1
                for k in range(len(bitness)):
                    if (bitness[k] / 255) >= pixel:
                        if k == 0:
                            left = right = bitness[k]
                        else:
                            left, right = bitness[k - 1], bitness[k]
                        break

                if pixel >= self.ordered_matrix[i % 8][j % 8]:
                    new_pixel = right
                else:
                    new_pixel = left

                new_row.append(new_pixel)
            new_data.append(new_row)

        return (np.array(new_data) / 255).astype(np.double)

    def random(self, data: np.ndarray, byte: int = 8) -> np.ndarray:
        bitness = self.bytes[byte - 1]
        new_data = []
        for row in data:
            new_row = []
            for pixel in row:
                # [0.0,1.0)
                threshold = random()
                left, right = 0, -1
                for k in range(len(bitness)):
                    if (bitness[k] / 255) >= pixel:
                        if k == 0:
                            left = right = bitness[k]
                        else:
                            left, right = bitness[k - 1], bitness[k]
                        break

                if pixel >= threshold:
                    new_pixel = right
                else:
                    new_pixel = left

                new_row.append(new_pixel)

            new_data.append(new_row)

        return (np.array(new_data) / 255).astype(np.double)

    def atkinson(self, data: np.ndarray, byte: int = 8) -> np.ndarray:
        new_data = deepcopy(data)

        for i in range(len(new_data)):
            for j in range(len(new_data[i])):
                pixel = new_data[i][j]
                new_pixel = self.find_closest_color(pixel, byte)

                error = pixel - new_pixel

                new_data[i][j] = new_pixel

                if j + 1 < len(new_data[i]):
                    new_data[i][j + 1] += error * (1 / 8)

                    if new_data[i][j + 1] > 1:
                        new_data[i][j + 1] = 1
                    elif new_data[i][j + 1] < 0:
                        new_data[i][j + 1] = 0

                if j + 2 < len(new_data[i]):
                    new_data[i][j + 2] += error * (1 / 8)

                    if new_data[i][j + 2] > 1:
                        new_data[i][j + 2] = 1
                    elif new_data[i][j + 2] < 0:
                        new_data[i][j + 2] = 0

                if i + 1 < len(new_data):
                    if j - 1 > 0:
                        new_data[i + 1][j - 1] += error * (1 / 8)

                        if new_data[i + 1][j - 1] > 1:
                            new_data[i + 1][j - 1] = 1
                        elif new_data[i + 1][j - 1] < 0:
                            new_data[i + 1][j - 1] = 0

                    new_data[i + 1][j] += error * (1 / 8)

                    if new_data[i + 1][j] > 1:
                        new_data[i + 1][j] = 1
                    elif new_data[i + 1][j] < 0:
                        new_data[i + 1][j] = 0

                    if j + 1 < len(new_data[i]):
                        new_data[i + 1][j + 1] += error * (1 / 8)

                        if new_data[i + 1][j + 1] > 1:
                            new_data[i + 1][j + 1] = 1
                        elif new_data[i + 1][j + 1] < 0:
                            new_data[i + 1][j + 1] = 0

                if i + 2 < len(new_data):
                    new_data[i + 2][j] += error * (1 / 8)

                    if new_data[i + 2][j] > 1:
                        new_data[i + 2][j] = 1
                    elif new_data[i + 2][j] < 0:
                        new_data[i + 2][j] = 0

        return np.array(new_data).astype(np.double)

    def floyd_steinberg(self, data: np.ndarray, byte: int = 8) -> np.ndarray:
        new_data = deepcopy(data)

        for i in range(len(new_data)):
            for j in range(len(new_data[i])):
                pixel = new_data[i][j]
                new_pixel = self.find_closest_color(pixel, byte)

                error = pixel - new_pixel

                new_data[i][j] = new_pixel

                if j + 1 < len(new_data[i]):
                    new_data[i][j + 1] += error * (7 / 16)

                    if new_data[i][j + 1] > 1:
                        new_data[i][j + 1] = 1
                    elif new_data[i][j + 1] < 0:
                        new_data[i][j + 1] = 0

                if i + 1 < len(new_data):
                    if j - 1 > 0:
                        new_data[i + 1][j - 1] += error * (3 / 16)

                        if new_data[i + 1][j - 1] > 1:
                            new_data[i + 1][j - 1] = 1
                        elif new_data[i + 1][j - 1] < 0:
                            new_data[i + 1][j - 1] = 0

                    new_data[i + 1][j] += error * (5 / 16)

                    if new_data[i + 1][j] > 1:
                        new_data[i + 1][j] = 1
                    elif new_data[i + 1][j] < 0:
                        new_data[i + 1][j] = 0

                    if j + 1 < len(new_data[i]):
                        new_data[i + 1][j + 1] += error * (1 / 16)

                        if new_data[i + 1][j + 1] > 1:
                            new_data[i + 1][j + 1] = 1
                        elif new_data[i + 1][j + 1] < 0:
                            new_data[i + 1][j + 1] = 0

        return np.array(new_data).astype(np.double)

    def find_closest_color(self, pixel, byte) -> float:
        bitness = self.bytes[byte - 1]
        left, right = 0, -1
        for k in range(len(bitness)):
            if (bitness[k] / 255) >= pixel:
                if k == 0:
                    left = right = bitness[k] / 255
                else:
                    left, right = bitness[k - 1] / 255, bitness[k] / 255
                break
        new_pixel = left if abs(left - pixel) < abs(right - pixel) else right
        return new_pixel


def test():
    manager = PgmManager()
    img_data = manager.read_p5("C:\\Users\\sword\\PycharmProjects\\cg22-project-Kikoriki\\lab1\\gradient.pgm")
    dith = Ditherer()
    img = Image.fromarray((dith.atkinson(img_data, 1) * 255).astype(np.uint8), "L")
    # img = Image.fromarray((np.array(img_data) * 255).astype(np.uint8))
    img.show()
