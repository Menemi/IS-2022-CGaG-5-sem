from matplotlib import pyplot as plt
import numpy as np


class PgmManager:
    def __init__(self):
        self.data = None
        self.codec = None
        self.width = None
        self.height = None
        self.depth = None

    def read_p5(self, pgm_name):
        try:
            f = open(pgm_name, "rb")
            f.close()
        except FileNotFoundError:
            raise

        with open(pgm_name, "rb") as pgmf:
            codec = pgmf.readline()

            if codec != b"P5\n":
                raise Exception(f"Incorrect format of PGM: {codec}")

            width, height = list(map(int, pgmf.readline().split()))
            self.depth = int(pgmf.readline())
            assert self.depth <= 255

            raster = []
            for i in range(height):
                row = []
                for j in range(width):
                    row.append(ord(pgmf.read(1)))
                raster.append(row)

        self.height = height
        self.width = width
        self.data = (np.array(raster) / 255).astype(np.double)

        return self.data

    def save_p5(self, image_data, path_to_save):
        if len(image_data[0][0]) == 3:
            for row in image_data:
                for pixel in row:
                    if pixel[0] == pixel[1] == pixel[2] == 0:
                        print("well\n")
                        continue
                    else:
                        print("well well well")
                        if pixel[0] != 0:
                            self.data = np.array(image_data[:, :, 0] * 255).astype(np.uint8)
                        elif pixel[1] != 0:
                            self.data = np.array(image_data[:, :, 1] * 255).astype(np.uint8)
                        elif pixel[2] != 0:
                            self.data = np.array(image_data[:, :, 2] * 255).astype(np.uint8)
                        break
                break

        height, width, depth = str(len(self.data)), str(len(self.data[0])), str(np.amax(self.data))

        with open(path_to_save.split("\\")[-1], "wb+") as new_file:
            new_file.write(b"P5\n")
            new_file.write(width.encode())
            new_file.write(b" ")
            new_file.write(height.encode())
            new_file.write(b"\n")
            new_file.write(depth.encode())
            new_file.write(b"\n")

            for row in self.data:
                new_file.write(bytearray(row))

    def show_img(self):
        plt.imshow(self.data)
        plt.show()
