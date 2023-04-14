import os
import cv2
import imutils
import argparse
import numpy as np
from keras_facenet import FaceNet

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())

number = 0
frame_count = 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

embedder = FaceNet()

print("Enter your name: ")
name = input()
folder_name = "dataset/" + name

if os.path.exists(folder_name):
    print("Folder exists")
else:
    os.mkdir(folder_name)

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

while True:
    if frame_count % 5 == 0:
        print("keyframe")
        (grabbed, image) = camera.read()
        if args.get("video") and not grabbed:
            break

        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in rects:
            roi = image[y:y + h, x:x + w]
            face_encodings = embedder.embeddings([roi])
            out_image = cv2.resize(roi, (108, 108))
            fram = os.path.join(folder_name + "/", str(number) + "." + "jpg")
            number += 1
            cv2.imwrite(fram, out_image)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        frame_count += 1
    else:
        frame_count += 1
        print("redundant frame")

    if number > 101:
        break

    cv2.imshow("output image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
