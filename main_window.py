from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import cv2

from ui_main_window import *
import checkersAnalyzer as ca

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.ui.control_bt.clicked.connect(self.controlTimer)

    def viewCam(self):
        ret, image = self.cap.read()

        analyzer = ca.checkersAnalyzer(False, image)

        analyzer.param1 = int(self.ui.Parametr11.text())
        analyzer.param2 = int(self.ui.Parametr22.text())
        analyzer.max_rad = int(self.ui.max_radius1.text())
        analyzer.min_rad = int(self.ui.min_radius1.text())
        analyzer.detectCircle()
        analyzer.drawTextInImageText()

        board = analyzer.drawBoard()

        qImg = QImage(board[2].data, 544, 544, 1632, QImage.Format_RGB888)
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
        self.ui.image_label.setScaledContents(True)

    def controlTimer(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture('Picture/movie2.mp4')
            self.timer.start(20)
            self.ui.control_bt.setText("Stop")
        else:
            self.timer.stop()
            self.cap.release()
            self.ui.control_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())