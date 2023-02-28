import cv2
import lockscreen_macos as Lock

# Inicializa la cámara web
cap = cv2.VideoCapture(0)

# Crea el detector de rostros
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Inicializa el contador de frames
frame_count = 0

while True:
    print(frame_count)
    # Lee un frame de la cámara
    ret, frame = cap.read()

    # Si el frame se ha leído correctamente, se procesa
    if ret:
        # Incrementa el contador de frames
        frame_count += 1

        # Detecta rostros en el frame actual
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)

        # Si no se detecta ningún rostro durante 10 frames consecutivos, se muestra un mensaje
        if len(faces) == 0:
            if frame_count >= 100:
                Lock.LockScreen.lockscreenMacOS()

        # Si se detecta al menos un rostro, se resetea el contador de frames
        else:
            frame_count = 0

    # Si se pulsa la tecla 'q', se sale del bucle y se termina la grabación
    if cv2.waitKey(1) == ord('q'):
        break
# Libera la cámara y cierra la ventana y el archivo de salida
cap.release()
cv2.destroyAllWindows()
