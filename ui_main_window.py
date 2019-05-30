from PyQt5 import QtCore, QtGui, QtWidgets
import sys
# 641, 63, 97
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1333, 780)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(13, 13, 544, 544))
        self.widget.setObjectName("widget")

        self.widget_image = QtWidgets.QWidget(Form)
        self.widget_image.setGeometry(QtCore.QRect(570, 13, 753, 753))
        self.widget_image.setObjectName("widget_image")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.widget_image)
        self.verticalLayout2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout2.setObjectName("verticalLayout2")

        self.image_label = QtWidgets.QLabel(self.widget)
        self.image_label.setEnabled(True)
        self.image_label.setFrameShape(QtWidgets.QFrame.Box)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")

        self.image_set = QtWidgets.QLabel(self.widget_image)
        self.image_set.setEnabled(True)
        self.image_set.setFrameShape(QtWidgets.QFrame.Box)
        self.image_set.setText("")
        self.image_set.setObjectName("image_set")

        self.verticalLayout2.addWidget(self.image_set)

        self.verticalLayout.addWidget(self.image_label)
        self.control_bt = QtWidgets.QPushButton(self.widget)
        self.control_bt.setObjectName("control_bt")
        self.verticalLayout.addWidget(self.control_bt)

        self.camera_control = QtWidgets.QPushButton(self.widget)
        self.camera_control.setObjectName("camera_control")
        self.verticalLayout.addWidget(self.camera_control)

        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(130, 585, 160, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setTickInterval(1)
        self.Parametr1 = QtWidgets.QLabel(Form)
        self.Parametr1.setGeometry(QtCore.QRect(5, 585, 131, 16))
        self.Parametr1.setObjectName("Parametr1")
        self.Parametr11 = QtWidgets.QLabel(Form)
        self.Parametr11.setGeometry(QtCore.QRect(95, 585, 31, 16))
        self.Parametr11.setObjectName("Parametr11")
        self.ChanellLog = QtWidgets.QTextBrowser(Form)

        self.ChanellLog.setGeometry(QtCore.QRect(303, 580, 256, 185))
        self.ChanellLog.setObjectName("ChanellLog")

        self.Parametr22 = QtWidgets.QLabel(Form)
        self.Parametr22.setGeometry(QtCore.QRect(95, 635, 55, 16))
        self.Parametr22.setObjectName("Parametr22")
        self.Parametr2 = QtWidgets.QLabel(Form)
        self.Parametr2.setGeometry(QtCore.QRect(5, 635, 111, 16))
        self.Parametr2.setObjectName("Parametr2")
        self.horizontalSlider_2 = QtWidgets.QSlider(Form)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(130, 635, 160, 22))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.setTickInterval(1)
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(200)

        self.max_radius1 = QtWidgets.QLabel(Form)
        self.max_radius1.setGeometry(QtCore.QRect(95, 685, 55, 16))
        self.max_radius1.setObjectName("max_radius1")
        self.max_radius = QtWidgets.QLabel(Form)
        self.max_radius.setGeometry(QtCore.QRect(5, 685, 111, 16))
        self.max_radius.setObjectName("max_radius")
        self.horizontalSlider_3 = QtWidgets.QSlider(Form)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(130, 685, 160, 22))
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_3.setMaximum(200)
        self.horizontalSlider_3.setMinimum(1)



        self.horizontalSlider_4 = QtWidgets.QSlider(Form)
        self.horizontalSlider_4.setGeometry(QtCore.QRect(130, 735, 160, 22))
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.horizontalSlider_4.setMinimum(1)
        self.horizontalSlider_4.setMaximum(99)
        self.min_radius1 = QtWidgets.QLabel(Form)
        self.min_radius1.setGeometry(QtCore.QRect(95, 735, 55, 16))
        self.min_radius1.setObjectName("min_radius1")
        self.min_radius = QtWidgets.QLabel(Form)
        self.min_radius.setGeometry(QtCore.QRect(5, 735, 121, 16))
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
        self.control_bt.setText(_translate("Form", "Start analysis"))
        self.camera_control.setText(_translate("Form", "Start camera"))
        self.Parametr1.setText(_translate("Form", "Canny threshold:"))
        self.Parametr11.setText(_translate("Form", "40"))
        self.Parametr22.setText(_translate("Form", "40"))
        self.Parametr2.setText(_translate("Form", "Center threshold:"))
        self.max_radius1.setText(_translate("Form", "24"))
        self.max_radius.setText(_translate("Form", "Maximum radius:"))
        self.min_radius1.setText(_translate("Form", "20"))
        self.min_radius.setText(_translate("Form", "Minimum radius:"))
        self.horizontalSlider.setValue(40)
        self.horizontalSlider_2.setValue(40)
        self.horizontalSlider_3.setValue(24)
        self.horizontalSlider_4.setValue(20)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

