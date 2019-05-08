import cv2
import numpy as np

def f():
    class boardDetect():
        img_base = cv2.resize(cv2.imread("DetectBoard/1.jpg", cv2.IMREAD_COLOR),(0,0), fx=0.2, fy=0.2)
        img_gray_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
        img_copy = img_base.copy()


        img_find = cv2.resize(cv2.imread("DetectBoard/default.jpg",cv2.IMREAD_GRAYSCALE),(0,0), fx=0.2, fy=0.2)
        w, h = img_find.shape[::-1]
        res = cv2.matchTemplate(img_gray_base, img_find, cv2.TM_CCOEFF_NORMED)
        a = 0.3
        b = np.where(res >= a)

        for pt in zip(*b[::-1]):
            cv2.rectangle(img_copy, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)

        key = ord('a')
        while key != ord('q'):
            cv2.imshow("Znaleziony", img_copy)
            cv2.imshow("find", img_find)
            cv2.imshow("first", img_base)
            key = cv2.waitKey(0)

def zad1():
    # wczytanie obrazu
    img1 = cv2.resize(cv2.imread("DetectBoard/default.jpg",cv2.IMREAD_COLOR),(0,0), fx=0.2, fy=0.2)
    # pobranie wymiarow
    # w, h, b = img1.shape
    # tworzenie macierzy do translacji
    # M = cv2.getRotationMatrix2D((h / 2, w / 2), 90, 1)
    # obraz obruzony o 90
    img2 = cv2.resize(cv2.imread("DetectBoard/1.jpg", cv2.IMREAD_COLOR),(0,0), fx=0.2, fy=0.2)
    # tworzenie detektora fast
    # fast = cv2.FastFeatureDetector_create()
    # tworzenie detektora ORB ograniczenie do 50 cech punktowych
    ORB = cv2.ORB_create(nfeatures=50)
    # szukanie cech punktowych fast
    # KP1 = fast.detect(img1,None)
    # KP2 = fast.detect(img2,None)
    # szukanie cech punktowych ORB
    kp1 = ORB.detect(img1, None)
    kp2 = ORB.detect(img2, None)
    # tworzenie deskryptorow fast
    # KP1, DES1 = fast.compute(img1,KP1)
    # KP2, DES2 = fast.compute(img2, KP2)
    # tworzenie deskryptorow ORB
    kp1, des1 = ORB.compute(img1, kp1)
    kp2, des2 = ORB.compute(img2, kp2)
    # tworzenie obiektu dopasowania
    BFM = cv2.BFMatcher(cv2.NORM_HAMMING)
    # szukanie dopasowan fast
    # matches2 = BFM.match(DES1, DES2)
    # szukanie dopasowan ORB
    matches = BFM.match(des1, des2)
    # rysowanie dopasowan ORB
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, None)
    # rysowanie dopasowan fast
    # img4 = cv2.drawMatches(img1,KP1, img2,KP2 ,matches2, None)

    key = ord('a')
    while key != ord('q'):
        cv2.imshow("Dopasowania orb", img3)
        # cv2.imshow("Dopasowania fast", img4)
        key = cv2.waitKey(0)


if __name__ == "__main__":
    zad1()