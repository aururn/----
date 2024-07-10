import cv2
import numpy as np
from matplotlib import pyplot as plt

path = r"C:\Users\Aurum\Documents\img\test.jpg"
img = cv2.imread(path)
cv2.imshow("aaa",img)

kernel = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(img,-1,kernel)

plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()