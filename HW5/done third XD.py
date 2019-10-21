import cv2 as cv 
import imutils
import matplotlib.pyplot as plt
from time import sleep
########################################################################################################
number = []
numberkp = []
numberdsc = []
features = []
matches = []
good = []
x = []
y = []
n = 0
########################################################################################################
sift = cv.xfeatures2d.SIFT_create()
bf = cv.BFMatcher(cv.NORM_L2,crossCheck=False)
########################################################################################################
target = cv.imread("/home/mohsencactus/Opencv/HW5/pic.PNG")
#target = imutils.resize(target , height=200 , width=300)
tgkp,tgdsc = sift.detectAndCompute(target,None)
########################################################################################################
numberpath = "/home/mohsencactus/Opencv/HW5/Q1/"
for i in range (10):
    result = cv.imread(numberpath + str(i) + '.PNG')
    result = imutils.resize(result,height=len(target))
    kp,dsc = sift.detectAndCompute(result,None)
    number.append(result)
    numberkp.append(kp)
    numberdsc.append(dsc)
########################################################################################################
    match = bf.match(tgdsc,numberdsc[i])
    match = sorted(match,key= lambda x:x.distance)
    matches.append(match)
########################################################################################################
    if i != 3:
        x = int(tgkp[match[n].queryIdx].pt[0])
        y = int(tgkp[match[n].queryIdx].pt[1])
        cv.circle(target,(x,y),5,(255,0,0),5)
        cv.putText(target,str(i),(x,y-20),cv.FONT_HERSHEY_DUPLEX,1.0,(255, 0, 0), 1)
    else :
        x = int(tgkp[match[2].queryIdx].pt[0])
        y = int(tgkp[match[2].queryIdx].pt[1])
        cv.circle(target,(x,y),5,(255,0,0),5)
        cv.putText(target,str(i),(x,y-30),cv.FONT_HERSHEY_DUPLEX,1.0,(255, 0, 0), 1)
########################################################################################################
    matchimg = cv.drawMatches(target,tgkp,number[i],numberkp[i],match[0:5],None)
    features.append(matchimg)
########################################################################################################
#print("m1",tgkp[match[0].queryIdx].pt)
cv.imshow("target",target)
cv.waitKey(0)

    