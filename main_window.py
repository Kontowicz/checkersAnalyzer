"""
In this example, we demonstrate how to create simple camera viewer using Opencv3 and PyQt5

Author: Berrouba.A
Last edited: 21 Feb 2018
"""

# import system module
import time
import sys
import numpy as np

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
import checkersDetect as cd
import moveDetect as md

im2 = []


class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('Picture/kont.jpg'))
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.start = True

        # create a timer

        #self.cap = cv2.VideoCapture(1)
        self.timer = QTimer()
        # self.analyzer = ca.checkersAnalyzer(True, cv2.resize(cd.checkersDetect(self.cap.read()).Detect()[1], (544, 544)))
        self.analyzer = []
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)

        self.ui.pushButton.clicked.connect(self.clearChanellLog)

    def clearChanellLog(self):
        self.ui.ChanellLog.setText("")

    # view camera

    def viewCam(self):
        isread = 1;
        # read image in BGR format
        try:
            ret, image = self.cap.read()
        except Exception as E:
            self.ui.ChanellLog.append("could not read ")
        # moveDetector = md.moveDetect(image)
        # if moveDetector.Detect():


        if image is not None:
            img2 = image.copy()
            image = cv2.resize(image, (544, 544))
            # wynik mały
            bytesPerLine5 = 3 * 311

            # lewy górny
            try:
                height, width, channel = image.shape
                bytesPerLine = 3 * width
                qImg7 = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
                self.ui.image_label_7.setPixmap(QPixmap.fromImage(qImg7))
                self.ui.image_label_7.setScaledContents(True)
            except Exception as E:
                pass

        try:
            detector = cd.checkersDetect(img2)
            ret, img2 = detector.Detect()
            isread = 1;
        except Exception as E:
            pass

        if ( img2 is not None):

            if (self.start):
                self.analyzer = ca.checkersAnalyzer(False, img2)
                self.start = False
            else:
                self.analyzer.readVideo(img2)


            # parametry się zmieniają
            self.analyzer.param1 = int(self.ui.Parametr11.text())
            self.analyzer.param2 = int(self.ui.Parametr22.text())
            self.analyzer.max = int(self.ui.max_radius1.text())
            self.analyzer.min = int(self.ui.min_radius1.text())

            # while (cap.isOpened() and a!=ord('q')):

            x = 1
            try:
                if self.ui.checkBox.isChecked():
                    self.analyzer.detectCircle(True)
                    self.analyzer.checkMove()
                else:
                    self.analyzer.detectCircle(False)
            except Exception as E:
                self.ui.ChanellLog.append("ERROR")

            try:
                board = self.analyzer.drawBoard()
                biale, czarne = self.analyzer.currentStateBoard.countPawns()
                self.ui.CzarneLiczba.setText(str(biale))
                self.ui.CzarneLiczba_2.setText(str(czarne))
                isread = 0;
            except Exception as E:
                pass

            # QtCore.QCoreApplication.processEvents()

            # Główny duży
            step = 3 * 544
            try:
                qImg = QImage(board[2].data, 544, 544, step, QImage.Format_RGB888)
                self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
                self.ui.image_label.setScaledContents(True)
            except Exception as E:
                pass

            try:
                # prawy górny

                height, width, channel = image.shape
                bytesPerLine = 3 * width
                qImg4 = QImage(img2.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
                self.ui.image_label_6.setPixmap(QPixmap.fromImage(qImg4))
                self.ui.image_label_6.setScaledContents(True)
            except Exception as E:
                pass

            # lewy dolny
            try:
                height1, width1, channel1 = board[0].shape
                bytesPerLine1 = 3 * width1
                qImg6 = QImage(board[0].data, width1, height1, bytesPerLine1, QImage.Format_RGB888).rgbSwapped()
                self.ui.image_label_4.setPixmap(QPixmap.fromImage(qImg6))
                self.ui.image_label_4.setScaledContents(True)
            except Exception as E:
                pass

            # prawy dolny
            try:
                qImg5 = QImage(cv2.resize(board[2], (311, 301)).data, 311, 301, bytesPerLine5,
                               QImage.Format_RGB888).rgbSwapped()
                self.ui.image_label_5.setPixmap(QPixmap.fromImage(qImg5))
                self.ui.image_label_5.setScaledContents(True)
            except Exception as E:
                pass

    # start/stop timer

    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(1)
            # start timer
            self.timer.start(100)
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
    global num_previous
    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())