import pyautogui
import time
import cv2
import numpy as np
from PIL import Image

IDLE_TIMEOUT = 5

# Recorta las regiones correspondientes a la barra de tareas en la parte superior e inferior de las imágenes

def compare_screenshots(screenshot1, screenshot2):

    top_crop = 150  # ajusta este valor según la altura de tu barra de tareas en la parte superior
    # ajusta este valor según la altura de tu barra de tareas en la parte inferior
    bottom_crop = 200
    screenshot1 = screenshot1.crop(
        (0, top_crop, screenshot1.width, screenshot1.height - bottom_crop))
    screenshot2 = screenshot2.crop(
        (0, top_crop, screenshot2.width, screenshot2.height - bottom_crop))

    # Convierte las imágenes a formato numpy array
    screenshot1 = np.array(screenshot1)
    screenshot2 = np.array(screenshot2)

    # Aplica la función cv2.absdiff() a las dos imágenes
    result = cv2.absdiff(screenshot1, screenshot2)

    # Compara la imagen resultante y devuelve True si las imágenes son iguales, False en caso contrario
    return result.sum() == 0


# Toma una captura de pantalla inicial
screenshot1 = pyautogui.screenshot()

while True:
    # Toma segunda captura de pantalla
    screenshot2 = pyautogui.screenshot()

    # Compara las dos capturas de pantalla
    if compare_screenshots(screenshot1, screenshot2):
        print("Las capturas de pantalla son iguales")
    else:
        print("Las capturas de pantalla son diferentes")

    # Actualiza la captura de pantalla inicial
    screenshot1 = screenshot2

    time.sleep(IDLE_TIMEOUT)
