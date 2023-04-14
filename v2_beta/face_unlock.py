import ctypes
import numpy as np
import argparse
import cv2
import pickle
import os
import time
from keras_facenet import FaceNet

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())

with open("trained_knn_model.clf", 'rb') as f:
    knn_clf = pickle.load(f)

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the FaceNet embedder
embedder = FaceNet()

last_seen_time = time.time()
lock_timeout = 10
face_detected = False

while True:
    (grabbed, image1) = camera.read()
    if args.get("video") and not grabbed:
        break

    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        face_detected = False
    else:
        for (x, y, w, h) in faces:
            roi = image1[y:y + h, x:x + w]
            face_encodings = embedder.embeddings([roi])

            closest_distances = knn_clf.kneighbors(
                face_encodings, n_neighbors=1)
            are_matches = [closest_distances[0][i][0]
                           <= 0.6 for i in range(len(faces))]
            predictions = [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(
                knn_clf.predict(face_encodings), [(x, y, x + w, y + h)], are_matches)]

            for name, (left, top, right, bottom) in predictions:
                cv2.rectangle(image1, (left, top),
                              (right, bottom), (0, 255, 0), 2)
                cv2.putText(image1, "{}".format(name), (left - 10, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if name != "unknown":
                    print("Unlock!")
                    face_detected = True
                    last_seen_time = time.time()
                else:
                    print("Block!")
                    face_detected = False

    cv2.imshow("output image", image1)

    if not face_detected and (time.time() - last_seen_time) > lock_timeout:
        ctypes.windll.user32.LockWorkStation()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
