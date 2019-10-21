import cv2 as cv 
import imutils
import matplotlib.pyplot as plt

def bgrr(frame):
    bgr = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    return bgr


impath = ("/home/mohsencactus/files/Codes/Github Python/Python Opencv-start/Part5_material/book1.jpg")
impath2 = ("/home/mohsencactus/files/Codes/Github Python/Python Opencv-start/Part5_material/book2.jpg")

img = cv.imread(impath)
img2 = cv.imread(impath2)

img = imutils.resize(img , width=500)
img2 = imutils.resize(img2 , width=500)


sift = cv.xfeatures2d.SIFT_create()
#kp = sift.detect(img ,None)
kp,dsc = sift.detectAndCompute(img ,None)
kp2,dsc2 = sift.detectAndCompute(img2 ,None)

bf = cv.BFMatcher(cv.NORM_L2,crossCheck=True)

match = bf.match(dsc,dsc2)
match = sorted(match,key= lambda x:x.distance)
matchrs = cv.drawMatches(img,kp,img2,kp2,match[0:40],None)




bgr = bgrr(img)
bgr2 = bgrr(img2)
bgr3 = bgrr(matchrs)

plt.imshow(bgr3)
plt.show()

