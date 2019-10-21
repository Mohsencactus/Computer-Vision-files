import cv2 as cv
import dlib 
import imutils
from imutils import face_utils

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/mohsencactus/Opencv/digit/opencv7_material/shape_predictor_68_face_landmarks.dat")

webcam = cv.VideoCapture(0)
img = cv.imread("/home/mohsencactus/Opencv/digit/opencv7_material/osol.jpg")
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

rects = detector(gray,1)

for rect in rects:
    (x1,y1) = (rect.left(),rect.top())
    (x2,y2) = (rect.right(),rect.bottom())
    cv.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)

    shape = predictor(gray,rect)
    shape = face_utils.shape_to_np(shape)

for (x,y) in shape:
    cv.circle(img,(x,y),3,(255,0,255),-1)

cv.imshow("frame",img)
cv.waitKey(0)