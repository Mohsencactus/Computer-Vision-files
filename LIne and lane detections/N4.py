
import cv2 as cv
import numpy as np 
import math
import time
###########################################
def nthn(X):
    pass
def checker(x1,x2,x3,x4,y1,y2,y3,y4):
    if y2 < y1 and y2 < y4 and y3 < y4 and y3 < y1:
        w1 = x3-x2
        w2 = x4-x1
        xs1 = int(x2+(w1/2))
        xs2 = int(x1+(w2/2))
        ys1 = int((y3+y2)/2)
        ys2 = int((y1+y4)/2)
        return(xs1,xs2,ys1,ys2,w1,w2)
    elif x2 < x1 and x2 < x3 and x2 < x4 and y2 > y4:
        w1 = x4-x3
        w2 = x1-x2
        xs1 = int(x3+(w1/2))
        xs2 = int(x2+(w2/2))
        ys1 = int((y3+y4)/2)
        ys2 = int((y2+y1)/2)
        return(xs1,xs2,ys1,ys2,w1,w2)
    else:
        w1 = x4-x3
        w2 = x1-x2
        xs1 = int(x3+(w1/2))
        xs2 = int(x2+(w2/2))
        ys1 = int((y3+y4)/2)
        ys2 = int((y2+y1)/2)
        return(xs1,xs2,ys1,ys2,w1,w2)
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
    _,frame1 = video.read()
    frame = frame1[int(yframe*(1/3)):int(yframe), int(0):int(xframe)]
###########################################
    Hmin = cv.getTrackbarPos("Hmin","window2")
    Smin = cv.getTrackbarPos("Smin","window2")
    Vmin = cv.getTrackbarPos("Vmin","window2")
    Hmax = cv.getTrackbarPos("Hmax","window2")
    Smax = cv.getTrackbarPos("Smax","window2")
    Vmax = cv.getTrackbarPos("Vmax","window2")
    Blur = 0#cv.getTrackbarPos('blur',"window2")
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
    mins = np.array([0,0,130])#Hmin,Smin,V minnp.array([0,0,130])
    maxs = np.array([180,65,255])#Hmax,Smax,Vmax
###########################################
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    binhsv = cv.inRange(hsv,mins,maxs)
    contours = cv.findContours(binhsv,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]
    try:
        if len(contours) > 0:
            cnt2 = max(contours,key = cv.contourArea) 
            rect = cv.minAreaRect(cnt2)            
            box = cv.boxPoints(rect)
            box = np.int0(box)
            x1,y1 = box[0]
            x2,y2 = box[1]
            x3,y3 = box[2]
            x4,y4 = box[3]
            

            x1,x2,y1,y2,w1,w2 = checker(x1,x2,x3,x4,y1,y2,y3,y4)

            rgb = frame[int(y1):int(y2),int(x1-(w1/2)):int(x3)]
            cv.imshow('window4',rgb)
            cv.drawContours(frame,[box],0,(0,255,255),2)
            mins2 = np.array([0,0,0])#Hmin,Smin,V minnp.array([0,0,130])
            maxs2 = np.array([180,80,130])#Hmax,Smax,Vmax
            hsv2 = cv.cvtColor(rgb,cv.COLOR_BGR2HSV)
            binhsv2 = cv.inRange(hsv2,mins2,maxs2)
            contours2 = cv.findContours(binhsv2,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]
        ###########################################
            try:
                if len(contours2) > 0:
                    cnt = max(contours2,key = cv.contourArea)
        ###########################################
                    rect = cv.minAreaRect(cnt)
                    accel = -(rect[2])            
                    box = cv.boxPoints(rect)
                    box = np.int0(box)
                    x1,y1 = box[0]
                    x2,y2 = box[1]
                    x3,y3 = box[2]
                    x4,y4 = box[3]
                    xs1,xs2,ys1,ys2,w1,w2 = checker(x1,x2,x3,x4,y1,y2,y3,y4)
        ###########################################
                    cv.line(rgb,(xs1,ys1),(xs2,ys2),(255,0,255),10)
                    parameter = np.polyfit((xs1,xs2),(ys1,ys2),1)
                    slope = parameter[0]
                    print(slope)
                    cv.circle(rgb,(int(x1),int(y1)),3,(255,0,255),5)
                    cv.circle(rgb,(int(x2),int(y2)),3,(0,0,255),5)
                    cv.circle(rgb,(int(x3),int(y3)),3,(255,255,255),5)
                    cv.circle(rgb,(int(x4),int(y4)),3,(255,0,0),5)
                    cv.drawContours(rgb,[box],0,(0,255,255),2)
###########################################
            except:
                pass
    except Exception as error:
        print(error)
###########################################
    cv.imshow('window2',frame)
###########################################
    key = cv.waitKey(1)
    if key == ord("q"):
        cv.destroyAllWindows()
        break