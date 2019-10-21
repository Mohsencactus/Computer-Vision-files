from sklearn.datasets import fetch_openml
from skimage import feature
from sklearn.svm import LinearSVC
import numpy as np 

#the hand writen numbers dataset
mnist_dataset = fetch_openml("MNIST_784")

#the dataset pic it self
tasvir = mnist_dataset.data
#the labels of the pics
label = mnist_dataset.target 

#list of hog features
hogl = []

#resizing the pics and extracting features out of each of them
for item in tasvir:
    f_vec = feature.hog(item.reshape(28,28)) 
    hogl.append((f_vec))

#initializing mcl 
model = LinearSVC()
#configuring the dataset
model.fit(np.array(hogl),label)
#checking the finall perdiction with the actual label
score = model.score(np.array(hogl),label)

print(score)