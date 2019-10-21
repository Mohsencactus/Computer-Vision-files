import cv2 as cv
import numpy as np 
import math
import time
###########################################
def nthn(X):
    pass
def cords(frame,linesavg,yframe,linesyavg):
    slope,inter = linesavg
    y1 = int(yframe)
    y2 = int(linesyavg[1])
    x1 = int((y1-inter)/slope)
    x2 = int((y2-inter)/slope)
    cv.line(frame,(x1,y1),(x2,y2),(255,255,0),10)
    return (x1,x2,y1,y2)
###########################################
video = cv.VideoCapture(1)

cv.namedWindow("window2",cv.WINDOW_NORMAL)

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
binroi = np.zeros_like(frame)
linesimg = np.zeros_like(frame)
###########################################
while True:
    linesx = []
    linesy = []
    linesfeatr = []
    linesfeatl = []
###########################################
    _,frame = video.read()
    Hmin = cv.getTrackbarPos("Hmin","window2")
    Smin = cv.getTrackbarPos("Smin","window2")
    Vmin = cv.getTrackbarPos("Vmin","window2")
    Hmax = cv.getTrackbarPos("Hmax","window2")
    Smax = cv.getTrackbarPos("Smax","window2")
    Vmax = cv.getTrackbarPos("Vmax","window2")
    Blur = 3#cv.getTrackbarPos('blur',"window2")
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
    mins = np.array([Hmin,Smin,Vmin])#
    maxs = np.array([Hmax,Smax,Vmax])#Hmax,Smax,Vmax
###########################################
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    binhsv = cv.inRange(hsv,mins,maxs)
    filhsv = cv.bitwise_and(frame ,frame ,mask = binhsv)
    contours = cv.findContours(binhsv,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]
    try:
        if len(contours) > 0:
            cnt = max(contours,key = cv.contourArea)
            (x,y,w,h) = cv.boundingRect(cnt) 
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            
            rgb = frame[int(y):int(y+h), int(x):int(x+w)]
            gray = cv.cvtColor(rgb,cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray,(5,5),0) 
            canny = cv.Canny(blur,50,150)
            lines = cv.HoughLinesP(canny,2,np.pi/180,100,np.array([]),minLineLength=5,maxLineGap=5) 
###########################################
            cv.imshow('fs',canny)
###########################################
            if len(lines) > 0:
                for line in lines:
                    xl1,yl1,xl2,yl2 = line[0]
                    parameter = np.polyfit((xl1,xl2),(yl1,yl2),1)
                    slope = parameter[0]
                    intercept = parameter[1]
###########################################
                    linesx.append((xl1,xl2))
                    linesy.append((yl1,yl2))
                    if slope > 0:
                        linesfeatl.append((slope,intercept))
                    elif slope < 0:
                        linesfeatr.append((slope,intercept))
                lineslavg = np.average(linesfeatl,axis=0)
                linesravg = np.average(linesfeatr,axis=0)
                linesxavg = np.average(linesx,axis=0)
                linesyavg = np.average(linesy,axis=0)
###########################################
                cords1 = cords(rgb,linesravg,yframe,linesyavg)
                cords2 = cords(rgb,lineslavg,yframe,linesyavg)
                randllines = (cords1,cords2)
                mainline = np.average(randllines,axis=0)
                cv.line(rgb,(int(mainline[0]),int(mainline[2])),(int(mainline[1]),int(mainline[3])),(0,255,255),10)
###########################################
    except Exception as error:
        print(error)
###########################################
    highlight = cv.addWeighted(frame,0.8,linesimg,1,1)
    highlighthsv = cv.addWeighted(filhsv,0.8,linesimg,1,1)
    cv.imshow('frame32',highlight)
    cv.imshow('window2',filhsv)
    #cv.imshow('window3',frame)
###########################################
    key = cv.waitKey(1)
    if key == ord("q"):
        cv.destroyAllWindows()
        break