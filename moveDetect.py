import cv2
import numpy as np

class moveDetect():

    def __init__(self, image):
        self.image = image
        self.kernel = np.ones((5, 5), np.uint8)
        self.lower_red_one = np.array([0, 80, 70])
        self.lower_red_two = np.array([170, 120, 70])
        self.upper_red_one = np.array([10, 255, 255])
        self.upper_red_two = np.array([180, 255, 255])

    def Detect(self):
        img_hsv2 = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        mask_one = cv2.inRange(img_hsv2, self.lower_red_one, self.upper_red_one)
        mask_two = cv2.inRange(img_hsv2, self.lower_red_two, self.upper_red_two)
        mask_final = mask_one + mask_two
        morphology = cv2.morphologyEx(mask_final, cv2.MORPH_OPEN, self.kernel)
        morphology = cv2.morphologyEx(morphology, cv2.MORPH_DILATE, self.kernel)
        morphology = cv2.rectangle(morphology,(10,10),(440,440),(0,0,0),-1)
        _, contours, _ = cv2.findContours(morphology,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if len(contours)==34:
            return True
        else:
            return False


# cap = cv2.VideoCapture(1)
#
#
# while(True):
#     ret, frame = cap.read()
#     m=moveDetect(frame)
#     wynik = m.Detect()
#
#     cv2.imshow('frame',wynik)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()




