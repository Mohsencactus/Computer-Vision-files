import cv2 as cv
import numpy as np 
########################################################
def nthn(X):
    pass
def cords(slin,yframe,img):
    slope,inter = slin
    y1 = yframe
    y2 = int(yframe*(3/5))
    x1 = int((y1-inter)/slope)
    x2 = int((y2-inter)/slope)
    cv.line(img,(x1,y1),(x2,y2),(255,0,0),10)

def roiit(frame,x1,x2,x3,x4,y1,y2,y3,y4):
    roi = np.array([[(x1,y1),(x2,y2),(x3,y3),(x4,y4)]])
    binroi = np.zeros_like(frame)
    cv.fillPoly(binroi,roi,(255,255,0))
    return roi,binroi

datafile = '/home/mohsencactus/Github Python/Python Opencv-start/hsv.txt'

with open(datafile, "r") as maindata: 
    data = maindata.read()

########################################################
cv.namedWindow("window2",cv.WINDOW_NORMAL)
cv.createTrackbar("Hmin","window2",0,255,nthn)
cv.createTrackbar("Hmax","window2",0,255,nthn)
cv.createTrackbar("Smin","window2",0,255,nthn)
cv.createTrackbar("Smax","window2",0,255,nthn)
cv.createTrackbar("Vmin","window2",0,255,nthn)
cv.createTrackbar("Vmax","window2",0,255,nthn)
txt = data.split('_')
txt = np.int0(txt)
print(txt)
cv.setTrackbarPos("Hmin","window2",txt[0])
cv.setTrackbarPos("Smin","window2",txt[1])
cv.setTrackbarPos("Vmin","window2",txt[2])
cv.setTrackbarPos("Hmax","window2",txt[3])
cv.setTrackbarPos("Smax","window2",txt[4])
cv.setTrackbarPos("Vmax","window2",txt[5])
cv.createTrackbar('blur',"window2",0,4,nthn)
cv.createTrackbar('mor',"window2",0,1,nthn)
########################################################
video = cv.VideoCapture(1)
########################################################
_,frame = video.read()
yframe = len(frame)
xframe = len(frame[1])
binroi = np.zeros_like(frame)
linesimg = np.zeros_like(frame)

while True:
    linesx = []
    linesy = []
    linesfeat = []
    left_fit = []
    right_fit = []
    linesimg = np.zeros_like(frame)

    Hmin = cv.getTrackbarPos("Hmin","window2")
    Smin = cv.getTrackbarPos("Smin","window2")
    Vmin = cv.getTrackbarPos("Vmin","window2")
    Hmax = cv.getTrackbarPos("Hmax","window2")
    Smax = cv.getTrackbarPos("Smax","window2")
    Vmax = cv.getTrackbarPos("Vmax","window2")
########################################################
    Blur = cv.getTrackbarPos("blur","window2")
    mor = cv.getTrackbarPos("mor","window2")
    with open(datafile, "w") as maindata:
        line = str(Hmin)+'_'+str(Smin)+'_'+str(Vmin)+'_'+str(Hmax)+'_'+str(Smax)+'_'+str(Vmax)
        maindata.write(line)
    mins = np.array([Hmin,Smin,Vmin])
    maxs = np.array([Hmax,Smax,Vmax])
########################################################
    _,frame = video.read()
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    binhsv1 = cv.inRange(hsv,mins,maxs)
    
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
    if mor == 1 :
        kernel = np.ones((5,5),np.uint8)
        dilation = cv.dilate(binhsv1,kernel,iterations = 2)
        kernel = np.ones((15,15),np.uint8)
        opening = cv.morphologyEx(dilation, cv.MORPH_OPEN, kernel)
        binhsv = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
    else:
        binhsv = binhsv1

    filhsv = cv.bitwise_and(frame ,frame ,mask = binhsv)
    contours = cv.findContours(binhsv,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]
    try:
        if len(contours) > 0:
            cnt = max(contours,key = cv.contourArea)
            rect = cv.minAreaRect(cnt)            
            box = cv.boxPoints(rect)
            box = np.int0(box)
            region,binroi = roiit(frame,box[0][0],box[1][0],box[2][0],box[3][0],box[0][1],box[1][1],box[2][1],box[3][1])
            cv.drawContours(frame,[box],0,(0,255,255),2)
            rgb = cv.cvtColor(filhsv,cv.COLOR_HSV2BGR)

            gray = cv.cvtColor(rgb,cv.COLOR_BGR2GRAY)
            canny1 = cv.Canny(gray,50,150)
            cannyrgb = cv.cvtColor(canny1,cv.COLOR_GRAY2BGR)

            roied = cv.bitwise_and(cannyrgb,binroi)
            canny = cv.Canny(roied,50,150,3)
            cv.imshow('frame',canny)
            lines = cv.HoughLinesP(canny,2,np.pi/180,100,np.array([]),minLineLength=5,maxLineGap=5) 

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
                    averageavg = np.average((right_fitavg,left_fitavg),axis=0)
                    cords(left_fitavg,yframe,linesimg)
                    cords(right_fitavg,yframe,linesimg)

            except Exception as error:
                print(error)        
    except Exception as error:
        print(error)

    highlight = cv.addWeighted(frame,0.8,linesimg,1,1)

    cv.imshow('frame32',highlight)
    cv.imshow('window2',filhsv)

    key = cv.waitKey(1)
    if key == ord("q"):
        cv.destroyAllWindows()
        break