import cv2
import numpy as np

class moveDetect():

    def __init__(self, image):
        self.image = image
        self.kernel = np.ones((5, 5), np.uint8)
        self.low_green = np.array([50,60,60])
        self.high_green = np.array([80, 255, 255])

    def Detect(self):
        img_hsv2 = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv2, self.low_green, self.high_green)
        morphology = cv2.dilate(mask,self.kernel,iterations=3)
        morphology = cv2.dilate(morphology,self.kernel)
        _, contours, _ = cv2.findContours(morphology,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)==12:
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




