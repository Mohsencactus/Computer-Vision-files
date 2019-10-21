from sklearn.datasets import fetch_openml
from skimage import feature
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import cv2 as cv
#########################################################################################################
mnist_dataset = fetch_openml("MNIST_784")
tasvir = mnist_dataset.data
label = mnist_dataset.target 
#########################################################################################################
hogl = []
detection = []
rois = []
for item in tasvir:
    f_vec = feature.hog(item.reshape(28,28)) 
    hogl.append((f_vec))
#########################################################################################################
#model = KNeighborsClassifier(n_neighbors=50)
model = LinearSVC()
model.fit(np.array(hogl),label)
#########################################################################################################
frame = cv.imread("/home/mohsencactus/Opencv/digit/digit2.jpg")
grayed = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
binaried = cv.inRange(grayed, 0, 90)
contours = cv.findContours(binaried,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)[1]
#######################################################
if len(contours) > 0:
    for cnt in contours:
        x,y,w,h = cv.boundingRect(cnt)
        x,y,w,h = x-10,y-10,w+30,h+30
        #cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi = frame[y:y+h,x:x+w]
        roi = cv.resize(roi,(28,28))
        rois.append(roi)
        vec_roi = feature.hog(roi)
        result = model.predict(np.array([vec_roi]))[0]
        cv.putText(frame,str(result),(x,y-20),cv.FONT_HERSHEY_DUPLEX,1.0,(255, 0, 0), 1)
        detection.append(result)
#########################################################################################################
cv.imshow("frame1", frame)
cv.imshow("frame3", binaried)
#########################################################################################################
cv.waitKey(0)
cv.destroyAllWindows()

 