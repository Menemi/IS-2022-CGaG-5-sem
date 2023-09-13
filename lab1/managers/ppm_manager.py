from matplotlib import pyplot as plt
import numpy as np

class PpmManager:
    def __init__(self):
        self.data = None
        self.codec = None
        self.width = None
        self.height = None
        self.depth = None

    def read_p6(self, ppm_name):
        try:
            f = open(ppm_name, "rb")
            f.close()
        except FileNotFoundError:
            raise

        with open(ppm_name, 'rb') as ppmf:
            codec = ppmf.readline()

            if codec != b'P6\n' and codec != b'P6\r\n':
                raise Exception(f"Incorrect format of PPM: {codec}")

            width, height = list(map(int, ppmf.readline().split()))
            self.depth = int(ppmf.readline())
            assert self.depth <= 255

            raster = []
            for i in range(height):
                row = []
                for j in range(width):
                    rgb = []
                    for k in range(3):
                        rgb.append(ord(ppmf.read(1)))
                    row.append(np.array(rgb))
                raster.append(np.array(row))

        self.height = height
        self.width = width
        self.data = (np.array(raster) / 255).astype(np.double)

        return self.data

    def save_p6(self, image_data, path_to_save):
        file_data = (image_data * 255).astype(np.uint8)
        height, width, depth = str(self.height), str(self.width), str(self.depth)

        with open(path_to_save.split("\\")[-1], "wb+") as new_file:
            new_file.write(b"P6\n")
            new_file.write(width.encode())
            new_file.write(b" ")
            new_file.write(height.encode())
            new_file.write(b"\n")
            new_file.write(depth.encode())
            new_file.write(b"\n")

            for row in file_data:
                for rgb in row:
                    new_file.write(bytearray(rgb))

    def show_img(self):
        plt.imshow(self.data)
        plt.show()
