import cv2 as cv 
import imutils
from time import sleep
########################################################################################################
number = []
numberkp = []#target = imutils.resize(target , height=200 , width=300)
numberdsc = []#target = imutils.resize(target , height=200 , width=300)
features = []#target = imutils.resize(target , height=200 , width=300)

########################################################################################################
sift = cv.xfeatures2d.SIFT_create()
bf = cv.BFMatcher(cv.NORM_L2,crossCheck=False)
########################################################################################################
target = cv.imread("/home/mohsencactus/Opencv/HW5/pic.PNG")
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
    print(match)
    match = sorted(match,key= lambda x:x.distance)
    matchimg = cv.drawMatches(target,tgkp,number[i],numberkp[i],match[0:1],None)
    features.append(matchimg)
########################################################################################################
for i in features:
    cv.imshow("target",i)
    cv.waitKey(0)




