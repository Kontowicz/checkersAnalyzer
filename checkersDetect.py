import cv2
import numpy as np


class checkersDetect():

    def __init__(self, image):
        self.image = image
        self.kernel = np.ones((5, 5), np.uint8)
        self.lower_blue = np.array([94, 80, 2])
        self.upper_blue = np.array([126, 255, 255])

    def Detect(self):
        img_hsv2 = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv2, self.lower_blue, self.upper_blue)
        morphology = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        morphology = cv2.morphologyEx(morphology, cv2.MORPH_DILATE, self.kernel)

        _, contours, _ = cv2.findContours(morphology, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tab = []

        if len(contours) == 4:
            for x in range(0, 4):
                cnt = contours[x]
                M = cv2.moments(cnt)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                tab.append([cx, cy])

            if (tab[0][0] < tab[1][0]):
                pom = tab[0]
                tab[0] = tab[1]
                tab[1] = pom
            if (tab[2][0] < tab[3][0]):
                pom = tab[2]
                tab[2] = tab[3]
                tab[3] = pom

            pts2 = np.float32([[0, 0], [544, 0], [0, 544], [544, 544]])
            pts1 = np.float32(
                [[tab[3][0], tab[3][1]], [tab[2][0], tab[2][1]], [tab[1][0], tab[1][1]], [tab[0][0], tab[0][1]]])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            result = cv2.warpPerspective(self.image, M, (544, 544))

            return True, result
        else:
            return False, None
