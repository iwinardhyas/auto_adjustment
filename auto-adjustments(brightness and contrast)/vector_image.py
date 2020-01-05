import cv2
import numpy as np



# 1) Edges
def vector_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)

    # 2) Color
    color = cv2.bilateralFilter(img, 5, 200, 200)

    # 3) Cartoon
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon, color, edges, img

# img = cv2.imread("/home/erwin/Desktop/test_ibuk2/1_670074_DST0163_08:59:27.176995.jpg")

# cartoon, color, edges, img = vector_image(img)

# cv2.imshow("Image", img)
# cv2.imshow("Cartoon", cartoon)
# cv2.imshow("color", color)
# cv2.imshow("edges", edges)
# cv2.waitKey(0)
# cv2.destroyAllWindows()