import pyautogui


class CursorDetector:

    def exec():

        TIEMPO_INACTIVIDAD = 5  # segundos

        # Obtenemos la posición actual del cursor
        posicion_actual = pyautogui.position()

        while True:
            # Esperamos a que el cursor se mueva
            pyautogui.sleep(TIEMPO_INACTIVIDAD)

        # Obtenemos la nueva posición del cursor
            nueva_posicion = pyautogui.position()

            # Si la posición es la misma, se considera inactividad de pantalla
            if nueva_posicion == posicion_actual:
                print("Inactividad de pantalla detectada")
            else:
                # Si la posición del puntero cambió, actualizamos la posición actual del cursor
             posicion_actual = nueva_posicion


if __name__ == '__main__':
    CursorDetector.exec()
