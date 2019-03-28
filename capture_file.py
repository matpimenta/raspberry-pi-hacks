#!/usr/bin/env python
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("error")

print('Reading...')
return_value, image = cap.read()

if return_value:
    filename = 'opencv.jpg'
    print('Writing image: ' + filename)
    cv2.imwrite(filename, image)
else:
    print('Failure to capture snapshot')

del cap
