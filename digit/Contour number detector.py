import numpy as np
import cv2 as cv
#########################################################################################################
frame = cv.imread("/home/mohsencactus/Opencv/HW5/download.jpeg")
#########################################################################################################
grayed = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
binaried = cv.inRange(grayed, 0, 90)
contours = cv.findContours(binaried,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)[1]
#########################################################################################################
if len(contours) > 0:
    for cnt in contours:
        x,y,w,h = cv.boundingRect(cnt)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
#########################################################################################################
cv.imshow("frame1", frame)
cv.imshow("frame3", binaried)
#########################################################################################################
cv.waitKey(0)
cv.destroyAllWindows()

 