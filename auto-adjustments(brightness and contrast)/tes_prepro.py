import cv2
import os
import numpy as np

path = '/home/erwin/Downloads/WhatsApp Image 2019-10-10 at 1.32.35 PM.jpeg'

img = cv2.imread(path,0)
alpha = 4.5
beta = -160
# beta = -150

new = alpha * img + beta
new = np.clip(new, 0, 255).astype(np.uint8)
# new = cv2.adaptiveThreshold(new, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 7)
kernel = np.ones((2, 2), np.uint8)
kernel1 = np.ones((1, 1), np.uint8)
new = cv2.erode(new, kernel, iterations=2)
new = cv2.erode(new, kernel1, iterations=12)
new = cv2.blur(new, (2, 2))
ret,new = cv2.threshold(new,100,255,cv2.THRESH_TOZERO)
cv2.imwrite('haha.jpg', new)

cv2.imshow('tes',new)
cv2.waitKey(0)
cv2.destroyAllWindows()