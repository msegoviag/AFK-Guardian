import time
import lockscreen as Lock
import os_detection as OSystem
from pynput import mouse, keyboard

class AFKdetector:

    def __init__(self):
        self.last_activity_time = time.time()

    def on_move(self, x, y):
        self.last_activity_time = time.time()

    def on_click(self, x, y, button, pressed):
        self.last_activity_time = time.time()

    def on_press(self, key):
        self.last_activity_time = time.time()

    def run(self):
        TIEMPO_INACTIVIDAD = 5  # segundos

        with mouse.Listener(on_move=self.on_move, on_click=self.on_click):
            with keyboard.Listener(on_press=self.on_press):
                while True:
                    # Calculamos el tiempo transcurrido desde la última actividad de los periféricos.
                    inactive_time = time.time() - self.last_activity_time
                    if inactive_time > TIEMPO_INACTIVIDAD:
                        print("Inactividad de pantalla detectada")
                        if (OSystem.sistema.nombre == "Windows"):
                            print("Inactividad")
                            Lock.LockScreen.lockcreenWindows()
                        elif (OSystem.sistema.nombre == "Darwin"):
                            Lock.LockScreen.lockscreenMacOS()
                        elif (OSystem.sistema.nombre == "Linux"):
                            Lock.LockScreen.lockscreenLinux()

                    time.sleep(1) # Esperamos 1 segundo antes de volver a comprobar la actividad

if __name__ == '__main__':
    detector = AFKdetector()
    detector.run()