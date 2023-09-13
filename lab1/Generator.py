header = b"P5\n765 400\n 255\n" # width height
data = []
for i in range(400):
    for j in range(255):
        row = []
        for _ in range(3):
            row.append(j)
        data.append(row)

with open("gradient.pgm", "wb") as f:
    f.write(header)
    for row in data:
        f.write(bytearray(row))