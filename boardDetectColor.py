import cv2
import numpy as np

kernel = np.ones((5,5), np.uint8)
img_base = cv2.resize(cv2.imread("BoardDetect/n2.jpg", cv2.IMREAD_COLOR),(0,0), fx=0.2, fy=0.2)
img_ycbr = cv2.cvtColor(img_base,cv2.COLOR_BGR2YCrCb)
img_hsv = cv2.cvtColor(img_ycbr,cv2.COLOR_BGR2HSV)
img_hsv2 = cv2.cvtColor(img_base,cv2.COLOR_BGR2HSV)
img_gray_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
img_copy = img_base.copy()

lower_blue = np.array([37, 30, 100])
upper_blue = np.array([157, 255, 255])
mask = cv2.inRange(img_hsv2, lower_blue, upper_blue)
result = cv2.bitwise_and(img_base, img_base, mask=mask)
img_erosion = cv2.erode(mask, kernel, iterations=1)
img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)


image_kontury, contours, hierarchy = cv2.findContours(img_dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
tab = []

for x in range(0,4):
    print(x)
    cnt = contours[x]
    M = cv2.moments(cnt)
    cx  =  int ( M [ 'm10' ] / M [ 'm00' ])
    cy  =  int ( M [ 'm01' ] / M [ 'm00' ])
    tab.append(cx)
    tab.append(cy)
pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450,450]])
pts1 = np.float32([[tab[6],tab[7]],[tab[4],tab[5]],[tab[2],tab[3]],[tab[0],tab[1]]])
M = cv2.getPerspectiveTransform(pts1, pts2)
img2 = cv2.warpPerspective(img_base, M, (450, 450))


key = ord('a')
while key != ord('q'):

    cv2.imshow("Base", img_base)
    cv2.imshow("HSV", img_hsv2)
    cv2.imshow("mask", img_dilation)
    cv2.imshow("result", img2)
    key = cv2.waitKey(0)




