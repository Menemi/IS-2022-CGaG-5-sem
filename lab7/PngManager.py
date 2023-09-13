from struct import pack
import zlib
from math import floor
import numpy as np
from PIL import Image


def paeth_predictor(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        Pr = a
    elif pb <= pc:
        Pr = b
    else:
        Pr = c
    return Pr


def get_a(data, row_number, pix_number, width, bytes_per_pixel):
    if pix_number < bytes_per_pixel:
        return 0
    else:
        return data[row_number * width * bytes_per_pixel + pix_number - bytes_per_pixel]


def get_b(data, row_number, pix_number, width, bytes_per_pixel):
    if row_number == 0:
        return 0
    else:
        return data[(row_number - 1) * width * bytes_per_pixel + pix_number]


def get_c(data, row_number, pix_number, width, bytes_per_pixel):
    if pix_number < bytes_per_pixel or row_number == 0:
        return 0
    else:
        return data[(row_number - 1) * width * bytes_per_pixel + pix_number - bytes_per_pixel]


def filter_pixel(filter_type, data, x, row_number, pix_number, width, bytes_per_pixel):
    pix_number -= 1
    args = data, row_number, pix_number, width, bytes_per_pixel

    if filter_type == 0:
        return x

    elif filter_type == 1:
        return x + get_a(*args)

    elif filter_type == 2:
        return x + get_b(*args)

    elif filter_type == 3:
        a = get_a(*args)
        b = get_b(*args)

        return x + floor((a + b) / 2)

    elif filter_type == 4:
        a = get_a(*args)
        b = get_b(*args)
        c = get_c(*args)
        return x + paeth_predictor(a, b, c)

    else:
        raise TypeError


class PngManager:
    def __init__(self):
        self.data = []
        self.color_type = None
        self.bytes_per_pixel = None
        self.chunks = []
        self.plte_data = []
        self.gamma = 1

    def read(self, png_name):
        png_name = "../lab1/" + png_name
        try:
            f = open(png_name, "rb")
            f.close()
        except FileNotFoundError:
            raise

        with open(png_name, "rb") as f:
            header = f.read(8)

            assert header == b'\x89PNG\r\n\x1a\n'

            while True:
                chunk_len = int.from_bytes(f.read(4), "big")
                chunk_name = f.read(4)
                chunk_data = f.read(chunk_len)
                chunk_crc = f.read(4)

                self.chunks.append((chunk_len, chunk_name, chunk_data, chunk_crc))

                if chunk_name == b'IEND':
                    break

            IHDR = self.chunks[0][2]

            width, height = int.from_bytes(IHDR[:4], "big"), int.from_bytes(IHDR[4:8], "big")
            depth = IHDR[8]
            self.color_type = IHDR[9]
            compression = IHDR[10]
            filtration = IHDR[11]
            interlace = IHDR[12]

            assert self.color_type in (0, 2, 3)
            assert depth == 8
            assert compression == 0
            assert filtration == 0
            assert interlace == 0

            if self.color_type == 0:
                self.bytes_per_pixel = 1

            elif self.color_type == 2:
                self.bytes_per_pixel = 3

            elif self.color_type == 3:
                self.bytes_per_pixel = 1
                for chunk in self.chunks:
                    if chunk[1] == b'PLTE':
                        PLTE = chunk[2]
                        break

                for i in range(0, len(PLTE), 3):
                    self.plte_data.append((PLTE[i], PLTE[i + 1], PLTE[i + 2]))

            IDAT = b''.join(chunk_data for _, chunk_name, chunk_data, _ in self.chunks if chunk_name == b'IDAT')
            decompressed = zlib.decompress(IDAT)

            row_step = width * self.bytes_per_pixel + 1

            for row_number in range(height):
                filter_type = decompressed[row_number * row_step]
                for pix_number in range(1, row_step):
                    x = decompressed[row_number * row_step + pix_number]

                    filtered = filter_pixel(filter_type, self.data, x, row_number, pix_number, width, self.bytes_per_pixel)

                    self.data.append(filtered & 0xff)

            if self.color_type == 0:
                data = []
                for i in range(len(self.data)):
                    for j in range(3):
                        data.append(self.data[i])
                self.data = data

            elif self.color_type == 3:
                temp = []
                for color_index in self.data:
                    temp.append(self.plte_data[color_index])
                self.data = temp

            self.data = np.array(self.data) / 255

            for _, chunk_name, chunk_data, _ in self.chunks:
                if chunk_name == b'gAMA':
                    self.gamma = int.from_bytes(chunk_data, "big") / 100000
                    break
            self.data = (self.data ** self.gamma)

            self.data = self.data.reshape((height, width, 3)).astype(np.double)

        return self.data

    def save(self, data, path):
        path = "../lab1/" + path
        png_signature = b'\x89PNG\r\n\x1a\n'
        try:
            f = open(path, "wb")
            f.close()
        except FileNotFoundError:
            raise

        filtered_data = []
        ravel_data = data.ravel()
        width = len(data[0]) * 3
        for i in range(len(ravel_data)):
            if i % width == 0:
                filtered_data.append(0)
            filtered_data.append(ravel_data[i])

        with open(path, "wb") as f:
            f.write(png_signature)

            f.write(pack(">I", 13))
            f.write(b"IHDR")
            f.write(pack(">IIBBBBB", len(data[0]), len(data), 8, self.color_type, 0, 0, 0))
            f.write(
                pack(">I", zlib.crc32(pack(">BBBBB", 8, self.color_type, 0, 0, 0), zlib.crc32(pack(">4s", b"IHDR")))))

            f.write(pack(">I", 4))
            f.write(b"gAMA")
            f.write(pack(">I", int(self.gamma * 100000)))
            f.write(
                pack(">I", zlib.crc32(pack(">I", int(self.gamma * 100000)), zlib.crc32(pack(">4s", b"gAMA")))))

            compressed = zlib.compress(bytes(filtered_data))

            print(len(compressed))

            print(len(zlib.decompress(compressed)))
            f.write(pack(">I", len(compressed)))
            f.write(b"IDAT")
            f.write(compressed)
            f.write(
                pack(">I", zlib.crc32(compressed, zlib.crc32(pack(">4s", b"IDAT")))))

            f.write(pack(">I", 0))
            f.write(b"IEND")
            f.write(
                pack(">I", zlib.crc32(pack(">4s", b"IDAT"))))



def test_save():
    manager = PngManager()
    img = manager.read("small_h_1.png")
    manager.save((img * 255).astype(np.uint8), "small_h_2.png")
    pillow = Image.fromarray((img * 255).astype(np.uint8))
    pillow.show()


def test_read_sved():
    manager = PngManager()
    img = manager.read("small_h_2.png")
    pillow = Image.fromarray((img * 255).astype(np.uint8))
    pillow.show()

def test():
    manager = PngManager()
    img = manager.read("basn0g08.png")
    pillow = Image.fromarray((img * 255).astype(np.uint8))
    pillow.show()