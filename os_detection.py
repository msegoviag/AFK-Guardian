import platform

class SistemaOperativo:
    def __init__(self):
        self.nombre = platform.system()
        self.version = platform.release()

    def mostrar_info(self):
        print(f"Sistema operativo: {self.nombre}")
        print(f"Versión: {self.version}")

sistema = SistemaOperativo()