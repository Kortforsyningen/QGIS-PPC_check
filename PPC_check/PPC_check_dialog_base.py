# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PPC_check_dialog_base.ui'
#
# Created: Tue Mar 06 08:30:07 2018
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
        PPC_checkDialogBase.resize(467, 516)
        self.lineEditCamDir = QtGui.QLineEdit(PPC_checkDialogBase)
        self.lineEditCamDir.setGeometry(QtCore.QRect(150, 110, 251, 21))
        self.lineEditCamDir.setObjectName(_fromUtf8("lineEditCamDir"))
        self.labelCamDir = QtGui.QLabel(PPC_checkDialogBase)
        self.labelCamDir.setGeometry(QtCore.QRect(20, 110, 151, 21))
        self.labelCamDir.setObjectName(_fromUtf8("labelCamDir"))
        self.pushButton_InputPPC = QtGui.QPushButton(PPC_checkDialogBase)
        self.pushButton_InputPPC.setGeometry(QtCore.QRect(420, 110, 31, 21))
        self.pushButton_InputPPC.setObjectName(_fromUtf8("pushButton_InputPPC"))
        self.groupBox_2 = QtGui.QGroupBox(PPC_checkDialogBase)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 441, 91))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.inShapeAPPC = QtGui.QComboBox(self.groupBox_2)
        self.inShapeAPPC.setGeometry(QtCore.QRect(20, 20, 401, 22))
        self.inShapeAPPC.setObjectName(_fromUtf8("inShapeAPPC"))
        self.useSelectedAPPC = QtGui.QCheckBox(self.groupBox_2)
        self.useSelectedAPPC.setGeometry(QtCore.QRect(20, 60, 181, 17))
        self.useSelectedAPPC.setObjectName(_fromUtf8("useSelectedAPPC"))
        self.radioButtonPPC_ob = QtGui.QRadioButton(self.groupBox_2)
        self.radioButtonPPC_ob.setGeometry(QtCore.QRect(230, 60, 91, 17))
        self.radioButtonPPC_ob.setObjectName(_fromUtf8("radioButtonPPC_ob"))
        self.radioButtonPPC_Nadir = QtGui.QRadioButton(self.groupBox_2)
        self.radioButtonPPC_Nadir.setGeometry(QtCore.QRect(340, 60, 82, 17))
        self.radioButtonPPC_Nadir.setObjectName(_fromUtf8("radioButtonPPC_Nadir"))
        self.groupBox = QtGui.QGroupBox(PPC_checkDialogBase)
        self.groupBox.setGeometry(QtCore.QRect(10, 150, 441, 311))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.checkBoxGSD = QtGui.QCheckBox(self.groupBox)
        self.checkBoxGSD.setGeometry(QtCore.QRect(20, 110, 111, 17))
        self.checkBoxGSD.setObjectName(_fromUtf8("checkBoxGSD"))
        self.checkBoxSun = QtGui.QCheckBox(self.groupBox)
        self.checkBoxSun.setGeometry(QtCore.QRect(20, 143, 101, 16))
        self.checkBoxSun.setObjectName(_fromUtf8("checkBoxSun"))
        self.lineEditGSD = QtGui.QLineEdit(self.groupBox)
        self.lineEditGSD.setGeometry(QtCore.QRect(180, 110, 51, 20))
        self.lineEditGSD.setText(_fromUtf8(""))
        self.lineEditGSD.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditGSD.setObjectName(_fromUtf8("lineEditGSD"))
        self.labelGSD = QtGui.QLabel(self.groupBox)
        self.labelGSD.setGeometry(QtCore.QRect(240, 111, 61, 20))
        self.labelGSD.setObjectName(_fromUtf8("labelGSD"))
        self.lineEditSUN = QtGui.QLineEdit(self.groupBox)
        self.lineEditSUN.setGeometry(QtCore.QRect(180, 140, 51, 20))
        self.lineEditSUN.setText(_fromUtf8(""))
        self.lineEditSUN.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditSUN.setObjectName(_fromUtf8("lineEditSUN"))
        self.labelSun = QtGui.QLabel(self.groupBox)
        self.labelSun.setGeometry(QtCore.QRect(240, 140, 71, 20))
        self.labelSun.setObjectName(_fromUtf8("labelSun"))
        self.checkBoxTilt = QtGui.QCheckBox(self.groupBox)
        self.checkBoxTilt.setGeometry(QtCore.QRect(20, 173, 70, 17))
        self.checkBoxTilt.setObjectName(_fromUtf8("checkBoxTilt"))
        self.labelTilt = QtGui.QLabel(self.groupBox)
        self.labelTilt.setGeometry(QtCore.QRect(240, 170, 61, 20))
        self.labelTilt.setObjectName(_fromUtf8("labelTilt"))
        self.lineEditTilt = QtGui.QLineEdit(self.groupBox)
        self.lineEditTilt.setGeometry(QtCore.QRect(180, 169, 51, 21))
        self.lineEditTilt.setText(_fromUtf8(""))
        self.lineEditTilt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditTilt.setObjectName(_fromUtf8("lineEditTilt"))
        self.lineEditRef = QtGui.QLineEdit(self.groupBox)
        self.lineEditRef.setGeometry(QtCore.QRect(170, 200, 161, 20))
        self.lineEditRef.setText(_fromUtf8(""))
        self.lineEditRef.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditRef.setObjectName(_fromUtf8("lineEditRef"))
        self.checkBoxRef = QtGui.QCheckBox(self.groupBox)
        self.checkBoxRef.setGeometry(QtCore.QRect(20, 203, 151, 17))
        self.checkBoxRef.setObjectName(_fromUtf8("checkBoxRef"))
        self.checkBoxFile = QtGui.QCheckBox(self.groupBox)
        self.checkBoxFile.setGeometry(QtCore.QRect(20, 50, 411, 17))
        self.checkBoxFile.setObjectName(_fromUtf8("checkBoxFile"))
        self.checkBoxFormat = QtGui.QCheckBox(self.groupBox)
        self.checkBoxFormat.setGeometry(QtCore.QRect(20, 80, 401, 17))
        self.checkBoxFormat.setObjectName(_fromUtf8("checkBoxFormat"))
        self.checkBoxPic = QtGui.QCheckBox(self.groupBox)
        self.checkBoxPic.setGeometry(QtCore.QRect(20, 20, 381, 17))
        self.checkBoxPic.setObjectName(_fromUtf8("checkBoxPic"))
        self.checkBoxVoids = QtGui.QCheckBox(self.groupBox)
        self.checkBoxVoids.setGeometry(QtCore.QRect(20, 230, 231, 17))
        self.checkBoxVoids.setObjectName(_fromUtf8("checkBoxVoids"))
        self.button_box = QtGui.QDialogButtonBox(PPC_checkDialogBase)
        self.button_box.setGeometry(QtCore.QRect(110, 470, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))

        self.retranslateUi(PPC_checkDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), PPC_checkDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), PPC_checkDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(PPC_checkDialogBase)

    def retranslateUi(self, PPC_checkDialogBase):
        PPC_checkDialogBase.setWindowTitle(_translate("PPC_checkDialogBase", "PPC_check", None))
        self.labelCamDir.setText(_translate("PPC_checkDialogBase", "Path to camera dir:", None))
        self.pushButton_InputPPC.setText(_translate("PPC_checkDialogBase", "...", None))
        self.groupBox_2.setTitle(_translate("PPC_checkDialogBase", "PPC or footprint file", None))
        self.useSelectedAPPC.setText(_translate("PPC_checkDialogBase", "Use only selected features", None))
        self.radioButtonPPC_ob.setText(_translate("PPC_checkDialogBase", "Oblique", None))
        self.radioButtonPPC_Nadir.setText(_translate("PPC_checkDialogBase", "Nadir", None))
        self.groupBox.setTitle(_translate("PPC_checkDialogBase", "To be checked", None))
        self.checkBoxGSD.setText(_translate("PPC_checkDialogBase", "GSD", None))
        self.checkBoxSun.setText(_translate("PPC_checkDialogBase", "Sun angle", None))
        self.labelGSD.setText(_translate("PPC_checkDialogBase", "Meters", None))
        self.labelSun.setText(_translate("PPC_checkDialogBase", "Degrees", None))
        self.checkBoxTilt.setText(_translate("PPC_checkDialogBase", "Tilt", None))
        self.labelTilt.setText(_translate("PPC_checkDialogBase", "Degrees", None))
        self.checkBoxRef.setText(_translate("PPC_checkDialogBase", "Reference system:", None))
        self.checkBoxFile.setText(_translate("PPC_checkDialogBase", "File format conforms to SDFE Standard", None))
        self.checkBoxFormat.setText(_translate("PPC_checkDialogBase", "Feature format conforms to SDFE Standard", None))
        self.checkBoxPic.setText(_translate("PPC_checkDialogBase", "Check image naming", None))
        self.checkBoxVoids.setText(_translate("PPC_checkDialogBase", "Footprint Void Check", None))

