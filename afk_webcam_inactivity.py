import sys
import cv2
import time
import lockscreen as Lock
import os_detection as OSystem

try:
    # Inicializa la cámara web
    cap = cv2.VideoCapture(0)

    if cap is None or not cap.isOpened():
       print('Warning: unable to open video source.')
       sys.exit(1)

    # Crea el detector de rostros
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    # Inicializa el contador de frames
    frame_count = 0

    # Establecer segundos que serán convertidos a frames (seconds * fps)
    seconds = 20
    fps = 25
    seconds_to_frames = seconds * fps

    while True:

        # Tras reanudar la suspensión comprobamos que la webcam no está activa y la reactivamos
        if cap is None or not cap.isOpened():
            frame_count = 0
            cap = cv2.VideoCapture(0)

        # Lee un frame de la cámara
        ret, frame = cap.read()

        # La cámara puede estar siendo usada por otra app, comprobamos conexión.
        if frame is None:
            print(
                "Error al iniciar la cámara, puede que esté en uso. Reintentando conexión")
            time.sleep(2)
            cap = cv2.VideoCapture(0)

        # Si el frame se ha leído correctamente se procesa
        if ret:
            # Incrementa el contador de frames
            frame_count += 1

        # Detecta rostros en el frame actual
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        eyes = eye_cascade.detectMultiScale(frame, 1.4, 6)

    # Si no se detecta ningún rostro durante 10 frames consecutivos, se muestra un mensaje
        faces_empty = len(faces) == 0
        eyes_empty = len(eyes) == 0

        if eyes_empty and faces_empty:
            if frame_count >= seconds_to_frames:

                if (OSystem.sistema.nombre == "Windows"):
                    Lock.LockScreen.lockscreen_windows()
                elif (OSystem.sistema.nombre == "Darwin"):
                    Lock.LockScreen.lockscreenMacOS()
                elif (OSystem.sistema.nombre == "Linux"):
                    Lock.LockScreen.lockscreenLinux()

    # Si se detecta al menos un rostro, se resetea el contador de frames
        else:
            print("Face Detected.")
            frame_count = 0
            time.sleep(1)

except cv2.error as e:
    print("Problem using OpenCV: {}".format(e))
    sys.exit(1)
