import cv2 as cv
import dlib 
import numpy as np
from imutils import face_utils
import math

#####################################################
def distance(p1,p2):
    (x1,y1) = p1
    (x2,y2) = p2
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist  

#####################################################
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/mohsencactus/Opencv/digit/opencv7_material/shape_predictor_68_face_landmarks.dat")
webcam = cv.VideoCapture(0)
img = cv.imread("/home/mohsencactus/Opencv/digit/opencv7_material/pignose.png")
a = 10
b = 10
#####################################################
while True:
    frame = webcam.read()[1]
    blank = np.zeros_like(frame)
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

#####################################################
    faces = detector(gray,1)    
    for face in faces:
        fpoints = predictor(gray,face)
        fpoints = face_utils.shape_to_np(fpoints)
        #for (x,y) in fpoints:
        #    cv.circle(frame,(x,y),3,(255,0,0),-1)

#####################################################
        target = fpoints[27:36]
        height = int(distance(target[1],target[6]))+(b*2)
        width = int(distance(target[4],target[8]))+(a*2)
        #for (x,y) in target:
        #    cv.circle(frame,(x,y),3,(255,255,0),-1)

#####################################################
        img = cv.resize(img,(width,height))
        imggray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        #binar = cv.inRange(imggray, 0, 90)
        binar = cv.threshold(imggray, 25, 255, cv.THRESH_BINARY_INV)[1]
        #binar = cv.bitwise_not(binar)

#####################################################
        noseroi = frame[target[1][1]-b:target[6][1]+b,target[4][0]-a:target[8][0]+a]
        roiwithnose = cv.bitwise_and(noseroi, noseroi, mask=binar)
        #fillednose = cv.bitwise_and(img,img,mask=binar)
        fillednose = cv.add(roiwithnose, img)
        frame[target[1][1]-b:target[6][1]+b,target[4][0]-a:target[8][0]+a] = fillednose

#####################################################
    cv.imshow("frame",frame)
    if cv.waitKey(1) == ord("q"):
        cv.destroyAllWindows()
        break
    