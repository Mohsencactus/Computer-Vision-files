import cv2 as cv 
import imutils
from time import sleep
########################################################################################################
features = []
########################################################################################################
sift = cv.xfeatures2d.SIFT_create()
bf = cv.BFMatcher(cv.NORM_L2,crossCheck=False)
########################################################################################################
target = cv.imread("/home/mohsencactus/Opencv/HW5/pic.PNG")
#target = imutils.resize(target , height=200 , width=300)
tgkp,tgdsc = sift.detectAndCompute(target,None)
########################################################################################################
objective = cv.imread("/home/mohsencactus/Opencv/HW5/Q1/5.PNG")
objective = imutils.resize(objective,height=2*len(target))
okp,odsc = sift.detectAndCompute(objective,None)
########################################################################################################
match = bf.knnMatch(odsc,tgdsc,k=2)
for a,b in match:
    if a.distance < 0.6 * b.distance:
        features.append(a)
print(len(features))
matchimg = cv.drawMatches(objective,okp,target,tgkp,features,None)
########################################################################################################
for i in features:
    x = int(okp[i.queryIdx].pt[0])
    y = int(okp[i.queryIdx].pt[1])
    cv.circle(matchimg,(x,y),5,(255,0,0),5)
#cv.putText(target,str(i),(x,y-30),cv.FONT_HERSHEY_DUPLEX,1.0,(255, 0, 0), 1)



########################################################################################################
cv.imshow("target",matchimg)
cv.waitKey(0)

    