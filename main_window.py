from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import cv2

from ui_main_window import *
import checkersAnalyzer as ca
from moveDetect import moveDetect as md
from checkersDetect import checkersDetect as cd

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.Analysis = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.ui.control_bt.clicked.connect(self.controlTimer)
        self.ui.camera_control.clicked.connect(self.StartCamera)

    def viewCam(self):
            ret, frame = self.cap.read()
            cD = cd(frame)
            detect, image = cD.Detect()
            if self.Analysis:
                if detect:
                    mD = md(image)
                    if mD.Detect():
                        analyzer = ca.checkersAnalyzer(False, image)
                        analyzer.param1 = int(self.ui.Parametr11.text())
                        analyzer.param2 = int(self.ui.Parametr22.text())
                        analyzer.max_rad = int(self.ui.max_radius1.text())
                        analyzer.min_rad = int(self.ui.min_radius1.text())

                        try:
                            analyzer.detectCircle()
                        except Exception as E:
                            self.ui.ChanellLog.append(str(E))
                        board = analyzer.drawBoard()

                        qImg = QImage(board[0], 714, 714, 2142, QImage.Format_RGB888)
                        qImg2 = QImage(board[2], 544, 544, 1632, QImage.Format_RGB888)
                        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
                        self.ui.image_label.setScaledContents(True)
                        self.ui.image_set.setPixmap(QPixmap.fromImage(qImg2))
                        self.ui.image_set.setScaledContents(True)
                #else:
                    #qImg = QImage(cv2.resize(image,(544,544)), 544, 544, 1632, QImage.Format_RGB888)
                    #self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
                    #self.ui.image_label.setScaledContents(True)
            else:
                qImg = QImage(cv2.resize(frame,(544,544)), 544, 544, 1632, QImage.Format_RGB888)
                self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
                self.ui.image_label.setScaledContents(True)

    def controlTimer(self):
        if not self.Analysis:
            if self.timer.isActive():
                self.ui.control_bt.setText("Stop analysis")
                self.Analysis = not self.Analysis
        else:
            if self.timer.isActive():
                self.ui.control_bt.setText("Start analysis")
                self.Analysis = not self.Analysis
                self.ui.ChanellLog.clear()


    def StartCamera(self):
        if not self.timer.isActive():
            self.ui.camera_control.setText("Stop camera")
            self.cap = cv2.VideoCapture(1)
            self.timer.start(20)
        else:
            self.ui.camera_control.setText("Start camera")
            self.cap.release()
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())