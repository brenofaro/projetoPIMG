import skimage
import skimage as sk
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate
import qrcode
import os
from PIL import Image

DATASET_PATH = 'dataset'

def translate_image(img, canvas_size, dx, dy, fill=(255, 255, 255)):
    canvas = Image.new("RGBA", canvas_size, fill + (255,))
    canvas.paste(img, (dx, dy), img if img.mode == 'RGBA' else None)
    return canvas


def generate_qrcode(data, angle=0, size=1, dx=0, dy=0):
    qr = qrcode.QRCode(
        version=size,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img = translate_image(img, (1400, 1400), dx, dy)
    img = np.array(img)
    if angle:
        img = rotate(img, angle, cval=255)

    return img


def generate_dataset(directory, quantity):
    for i in range(quantity):
        random_angle = random.randint(0, 360)
        random_size = random.randint(1, 5)
        dx, dy = random.randint(1,500), random.randint(1,500)
        data = random.randint(1000,99999999)
        filename = f"{data}.png"
        path = os.path.join(directory, filename)

        qr = generate_qrcode(data, random_angle, random_size, dx, dy)
        sk.io.imsave(path, qr)


generate_dataset(DATASET_PATH, 10)





