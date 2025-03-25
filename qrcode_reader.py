
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

from skimage.io import imshow

DATASET_PATH = 'dataset'

# imagem = '86417714.png'
imagem = '8054822.png'


caminho_imagem = os.path.join(DATASET_PATH, imagem)

imagem = Image.open(caminho_imagem)

imagem_pb = imagem.convert("L")

imagem_array = np.array(imagem_pb)


limiar = 128
imagem_bin = (imagem_array > limiar).astype(int)  # Converte para 1 (branco) e 0 (preto)

def encontrar_bbox(imagem_bin, tollerance=5):
    linhas, colunas = np.where(imagem_bin == 0)  # Pega as coordenadas dos pixels pretos

    if len(linhas) == 0 or len(colunas) == 0:
        return None

    # Determina os extremos da bounding box
    y_min, y_max = linhas.min(), linhas.max()
    x_min, x_max = colunas.min(), colunas.max()

    # Adicionando tolerância
    y_min, y_max = y_min - tollerance, y_max + tollerance
    x_min, x_max = x_min - tollerance, x_max + tollerance

    print(f'{y_min=}, {y_max=}, {x_min=}, {x_max=}')
    return (x_min, y_min, x_max, y_max)


bbox = encontrar_bbox(imagem_bin)

# Plotar a imagem original com a bounding box desenhada
fig, ax = plt.subplots()
ax.imshow(imagem, cmap="gray")
ax.grid(True)
if bbox:
    x_min, y_min, x_max, y_max = bbox
    rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(rect)

plt.axis("off")
plt.show()

def show_qrcode_detected(bbox):
    x_min, y_min, x_max, y_max = bbox
    return imagem_bin[y_min:y_max, x_min:x_max]

qrcode_detected = show_qrcode_detected(bbox)
plt.imshow(qrcode_detected, cmap="gray")
plt.show()



