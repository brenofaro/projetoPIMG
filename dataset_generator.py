import math
import skimage as sk
import random
import numpy as np
import qrcode
import os
from PIL import Image


def rotate_matrix(theta):
    theta = np.deg2rad(theta)
    c = math.cos(theta)
    s = math.sin(theta)
    matriz = np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ], dtype=float)
    return matriz

def rotacao(img, theta, cval=255):
    altura, largura = img.shape[:2]

    saida = np.ones_like(img) * cval # Imagem com a cor de fundo branco

    cx, cy = largura / 2, altura / 2

    Matriz = rotate_matrix(theta)

    M_inv = np.linalg.inv(Matriz)

    for y_nova in range(altura):
        for x_nova in range(largura):

            xy_saida = np.array([x_nova - cx, y_nova - cy, 1]) # Colocando a origem para o centro da imagem

            xy_entrada = M_inv @ xy_saida # Aplicando a matriz inversa na imagem de saída

            x_entrada, y_entrada = xy_entrada[0] + cx, xy_entrada[1] + cy # Voltando a origem para o canto superior esquerdo

            x_entrada = int(round(x_entrada))
            y_entrada = int(round(y_entrada))

            if 0 <= x_entrada < largura and 0 <= y_entrada < altura:
                saida[y_nova,x_nova] = img[y_entrada, x_entrada]

    return saida


def translate_image(img, canvas_size, dx, dy, fill=(255, 255, 255)):
    canvas = Image.new("RGBA", canvas_size, fill + (255,))
    canvas.paste(img, (dx, dy), img if img.mode == 'RGBA' else None)
    return canvas


def generate_qrcode(data, angle=0, size=1, dx=0, dy=0, canvas_size=(1400, 1400)):
    qr = qrcode.QRCode(
        version=size,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    if dx or dy:
        img = translate_image(img, canvas_size, dx, dy)
    img = np.array(img)
    if angle:
        # img = rotate(img, angle, cval=255, reshape=False)
        img = rotacao(img, angle)

    return img


def generate_dataset(directory, quantity, canvas_size):
    for i in range(quantity):
        random_angle = random.randint(0, 360)
        random_size = random.randint(1, 5)
        dx, dy = random.randint(1, 500), random.randint(1, 500)
        data = random.randint(1000, 99999999)
        filename = f"{data}.png"
        path = os.path.join(directory, filename)

        qr = generate_qrcode(data, random_angle, random_size, dx, dy, canvas_size)
        sk.io.imsave(path, qr)


DATASET_PATH = 'dataset2'
CANVAS_SIZE = (1000, 1000)

generate_dataset(DATASET_PATH, 1, CANVAS_SIZE)