import cv2
import numpy as np



cap = cv2.VideoCapture("BoardDetect/movie.mp4")
kernel = np.ones((5,5), np.uint8)

img2 = np.zeros([100,100,3])
img2[:]=[255,255,255]
font = cv2.FONT_HERSHEY_SIMPLEX

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('BoardDetect/test.avi', fourcc, 20.0, (1152,736))

key = ord('a')
while key != ord('q'):

    _, frame = cap.read()
    img_base = frame
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
    if len(contours)==4:
        for x in range(0,4):
            cnt = contours[x]
            M = cv2.moments(cnt)
            cx  =  int ( M [ 'm10' ] / M [ 'm00' ])
            cy  =  int ( M [ 'm01' ] / M [ 'm00' ])
            tab.append(cx)
            tab.append(cy)
            #cv2.putText(img_base, str(x), (cx, cy), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

        pts2 = np.float32([[0, 0], [736, 0], [0, 736], [736,736]])
        pts1 = np.float32([[tab[4],tab[5]],[tab[6],tab[7]],[tab[2],tab[3]],[tab[0],tab[1]]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        img2 = cv2.warpPerspective(img_base, M, (736, 736))


    numpy_horizontal_concat = np.concatenate((img_base, img2), axis=1)
    print(img_base.shape)
    print(img2.shape)

    out.write(numpy_horizontal_concat)
    cv2.imshow("Base", img_base)
    cv2.imshow("Result", img2)
    cv2.imshow("R", numpy_horizontal_concat)
    key = cv2.waitKey(15)

cap.release()
out.release()
cv2.destroyAllWindows()



