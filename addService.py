# -*- coding: utf-8 -*-

# Modal window to add an OTP

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(400, 179)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 120, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 321, 80))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(5, 5, 5, 0)
        self.formLayout.setObjectName("formLayout")

        # Name of service
        self.labelService = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelService.setObjectName("labelService")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelService)
        self.lineService = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineService.setObjectName("lineService")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineService)
       
        # Service's OTP
        self.labelOTP = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelOTP.setObjectName("labelOTP")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelOTP)
       
        self.lineOTP = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineOTP.setObjectName("lineOTP")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineOTP)

        self.retranslateUi(Dialog)
        
        # Accept button adds an OTP
        self.buttonBox.accepted.connect(Dialog.accept)
        #self.buttonBox.accepted.connect(self.insertKey)

        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Service"))
        self.labelService.setText(_translate("Dialog", "ID de servicio"))
        self.labelOTP.setText(_translate("Dialog", "Código"))
