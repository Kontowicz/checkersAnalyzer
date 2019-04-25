# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dom\Desktop\ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(670, 717)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(11, 11, 641, 481))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QtWidgets.QLabel(self.widget)
        self.image_label.setEnabled(True)
        self.image_label.setFrameShape(QtWidgets.QFrame.Box)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")


        self.verticalLayout.addWidget(self.image_label)
        self.control_bt = QtWidgets.QPushButton(self.widget)
        self.control_bt.setObjectName("control_bt")
        self.verticalLayout.addWidget(self.control_bt)

        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 530, 160, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setTickInterval(1)





        self.Parametr1 = QtWidgets.QLabel(Form)
        self.Parametr1.setGeometry(QtCore.QRect(20, 510, 131, 16))
        self.Parametr1.setObjectName("Parametr1")
        self.Parametr11 = QtWidgets.QLabel(Form)
        self.Parametr11.setGeometry(QtCore.QRect(140, 510, 31, 16))
        self.Parametr11.setObjectName("Parametr11")
        # self.Biale = QtWidgets.QLabel(Form)
        # self.Biale.setGeometry(QtCore.QRect(130, 650, 55, 16))
        # self.Biale.setObjectName("Biale")
        # self.Czarne = QtWidgets.QLabel(Form)
        # self.Czarne.setGeometry(QtCore.QRect(130, 680, 55, 16))
        # self.Czarne.setObjectName("Czarne")
        # self.CzarneLiczba = QtWidgets.QLabel(Form)
        # self.CzarneLiczba.setGeometry(QtCore.QRect(200, 650, 55, 16))
        # self.CzarneLiczba.setObjectName("CzarneLiczba")
        # self.CzarneLiczba_2 = QtWidgets.QLabel(Form)
        # self.CzarneLiczba_2.setGeometry(QtCore.QRect(200, 680, 55, 16))
        # self.CzarneLiczba_2.setObjectName("CzarneLiczba_2")
        self.ChanellLog = QtWidgets.QTextBrowser(Form)
        self.ChanellLog.setGeometry(QtCore.QRect(390, 520, 256, 192))
        self.ChanellLog.setObjectName("ChanellLog")
        self.Parametr22 = QtWidgets.QLabel(Form)
        self.Parametr22.setGeometry(QtCore.QRect(360, 510, 55, 16))
        self.Parametr22.setObjectName("Parametr22")
        self.Parametr2 = QtWidgets.QLabel(Form)
        self.Parametr2.setGeometry(QtCore.QRect(200, 510, 151, 16))
        self.Parametr2.setObjectName("Parametr2")
        self.horizontalSlider_2 = QtWidgets.QSlider(Form)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(200, 530, 160, 22))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.setTickInterval(1)
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(200)

        self.max_radius1 = QtWidgets.QLabel(Form)
        self.max_radius1.setGeometry(QtCore.QRect(140, 590, 55, 16))
        self.max_radius1.setObjectName("max_radius1")
        self.max_radius = QtWidgets.QLabel(Form)
        self.max_radius.setGeometry(QtCore.QRect(20, 590, 111, 16))
        self.max_radius.setObjectName("max_radius")
        self.horizontalSlider_3 = QtWidgets.QSlider(Form)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(20, 610, 160, 22))
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_3.setMaximum(200)
        self.horizontalSlider_3.setMinimum(1)


        self.horizontalSlider_4 = QtWidgets.QSlider(Form)
        self.horizontalSlider_4.setGeometry(QtCore.QRect(200, 610, 160, 22))
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.horizontalSlider_4.setMinimum(1)
        self.horizontalSlider_4.setMaximum(99)

        self.min_radius1 = QtWidgets.QLabel(Form)
        self.min_radius1.setGeometry(QtCore.QRect(320, 590, 55, 16))
        self.min_radius1.setObjectName("min_radius1")
        self.min_radius = QtWidgets.QLabel(Form)
        self.min_radius.setGeometry(QtCore.QRect(200, 590, 121, 16))
        self.min_radius.setObjectName("min_radius")

        self.horizontalSlider.valueChanged.connect(self.v_horizontal1)

        self.horizontalSlider_2.valueChanged.connect(self.v_horizontal2)
        self.horizontalSlider_3.valueChanged.connect(self.v_horizontal3)
        self.horizontalSlider_4.valueChanged.connect(self.v_horizontal4)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def v_horizontal1(self) :
        self.Parametr11.setText(str(self.horizontalSlider.value()))

    def v_horizontal2(self):
        self.Parametr22.setText(str(self.horizontalSlider_2.value()))
    def v_horizontal3(self):
        self.max_radius1.setText(str(self.horizontalSlider_3.value()))
    def v_horizontal4(self):
        self.min_radius1.setText(str(self.horizontalSlider_4.value()))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cam view"))
        self.control_bt.setText(_translate("Form", "Start"))
        self.Parametr1.setText(_translate("Form", "Canny Treshold :"))
        self.Parametr11.setText(_translate("Form", "30"))
        # self.Biale.setText(_translate("Form", "Białe: "))
        # self.Czarne.setText(_translate("Form", "Czarne: "))
        # self.CzarneLiczba.setText(_translate("Form", "TextLabel"))
        # self.CzarneLiczba_2.setText(_translate("Form", "TextLabel"))
        self.Parametr22.setText(_translate("Form", "100"))
        self.Parametr2.setText(_translate("Form", "Center detection treshold :"))
        self.max_radius1.setText(_translate("Form", "50"))
        self.max_radius.setText(_translate("Form", "Maximum radius :"))
        self.min_radius1.setText(_translate("Form", "24"))
        self.min_radius.setText(_translate("Form", "Minimum radius:"))
        self.horizontalSlider.setValue(30)
        self.horizontalSlider_2.setValue(100)
        self.horizontalSlider_3.setValue(50)
        self.horizontalSlider_4.setValue(24)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

