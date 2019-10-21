import cv2 as cv
import numpy as np 
import math
import time
###########################################
def nthn(X):
    pass
def cords(slin,yframe,img):
    slope,inter = slin
    y1 = yframe
    y2 = int(yframe*(3/5))
    x1 = int((y1-inter)/slope)
    x2 = int((y2-inter)/slope)
    cv.line(img,(x1,y1),(x2,y2),(255,0,0),10)
###########################################
video = cv.VideoCapture(1)

cv.namedWindow("window2",cv.WINDOW_NORMAL)
cv.createTrackbar("Hmin","window2",0,255,nthn)
cv.createTrackbar("Hmax","window2",0,180,nthn)
cv.createTrackbar("Smin","window2",0,255,nthn)
cv.createTrackbar("Smax","window2",0,255,nthn)
cv.createTrackbar("Vmin","window2",0,255,nthn)
cv.createTrackbar("Vmax","window2",0,255,nthn)
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
roix1 = int(xframe*2/8)
roiy1 = int(yframe*0/3)
roix2 = int(xframe*6/8)
roiy2 = int(yframe*0/3)
roix4 = int(xframe*0/4)
roiy4 = int(yframe)
roix3 = int(xframe*4/4)
roiy3 = int(yframe)
roi = np.array([[(roix1,roiy1),(roix2,roiy2),(roix3,roiy3),(roix4,roiy4)]])
###########################################
while True:
    linesx = []
    linesy = []
    linesfeat = []
###########################################
    _,frame = video.read()
    Hmin = cv.getTrackbarPos("Hmin","window2")
    Smin = cv.getTrackbarPos("Smin","window2")
    Vmin = cv.getTrackbarPos("Vmin","window2")
    Hmax = cv.getTrackbarPos("Hmax","window2")
    Smax = cv.getTrackbarPos("Smax","window2")
    Vmax = cv.getTrackbarPos("Vmax","window2")
    mins = np.array([Hmin,Smin,Vmin])
    maxs = np.array([Hmax,Smax,Vmax])
###########################################
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    binhsv = cv.inRange(hsv,mins,maxs)
    filhsv = cv.bitwise_and(frame ,frame ,mask = binhsv)
    rgb = cv.cvtColor(filhsv,cv.COLOR_HSV2BGR)
    gray = cv.cvtColor(rgb,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),0) 
    canny1 = cv.Canny(blur,50,150)
    cannyrgb = cv.cvtColor(canny1,cv.COLOR_GRAY2BGR)
###########################################    
    cv.fillPoly(binroi,roi,(255,255,255))
###########################################
    roied = cv.bitwise_and(cannyrgb,binroi)
    canny = cv.Canny(roied,50,150)
    lines = cv.HoughLinesP(canny,2,np.pi/180,100,np.array([]),minLineLength=5,maxLineGap=5) 
###########################################
    left_fit = []
    right_fit = []
    linesimg = np.zeros_like(frame)
    try:
        if len(lines) > 0:
            for line in lines:
                xl1,yl1,xl2,yl2 = line[0]
                parameter = np.polyfit((xl1,xl2),(yl1,yl2),1)
                slope = parameter[0]
                intercept = parameter[1]
                if slope < 0:
                    left_fit.append((slope,intercept))
                else :
                    right_fit.append((slope,intercept))
            left_fitavg = np.average(left_fit,axis=0)
            right_fitavg = np.average(right_fit,axis=0)
            average = [left_fitavg,right_fitavg]
            for i in range (0,len(average)):
                if isinstance(average[i], np.ndarray) == True:
                    cords(average[i],yframe,linesimg)

    except Exception as error:
        print(error)
###########################################
    highlight = cv.addWeighted(frame,0.8,linesimg,1,1)
    highlighthsv = cv.addWeighted(filhsv,0.8,linesimg,1,1)
    cv.imshow('frame32',highlight)
    cv.imshow('frame',roied)
    cv.imshow('window2',filhsv)
###########################################
    key = cv.waitKey(1)
    if key == ord("q"):
        cv.destroyAllWindows()
        break