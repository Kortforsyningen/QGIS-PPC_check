# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PPC_check_dialog_base.ui'
#
# Created: Thu Apr 07 08:55:58 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PPC_checkDialogBase(object):
    def setupUi(self, PPC_checkDialogBase):
        PPC_checkDialogBase.setObjectName(_fromUtf8("PPC_checkDialogBase"))
        PPC_checkDialogBase.resize(393, 424)
        self.button_box = QtGui.QDialogButtonBox(PPC_checkDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 370, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.groupBox_2 = QtGui.QGroupBox(PPC_checkDialogBase)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 371, 91))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.inShapeA = QtGui.QComboBox(self.groupBox_2)
        self.inShapeA.setGeometry(QtCore.QRect(20, 20, 331, 22))
        self.inShapeA.setObjectName(_fromUtf8("inShapeA"))
        self.useSelectedA = QtGui.QCheckBox(self.groupBox_2)
        self.useSelectedA.setGeometry(QtCore.QRect(30, 60, 181, 17))
        self.useSelectedA.setObjectName(_fromUtf8("useSelectedA"))
        self.groupBox = QtGui.QGroupBox(PPC_checkDialogBase)
        self.groupBox.setGeometry(QtCore.QRect(10, 160, 371, 201))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.checkBoxGSD = QtGui.QCheckBox(self.groupBox)
        self.checkBoxGSD.setGeometry(QtCore.QRect(20, 80, 111, 17))
        self.checkBoxGSD.setObjectName(_fromUtf8("checkBoxGSD"))
        self.checkBoxSun = QtGui.QCheckBox(self.groupBox)
        self.checkBoxSun.setGeometry(QtCore.QRect(20, 113, 70, 16))
        self.checkBoxSun.setObjectName(_fromUtf8("checkBoxSun"))
        self.lineEditGSD = QtGui.QLineEdit(self.groupBox)
        self.lineEditGSD.setGeometry(QtCore.QRect(100, 80, 51, 20))
        self.lineEditGSD.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditGSD.setObjectName(_fromUtf8("lineEditGSD"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(160, 81, 46, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEditSUN = QtGui.QLineEdit(self.groupBox)
        self.lineEditSUN.setGeometry(QtCore.QRect(100, 110, 51, 20))
        self.lineEditSUN.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditSUN.setObjectName(_fromUtf8("lineEditSUN"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(160, 110, 46, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.checkBoxTilt = QtGui.QCheckBox(self.groupBox)
        self.checkBoxTilt.setGeometry(QtCore.QRect(20, 143, 70, 17))
        self.checkBoxTilt.setObjectName(_fromUtf8("checkBoxTilt"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(160, 140, 46, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEditTilt = QtGui.QLineEdit(self.groupBox)
        self.lineEditTilt.setGeometry(QtCore.QRect(100, 139, 51, 21))
        self.lineEditTilt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditTilt.setObjectName(_fromUtf8("lineEditTilt"))
        self.lineEditRef = QtGui.QLineEdit(self.groupBox)
        self.lineEditRef.setGeometry(QtCore.QRect(140, 170, 161, 20))
        self.lineEditRef.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditRef.setObjectName(_fromUtf8("lineEditRef"))
        self.checkBoxRef = QtGui.QCheckBox(self.groupBox)
        self.checkBoxRef.setGeometry(QtCore.QRect(20, 173, 111, 17))
        self.checkBoxRef.setObjectName(_fromUtf8("checkBoxRef"))
        self.checkBoxFile = QtGui.QCheckBox(self.groupBox)
        self.checkBoxFile.setGeometry(QtCore.QRect(20, 20, 231, 17))
        self.checkBoxFile.setObjectName(_fromUtf8("checkBoxFile"))
        self.checkBoxFormat = QtGui.QCheckBox(self.groupBox)
        self.checkBoxFormat.setGeometry(QtCore.QRect(20, 50, 241, 17))
        self.checkBoxFormat.setObjectName(_fromUtf8("checkBoxFormat"))
        self.label_3 = QtGui.QLabel(PPC_checkDialogBase)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 101, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton_Input = QtGui.QPushButton(PPC_checkDialogBase)
        self.pushButton_Input.setGeometry(QtCore.QRect(348, 120, 31, 21))
        self.pushButton_Input.setObjectName(_fromUtf8("pushButton_Input"))
        self.lineEditCam = QtGui.QLineEdit(PPC_checkDialogBase)
        self.lineEditCam.setGeometry(QtCore.QRect(120, 120, 221, 21))
        self.lineEditCam.setObjectName(_fromUtf8("lineEditCam"))

        self.retranslateUi(PPC_checkDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), PPC_checkDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), PPC_checkDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(PPC_checkDialogBase)

    def retranslateUi(self, PPC_checkDialogBase):
        PPC_checkDialogBase.setWindowTitle(_translate("PPC_checkDialogBase", "PPC_check", None))
        self.groupBox_2.setTitle(_translate("PPC_checkDialogBase", "PPC file", None))
        self.useSelectedA.setText(_translate("PPC_checkDialogBase", "Use only selected features", None))
        self.groupBox.setTitle(_translate("PPC_checkDialogBase", "To be checked", None))
        self.checkBoxGSD.setText(_translate("PPC_checkDialogBase", "GSD", None))
        self.checkBoxSun.setText(_translate("PPC_checkDialogBase", "Sun angle", None))
        self.lineEditGSD.setText(_translate("PPC_checkDialogBase", "0.1", None))
        self.label.setText(_translate("PPC_checkDialogBase", "meters", None))
        self.lineEditSUN.setText(_translate("PPC_checkDialogBase", "25", None))
        self.label_2.setText(_translate("PPC_checkDialogBase", "Degrees", None))
        self.checkBoxTilt.setText(_translate("PPC_checkDialogBase", "Tilt", None))
        self.label_6.setText(_translate("PPC_checkDialogBase", "Degrees", None))
        self.lineEditTilt.setText(_translate("PPC_checkDialogBase", "5", None))
        self.lineEditRef.setText(_translate("PPC_checkDialogBase", "ETRS89,UTM32N,DVR90", None))
        self.checkBoxRef.setText(_translate("PPC_checkDialogBase", "Reference system:", None))
        self.checkBoxFile.setText(_translate("PPC_checkDialogBase", "File format conforms to SDFE Standard", None))
        self.checkBoxFormat.setText(_translate("PPC_checkDialogBase", "Feature format conforms to SDFE Standard", None))
        self.label_3.setText(_translate("PPC_checkDialogBase", "Path to camera dir:", None))
        self.pushButton_Input.setText(_translate("PPC_checkDialogBase", "...", None))

