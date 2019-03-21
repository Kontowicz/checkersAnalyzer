import checkersAnalyzer as ca
import cv2

#TODO: https://www.jetbrains.com/help/pycharm/viewing-reference-information.html

if __name__ == '__main__':
    a = ord('a')
    cap = cv2.VideoCapture('Picture/movie2.mp4')
    ret, frame = cap.read()
    analyzer = ca.checkersAnalyzer(False, frame)
    while (cap.isOpened() and a!=ord('q')):
        analyzer.detectCircle()
        analyzer.drawTextInImageText()
        board = analyzer.drawBoard()
        cv2.imshow('Plansza', board[0])
        cv2.imshow('Zaznaczone pionki', board[1])
        cv2.imshow('Wizualizacja', board[2])
        ret, frame = cap.read()
        analyzer.readVideo(frame)
        a = cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()