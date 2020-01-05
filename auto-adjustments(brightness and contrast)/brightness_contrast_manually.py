import cv2
import numpy as np

for i in range(100,0,-10):
    img = cv2.imread('/home/erwin/Desktop/1_670074_DST0163_08:59:27.176995.jpg')
    brightness = 0
    # brightness = 70
    contrast = i
    img_new = np.int16(img)
    img_new = img_new * (contrast/127+1) - contrast + brightness
    img_new = np.clip(img_new, 0, 255)
    img_new = np.uint8(img_new)
    cv2.imwrite('/home/erwin/Desktop/1_670074_DST0163_08:59:27.17699'+str(i)+'.jpg',img_new)

# cv2.imshow('input',img)
# cv2.imshow('output',img_new)
# cv2.waitKey(0)
# cv2.destroyAllWindows()