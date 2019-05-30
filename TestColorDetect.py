import cv2
import numpy as np
cap = cv2.VideoCapture(1)
from checkersDetect import checkersDetect as CD
from moveDetect import  moveDetect as MD
import  checkersAnalyzer as CA

class Green():
    def __init__(self, image):
        self.image = image
        self.kernel = np.ones((5, 5), np.uint8)
        self.low_green = np.array([36,25,25])
        self.high_green = np.array([70, 255, 255])

    def Detect(self):
        img_hsv2 = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv2, self.low_green, self.high_green)
        morphology = cv2.erode(mask,self.kernel)
        morphology = cv2.morphologyEx(morphology, cv2.MORPH_OPEN, self.kernel)
        morphology = cv2.morphologyEx(morphology, cv2.MORPH_DILATE, self.kernel)
        return morphology

class Yelow():
    def __init__(self, image):
        self.image = image
        self.kernel = np.ones((5, 5), np.uint8)
        self.lower_red_one = np.array([0, 120, 70])
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
        return  morphology

class Blue():
    def __init__(self, image,a,b,c,d,e,f):
        self.image = image
        self.kernel = np.ones((5, 5), np.uint8)
        self.lower_blue = np.array([a,b,c])
        self.upper_blue = np.array([d,e,f])

    def Detect(self):
        img_hsv2 = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv2, self.lower_blue, self.upper_blue)
        morphology = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        #morphology = cv2.morphologyEx(morphology, cv2.MORPH_DILATE, self.kernel)

        _, contours, _ = cv2.findContours(morphology,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        tab = []

        # if len(contours)==4:
        #     for x in range(0,4):
        #         cnt = contours[x]
        #         M = cv2.moments(cnt)
        #         cx  =  int ( M [ 'm10' ] / M [ 'm00' ])
        #         cy  =  int ( M [ 'm01' ] / M [ 'm00' ])
        #         tab.append(cx)
        #         tab.append(cy)
        #
        #     pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450,450]])
        #     pts1 = np.float32([[tab[6],tab[7]],[tab[4],tab[5]],[tab[2],tab[3]],[tab[0],tab[1]]])
        #     M = cv2.getPerspectiveTransform(pts1, pts2)
        #     result = cv2.warpPerspective(self.image, M, (450, 450))
        #
        #     return True, result
        # else:
        #     return False, None

        return morphology

def nothing(x):
    None# wyswietlanie wartosci w konsoli


class Red():

    def __init__(self, image):
        self.image = cv2.resize(image,(450,450))
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

        return morphology, len(contours)


cv2.namedWindow('Blue')

dobrze = 0
zle = 0


while(True):
    ret, frame = cap.read()
    rd = Red(frame)
    cv2.imshow("Blue",rd.Detect()[0])
    if rd.Detect()[1]==34:
        dobrze+=1
    else:
        zle+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("DONRZE: ", dobrze, "ZLE: ",zle)
        break
cap.release()
cv2.destroyAllWindows()