import cv2 as cv 
import imutils

impath = ("/home/mohsencactus/!!Opencv/Part5_material/book1.jpg")
impath2 = ("/home/mohsencactus/!!Opencv/Part5_material/book2.jpg")

img = cv.imread(impath)
img2 = cv.imread(impath2)

img = imutils.resize(img , width=500)
img2 = imutils.resize(img2 , width=500)


sift = cv.xfeatures2d.SIFT_create()
#kp = sift.detect(img ,None)
kp,dsc = sift.detectAndCompute(img ,None)
kp2,dsc2 = sift.detectAndCompute(img2 ,None)

bf = cv.BFMatcher(cv.NORM_L2,crossCheck=False)

match = bf.knnMatch(dsc,dsc2,k=2)
features = []

for a,b in match:
    if a.distance < 0.4 * b.distance:
        features.append(a)


matchrs = cv.drawMatches(img,kp,img2,kp2,features,None)

cv.imshow("frame",matchrs)
cv.waitKey(0)
