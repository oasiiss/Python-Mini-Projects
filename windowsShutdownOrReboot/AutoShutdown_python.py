# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Huawei/Desktop/windows Auto Shutdown or Reboot/AutoShutdown.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(319, 154)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButtonReboot = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonReboot.setChecked(False)
        self.radioButtonReboot.setObjectName("radioButtonReboot")
        self.horizontalLayout.addWidget(self.radioButtonReboot)
        self.radioButtonShutdown = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonShutdown.setChecked(True)
        self.radioButtonShutdown.setObjectName("radioButtonShutdown")
        self.horizontalLayout.addWidget(self.radioButtonShutdown)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName("timeEdit")
        self.horizontalLayout_2.addWidget(self.timeEdit)
        self.ApplyBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ApplyBtn.setObjectName("ApplyBtn")
        self.horizontalLayout_2.addWidget(self.ApplyBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.lblStat = QtWidgets.QLabel(self.centralwidget)
        self.lblStat.setText("")
        self.lblStat.setAlignment(QtCore.Qt.AlignCenter)
        self.lblStat.setObjectName("lblStat")
        self.verticalLayout.addWidget(self.lblStat)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Auto Shutdown or Reboot"))
        self.radioButtonReboot.setText(_translate("MainWindow", "Reboot"))
        self.radioButtonShutdown.setText(_translate("MainWindow", "Shutdown"))
        self.ApplyBtn.setText(_translate("MainWindow", "apply"))

