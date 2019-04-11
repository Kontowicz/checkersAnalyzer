import checkersAnalyzer as ca
import cv2

if __name__ == '__main__':
    a = ord('a')
    cap = cv2.VideoCapture('Picture/output.mp4')
    ret, frame = cap.read()
    counter = 0
    analyzer = ca.checkersAnalyzer(True, frame)
    while (cap.isOpened() and a!=ord('q')):
        if counter == 25:
            counter = 0
            analyzer.detectCircle()
            analyzer.drawTextInImageText()
            board = analyzer.drawBoard()
            cv2.imshow('Plansza', board[0])
            cv2.imshow('Zaznaczone pionki', board[1])
            cv2.imshow('Wizualizacja', board[2])
        counter += 1
        ret, frame = cap.read()
        analyzer.readVideo(frame)
        a = cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()