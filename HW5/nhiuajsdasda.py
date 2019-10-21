import cv2 as cv
import dlib 
import imutils
from imutils import face_utils

detector = dlib.get_frontal_face_detector()
perdictor = dlib.shape_predictor("shape_perdictor")

img = cv.imread()
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

rec = detector(gray,1)