import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from vector_image import vector_image

# Automatic brightness and contrast optimization with optional histogram clipping
# image FR using clip_hist_percent = 25

def automatic_brightness_and_contrast(image, clip_hist_percent=10):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    
    # Calculate new histogram with desired range and show histogram 
    # new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    # plt.plot(hist)
    # plt.plot(new_hist)
    # plt.xlim([0,256])
    # plt.show()
    image = alpha * image + beta
    auto_result = np.clip(image, 0, 255).astype(np.uint8)
    print(alpha)
    print (beta)

    # auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)


def prepro(img):
    alpha = 2.5
    beta = -160
    # beta = -150

    new = alpha * img + beta
    new = np.clip(new, 0, 255).astype(np.uint8)
    # new = cv2.adaptiveThreshold(new, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 7)
    kernel = np.ones((2, 2), np.uint8)
    kernel1 = np.ones((1, 1), np.uint8)
    new = cv2.erode(new, kernel, iterations=1)
    new = cv2.erode(new, kernel1, iterations=12)
    new = cv2.blur(new, (2, 2))
    ret,new = cv2.threshold(new,100,255,cv2.THRESH_TOZERO)

    print(alpha)
    print (beta)

    return (new, alpha, beta)

def prepro2(img):
    img = cv2.blur(img, (2, 2))
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49, 50)
    kernel = np.ones((1, 1), np.uint8)
    kernel_dillation = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    new = cv2.dilate(closing,kernel_dillation, iterations=1)
    new = cv2.erode(new,kernel_dillation, iterations=2)

    return new

# path = '/home/erwin/Desktop/test_ibuk2/'
# path = '/home/erwin/Documents/project_docrec/error/toefl/jpg/angka tidak terbaca google vision8.jpg'
path = '/home/erwin/Documents/project_docrec/error_file.jpg'
image = cv2.imread(path)
hist = cv2.calcHist([image],[0],None,[256],[0,256])
plt.plot(hist)
# plt.plot(new_hist)
plt.xlim([0,256])
plt.show()
# new, alpha, beta = prepro(image)
# auto_result, alpha, beta = automatic_brightness_and_contrast(new)
# new = prepro2(image)

# cv2.imshow('result',new)
# cv2.waitKey(0)
# for im in os.listdir(path):
#     image_im = path+im
#     print(im)

#     image = cv2.imread(image_im)
#     auto_result, alpha, beta = automatic_brightness_and_contrast(image)
#     print('alpha', alpha)
#     print('beta', beta)
#     cartoon, color, edges, img = vector_image(auto_result)

#     # cv2.imshow('auto_result', cartoon)
#     cv2.imwrite('/home/erwin/Desktop/'+im+'.jpeg', cartoon)
    # cv2.imshow('image', image)
    # cv2.waitKey()