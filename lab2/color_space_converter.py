from PIL import Image, ImageTk

from lab1.managers.ppm_manager import PpmManager
import numpy as np


class ColorSpaceConverter:
    @staticmethod
    def rgb_to_hsl(data: np.ndarray) -> np.ndarray:
        hsl_data = []
        for row in data:
            hsl_row = []
            for rgb in row:
                r, g, b = rgb[0], rgb[1], rgb[2]

                c_max = max(r, g, b)
                c_min = min(r, g, b)
                delta = c_max - c_min

                h = None
                if delta == 0:
                    h = 0
                elif c_max == r:
                    h = 60 * (((g - b) / delta) % 6)
                elif c_max == g:
                    h = 60 * (((b - r) / delta) + 2)
                elif c_max == b:
                    h = 60 * (((r - g) / delta) + 4)

                l = (c_max + c_min) / 2

                if delta == 0:
                    s = 0
                else:
                    s = delta / (1 - abs(2 * l - 1))

                hsl_row.append([h, s, l])

            hsl_data.append(hsl_row)

        return (np.array(hsl_data)).astype(np.double)

    @staticmethod
    def hsl_to_rgb(data: np.ndarray) -> np.ndarray:
        rgb_data = []
        for row in data:
            rgb_row = []

            for hsl in row:
                h, s, l = hsl[0], hsl[1], hsl[2]

                c = (1 - abs(2 * l - 1)) * s
                x = c * (1 - abs(((h / 60) % 2) - 1))
                m = l - c / 2

                r_, g_, b_ = 0, 0, 0
                if 0 <= h < 60:
                    r_, g_, b_ = c, x, 0
                elif 60 <= h < 120:
                    r_, g_, b_ = x, c, 0
                elif 120 <= h < 180:
                    r_, g_, b_ = 0, c, x
                elif 180 <= h < 240:
                    r_, g_, b_ = 0, x, c
                elif 240 <= h < 300:
                    r_, g_, b_ = x, 0, c
                elif 300 <= h < 360:
                    r_, g_, b_ = c, 0, x

                r, g, b = (r_ + m), (g_ + m), (b_ + m)

                rgb_row.append([r, g, b])

            rgb_data.append(rgb_row)

        return (np.array(rgb_data)).astype(np.double)

    @staticmethod
    def rgb_to_hsv(data: np.ndarray) -> np.ndarray:
        hsv_data = []
        for row in data:
            hsv_row = []
            for rgb in row:
                r, g, b = rgb[0], rgb[1], rgb[2]

                maximum, minimum = max(r, g, b), min(r, g, b)
                delta = maximum - minimum

                if delta == 0:
                    h = 0
                elif maximum == r:
                    h = 60 * (((g - b) / delta) % 6)
                elif maximum == g:
                    h = 60 * (((b - r) / delta) + 2)
                else:
                    h = 60 * (((r - g) / delta) + 4)

                if maximum == 0:
                    s = 0
                else:
                    s = delta / maximum

                v = maximum

                hsv_row.append([h, s, v])

            hsv_data.append(hsv_row)

        return (np.array(hsv_data)).astype(np.double)

    @staticmethod
    def hsv_to_rgb(data: np.ndarray) -> np.ndarray:
        rgb_data = []
        for row in data:
            rgb_row = []

            for hsv in row:
                h, s, v = hsv[0], hsv[1], hsv[2]

                C = v * s
                X = C * (1 - abs(((h / 60) % 2) - 1))
                m = v - C

                r_, g_, b_ = 0, 0, 0
                if 0 <= h < 60:
                    r_, g_, b_ = C, X, 0
                elif 60 <= h < 120:
                    r_, g_, b_ = X, C, 0
                elif 120 <= h < 180:
                    r_, g_, b_ = 0, C, X
                elif 180 <= h < 240:
                    r_, g_, b_ = 0, X, C
                elif 240 <= h < 300:
                    r_, g_, b_ = X, 0, C
                elif 300 <= h < 630:
                    r_, g_, b_ = C, 0, X

                rgb_row.append([r_ + m, g_ + m, b_ + m])

            rgb_data.append(rgb_row)

        return (np.array(rgb_data)).astype(np.double)

    @staticmethod
    def rgb_to_cmyk(data: np.ndarray) -> np.ndarray:
        cmy_data = []
        for row in data:
            cmy_row = []
            for rgb in row:
                r, g, b = rgb[0], rgb[1], rgb[2]

                k = 1 - max(r, g, b)
                if k != 1:
                    c = (1 - r - k) / (1 - k)
                    m = (1 - g - k) / (1 - k)
                    y = (1 - b - k) / (1 - k)
                else:
                    c, m, y = 0, 0, 0
                cmy_row.append([c, m, y, k])

            cmy_data.append(cmy_row)

        return (np.array(cmy_data)).astype(np.double)

    @staticmethod
    def cmyk_to_rgb(data: np.ndarray) -> np.ndarray:
        rgb_data = []
        for row in data:
            rgb_row = []
            for cmyk in row:
                c, m, y, k = cmyk[0], cmyk[1], cmyk[2], cmyk[3]

                r = (1 - c) * (1 - k)
                g = (1 - m) * (1 - k)
                b = (1 - y) * (1 - k)

                rgb_row.append([r, g, b])

            rgb_data.append(rgb_row)

        return (np.array(rgb_data)).astype(np.double)

    @staticmethod
    def rgb_to_ycocg(data: np.ndarray) -> np.ndarray:
        ycocg_data = []
        for row in data:
            ycocg_row = []
            for rgb in row:
                r, g, b = rgb[0], rgb[1], rgb[2]

                y = 1 / 4 * r + 1 / 2 * g + 1 / 4 * b
                c_o = 1 / 2 * r - 1 / 2 * b
                c_g = - 1 / 4 * r + 1 / 2 * g - 1 / 4 * b

                ycocg_row.append([y, c_o, c_g])

            ycocg_data.append(ycocg_row)

        return (np.array(ycocg_data)).astype(np.double)

    @staticmethod
    def ycocg_to_rgb(data: np.ndarray) -> np.ndarray:
        rgb_data = []
        for row in data:
            rgb_row = []
            for ycocg in row:
                y, c_o, c_g = ycocg[0], ycocg[1], ycocg[2]

                r = y + c_o - c_g
                g = y + c_g
                b = y - c_o - c_g

                rgb_row.append([r, g, b])

            rgb_data.append(rgb_row)

        return (np.array(rgb_data)).astype(np.double)

    @staticmethod
    def rgb_to_ycbcr(data: np.ndarray, standard: int) -> np.ndarray:
        ycbcr_data = []
        for row in data:
            ycbcr_row = []
            for rgb in row:
                a, b, c, d, e = 1, 1, 1, 1, 1
                R, G, B = rgb[0], rgb[1], rgb[2]
                if standard == 601:
                    a, b, c, d, e = .299, .587, .114, 1.772, 1.402
                elif standard == 709:
                    a, b, c, d, e = .2126, .7152, .0722, 1.8556, 1.5748

                y_ = a * R + b * G + c * B
                c_r = (R - y_) / e
                c_b = (B - y_) / d

                ycbcr_row.append([y_, c_b, c_r])

            ycbcr_data.append(ycbcr_row)

        return (np.array(ycbcr_data)).astype(np.double)

    @staticmethod
    def ycbcr_to_rgb(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = []
        for row in data:
            rgb_row = []
            for ycbcr in row:
                a, b, c, d, e = 1, 1, 1, 1, 1
                y_, c_b, c_r = ycbcr[0], ycbcr[1], ycbcr[2]
                if standard == 601:
                    a, b, c, d, e = .299, .587, .114, 1.772, 1.402
                elif standard == 709:
                    a, b, c, d, e = .2126, .7152, .0722, 1.8556, 1.5748

                R = y_ + e * c_r
                G = y_ - (a * e / b) * c_r - (c * d / b) * c_b
                B = y_ + d * c_b

                rgb_row.append([R, G, B])

            rgb_data.append(rgb_row)

        return (np.array(rgb_data)).astype(np.double)

    @staticmethod
    def hsl_to_hsv(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.hsl_to_rgb(data)
        return ColorSpaceConverter.rgb_to_hsv(rgb_data)

    @staticmethod
    def hsv_to_hsl(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.hsv_to_rgb(data)
        return ColorSpaceConverter.rgb_to_hsl(rgb_data)

    @staticmethod
    def hsl_to_ycbcr(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = ColorSpaceConverter.hsl_to_rgb(data)
        return ColorSpaceConverter.rgb_to_ycbcr(rgb_data, standard)

    @staticmethod
    def ycbcr_to_hsl(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycbcr_to_rgb(data, standard)
        return ColorSpaceConverter.rgb_to_hsl(rgb_data)

    @staticmethod
    def hsl_to_ycocg(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.hsl_to_rgb(data)
        return ColorSpaceConverter.rgb_to_ycocg(rgb_data)

    @staticmethod
    def ycocg_to_hsl(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycocg_to_rgb(data)
        return ColorSpaceConverter.rgb_to_hsl(rgb_data)

    @staticmethod
    def hsl_to_cmyk(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.hsl_to_rgb(data)
        return ColorSpaceConverter.rgb_to_cmyk(rgb_data)

    @staticmethod
    def cmyk_to_hsl(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.cmyk_to_rgb(data)
        return ColorSpaceConverter.rgb_to_hsl(rgb_data)

    @staticmethod
    def hsv_to_ycbcr(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = ColorSpaceConverter.hsv_to_rgb(data)
        return ColorSpaceConverter.rgb_to_ycbcr(rgb_data, standard)

    @staticmethod
    def ycbcr_to_hsv(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycbcr_to_rgb(data, standard)
        return ColorSpaceConverter.rgb_to_hsv(rgb_data)

    @staticmethod
    def hsv_to_ycocg(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.hsv_to_rgb(data)
        return ColorSpaceConverter.rgb_to_ycocg(rgb_data)

    @staticmethod
    def ycocg_to_hsv(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycocg_to_rgb(data)
        return ColorSpaceConverter.rgb_to_hsv(rgb_data)

    @staticmethod
    def hsv_to_cmyk(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.hsv_to_rgb(data)
        return ColorSpaceConverter.rgb_to_cmyk(rgb_data)

    @staticmethod
    def cmyk_to_hsv(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.cmyk_to_rgb(data)
        return ColorSpaceConverter.rgb_to_hsv(rgb_data)

    @staticmethod
    def ycbcr_601_to_709(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycbcr_to_rgb(data, standard=601)
        return ColorSpaceConverter.rgb_to_ycbcr(rgb_data, standard=709)

    @staticmethod
    def ycbcr_709_to_601(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycbcr_to_rgb(data, standard=709)
        return ColorSpaceConverter.rgb_to_ycbcr(rgb_data, standard=601)

    @staticmethod
    def ycbcr_to_ycocg(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycbcr_to_rgb(data, standard)
        return ColorSpaceConverter.rgb_to_ycocg(rgb_data)

    @staticmethod
    def ycocg_to_ycbcr(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycocg_to_rgb(data)
        return ColorSpaceConverter.rgb_to_ycbcr(rgb_data, standard)

    @staticmethod
    def ycbcr_to_cmyk(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycbcr_to_rgb(data, standard)
        return ColorSpaceConverter.rgb_to_cmyk(rgb_data)

    @staticmethod
    def cmyk_to_ycbcr(data: np.ndarray, standard: int) -> np.ndarray:
        rgb_data = ColorSpaceConverter.cmyk_to_rgb(data)
        return ColorSpaceConverter.rgb_to_ycbcr(rgb_data, standard)

    @staticmethod
    def ycocg_to_cmyk(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.ycocg_to_rgb(data)
        return ColorSpaceConverter.rgb_to_cmyk(rgb_data)

    @staticmethod
    def cmyk_to_ycocg(data: np.ndarray) -> np.ndarray:
        rgb_data = ColorSpaceConverter.cmyk_to_rgb(data)
        return ColorSpaceConverter.rgb_to_ycocg(rgb_data)


def test():
    manager = PpmManager()
    img_data = manager.read_p6("C:\\Users\\sword\\PycharmProjects\\cg22-project-Kikoriki\\lab1\\bell_206.ppm")
    # hsl_data = ColorSpaceConverter.rgb_to_hsl(img_data)
    # img = Image.fromarray((hsl_data*255).astype(np.uint8))
    img = Image.fromarray(img_data.astype(np.uint8))
    img.show()
