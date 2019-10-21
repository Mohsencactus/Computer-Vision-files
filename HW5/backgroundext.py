import numpy as np
import cv2 as cv

webcam = cv.VideoCapture(0)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
fgbg = cv.createBackgroundSubtractorMOG2()

while True:
    _,frame = webcam.read()

    fgmask = fgbg.apply(frame)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

    cv.imshow('frame',fgmask)
    if ord("q") == cv.waitKey(1):
        webcam.release()
        cv.destroyAllWindows()
        break

