import cv2 as cv 
#####################################################################################
impath = ("/home/mohsencactus/files/Codes/Github Python/Python Opencv-start/Part5_material/ielts.jpg")
path = ("/home/mohsencactus/files/Codes/Github Python/Python Opencv-start/Part5_material/conv.mp4")
#####################################################################################
img = cv.imread(impath)
vid = cv.VideoCapture(path)
#####################################################################################
while True:
    _,frame = vid.read()

    cv.imshow("frame",frame)
    if ord("q") == cv.waitKey(1):
        cv.destroyAllWindows()
        break 

