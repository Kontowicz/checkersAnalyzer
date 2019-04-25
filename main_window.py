"""
In this example, we demonstrate how to create simple camera viewer using Opencv3 and PyQt5

Author: Berrouba.A
Last edited: 21 Feb 2018
"""

# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
# import Opencv module
import cv2

from ui_main_window import *
import checkersAnalyzer as ca

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format


        analyzer = ca.checkersAnalyzer(False, image)


        analyzer.param1 = int(self.ui.Parametr11.text())
        analyzer.param2 = int(self.ui.Parametr22.text())
        analyzer.max_rad = int(self.ui.max_radius1.text())
        analyzer.min_rad = int(self.ui.min_radius1.text())
        # while (cap.isOpened() and a!=ord('q')):
        analyzer.detectCircle()
        analyzer.drawTextInImageText()




        board = analyzer.drawBoard()


        # get image infos
        height, width, channel = board[2].shape
        step = channel * width
        # create QImage from image


        qImg = QImage(board[2].data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
        self.ui.image_label.setScaledContents(True)

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture('Picture/movie2.mp4')
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())