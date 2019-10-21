import cv2 as cv 
import imutils
import matplotlib.pyplot as plt
#####################################################################################
def bgrr(frame):
    bgr = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    return bgr
#####################################################################################
impath = ("/home/mohsencactus/files/Codes/Github Python/Python Opencv-start/Part5_material/ielts.jpg")
path = ("/home/mohsencactus/files/Codes/Github Python/Python Opencv-start/Part5_material/conv.mp4")
sift = cv.xfeatures2d.SIFT_create()
#####################################################################################
img = cv.imread(impath)
img = imutils.resize(img , width=500)
kp,dsc = sift.detectAndCompute(img ,None)

vid = cv.VideoCapture(path)
#####################################################################################
while True:
    _,frame = vid.read()
    print(frame)
    plt.imshow(img)
    plt.show()
    
#kp2,dsc2 = sift.detectAndCompute(img2 ,None)
#
#bf = cv.BFMatcher(cv.NORM_L2,crossCheck=False)
#
#match = bf.knnMatch(dsc,dsc2,k=2)
#features = []
#
#for a,b in match:
#    if a.distance < 0.4 * b.distance:
#        features.append(a)
#
#matchrs = cv.drawMatches(img,kp,img2,kp2,features,None)
    #bgr = bgrr(frame)
    #bgr2 = bgrr(img2)
    #bgr3 = bgrr(matchrs)



