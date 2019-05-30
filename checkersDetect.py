import cv2
import numpy as np

class checkersDetect():

    def __init__(self, image):
        self.image = image
        self.kernel = np.ones((5, 5), np.uint8)
        self.lower_blue = np.array([94, 80, 2])
        self.upper_blue = np.array([126, 255, 255])

    def Detect(self):
        img_hsv2 = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv2, self.lower_blue, self.upper_blue)
        morphology = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        morphology = cv2.morphologyEx(morphology, cv2.MORPH_DILATE, self.kernel)

        _, contours, _ = cv2.findContours(morphology,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        tab = []

        if len(contours)==4:
            for x in range(0,4):
                cnt = contours[x]
                M = cv2.moments(cnt)
                cx  =  int ( M [ 'm10' ] / M [ 'm00' ])
                cy  =  int ( M [ 'm01' ] / M [ 'm00' ])
                tab.append(cx)
                tab.append(cy)

            pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450,450]])
            pts1 = np.float32([[tab[6],tab[7]],[tab[4],tab[5]],[tab[2],tab[3]],[tab[0],tab[1]]])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            result = cv2.warpPerspective(self.image, M, (450, 450))

            return True, result
        else:
            return False, None



# cap = cv2.VideoCapture(1)
#
#
# while(True):
#     ret, frame = cap.read()
#     m=checkersDetect(frame)
#     wynik = m.Detect()
#
#     cv2.imshow('frame',wynik)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

