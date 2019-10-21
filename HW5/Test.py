import os
import cv2 as cv 


files = []
path = '/home/mohsencactus/Opencv/HW5/Q1'
for filename in os.listdir(path):
   files.append(filename)
   
images = []
labels = []
for i in range (len(files)):
    filename = files[i]
    labels.append(filename.replace('.PNG',''))
    source = cv.imread(path + '/' + filename)
    source = cv.resize(source,(28,28))
    images.append(source)
    cv.imshow("sda",source)
    cv.waitKey(0)
    print(labels)