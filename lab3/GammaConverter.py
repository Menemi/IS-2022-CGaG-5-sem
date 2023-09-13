import numpy as np
from exceptions import IncorrectGammaError
from copy import deepcopy


class GammaConverter:
    def __init__(self, data: np.ndarray):
        self.data = data
        self.gamma = 0
        self.data_with_gamma = None

    def convert(self, gamma: str):
        try:
            new_gamma = float(gamma)
        except ValueError:
            raise IncorrectGammaError

        if new_gamma < 0.0:
            raise IncorrectGammaError
        elif new_gamma == 0.0:
            self.data_with_gamma = deepcopy(self.data)
            for i in range(len(self.data_with_gamma)):
                for j in range(len(self.data_with_gamma[0])):

                    if not isinstance(self.data[0][0], np.double):
                        for k in range(3):
                            pixel = self.data_with_gamma[i][j][k]

                            self.data_with_gamma[i][j][k] = 12.92 * pixel if pixel <= 0.0031308 else (1 + 0.055) * (
                                    pixel ** 1 / 2.4) - 0.055

                    else:
                        pixel = self.data_with_gamma[i][j]

                        self.data_with_gamma[i][j] = 12.92 * pixel if pixel <= 0.0031308 else (1 + 0.055) * (
                                pixel ** 1 / 2.4) - 0.055

        else:
            self.data_with_gamma = self.data ** new_gamma

        self.gamma = new_gamma
