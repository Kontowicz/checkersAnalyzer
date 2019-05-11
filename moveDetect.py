import cv2
import numpy as np

class moveDetect():

    def __init__(self, image):
        self.image = image
        self.kernel = np.ones((5, 5), np.uint8)
        self.lower_red = np.array([0, 100, 100])
        self.upper_red = np.array([179, 255, 255])

    def Detect(self):
        img_hsv2 = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv2, self.lower_red, self.upper_red)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)

        _, contours, _ = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if len(contours)==20:
            return True
        else:
            return False






