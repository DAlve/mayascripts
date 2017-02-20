# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\davea\Desktop\test.ui'
#
# Created: Mon Feb 20 22:17:19 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from Qt.QtCore import * 
from Qt.QtGui import *
from Qt.QtWidgets import *
#from Qt import QtCore
#from Qt import QtGui

try:
    from PySide2.QtCore import SIGNAL
    from PySide2 import QtGui
except:
    from PySide.QtCore import SIGNAL

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setGeometry(QRect(100, 90, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        #QObject.connect(self.buttonBox, SIGNAL("accepted()"), Dialog.accept)
        #QObject.connect(self.buttonBox, SIGNAL("rejected()"), Dialog.reject)
        #QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Test", None, QtGui.QApplication.UnicodeUTF8))

