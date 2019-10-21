import cv2 as cv
import numpy as np 
import math
import time
###########################################
def nthn(X):
    pass
###########################################
video = cv.VideoCapture(1)
cv.namedWindow("window2",cv.WINDOW_NORMAL)
###########################################
cv.createTrackbar("Hmin","window2",0,255,nthn)
cv.createTrackbar("Hmax","window2",0,180,nthn)
cv.createTrackbar("Smin","window2",0,255,nthn)
cv.createTrackbar("Smax","window2",0,255,nthn)
cv.createTrackbar("Vmin","window2",0,255,nthn)
cv.createTrackbar("Vmax","window2",0,255,nthn)
cv.createTrackbar('blur',"window2",0,4,nthn)
cv.setTrackbarPos("Hmax","window2",180)
cv.setTrackbarPos("Smax","window2",255)
cv.setTrackbarPos("Vmax","window2",255)
###########################################
_,frame = video.read()
yframe = len(frame)
xframe = len(frame[1])
###########################################
while True:
###########################################
    _,frame = video.read()
###########################################
    Hmin = cv.getTrackbarPos("Hmin","window2")
    Smin = cv.getTrackbarPos("Smin","window2")
    Vmin = cv.getTrackbarPos("Vmin","window2")
    Hmax = cv.getTrackbarPos("Hmax","window2")
    Smax = cv.getTrackbarPos("Smax","window2")
    Vmax = cv.getTrackbarPos("Vmax","window2")
    Blur = 3#cv.getTrackbarPos('blur',"window2")
###########################################
    if (Blur == 1):
        frame = cv.bilateralFilter(frame,9,75,75)
    elif(Blur == 2):
        frame = cv.blur(frame,(5,5))
    elif(Blur == 3):
        frame = cv.GaussianBlur(frame,(15,15),0)
    elif(Blur == 4):
        frame = cv.medianBlur(frame,25)
    else:
        pass
###########################################
    mins = np.array([0,0,130])#Hmin,Smin,Vmin
    maxs = np.array([180,40,255])#Hmax,Smax,Vmax
###########################################
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    binhsv = cv.inRange(hsv,mins,maxs)
    contours = cv.findContours(binhsv,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]
###########################################
    try:
        if len(contours) > 0:
            cnt = max(contours,key = cv.contourArea)
###########################################
            rect = cv.minAreaRect(cnt)
            accel = -(rect[2])            
            box = cv.boxPoints(rect)
            box = np.int0(box)
            x1,y1 = box[0]
            x2,y2 = box[1]
            x3,y3 = box[2]
            x4,y4 = box[3]
            
            if x3 > x1:
                w1 = x3-x2
                w2 = x4-x1
                cv.line(frame,(int(x2+(w1/2)),int((y3+y2)/2)),(int(x1+(w2/2)),int((y4+y1)/2)),(255,0,255),10)
            else:
                w1 = x4-x3
                w2 = x1-x2
                cv.line(frame,(int(x3+(w1/2)),int((y3+y4)/2)),(int(x2+(w2/2)),int((y2+y1)/2)),(255,0,255),10)
###########################################
            print(accel,x1,x2,x3,x4)
            cv.circle(frame,(int(x1),int(y1)),3,(255,0,255),5)
            cv.circle(frame,(int(x2),int(y2)),3,(0,0,255),5)
            cv.circle(frame,(int(x3),int(y3)),3,(255,255,255),5)
            cv.circle(frame,(int(x4),int(y4)),3,(255,0,0),5)
            cv.drawContours(frame,[box],0,(0,255,255),2)
###########################################
    except Exception as error:
        print(error)
###########################################
    cv.imshow('window3',frame)
###########################################
    key = cv.waitKey(1)
    if key == ord("q"):
        cv.destroyAllWindows()
        break