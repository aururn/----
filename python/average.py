import cv2
import numpy as np
from matplotlib import pyplot as plt


path = r"C:\Users\Aurum\Documents\img\test.png"
img = cv2.imread(path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.blur(img_gray,(5,5))
blur2 = cv2.GaussianBlur(img_gray,(5,5),0)
blur3 = cv2.bilateralFilter(img_gray,9,75,75)
median = cv2.medianBlur(img_gray,5)


titles = ['Original Image','blur','Gaussian','bilateral','median']
images = [img_gray, blur, blur2, blur3, median]

for i in range(5):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()