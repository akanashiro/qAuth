# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_qAuthClass(object):
    def setupUi(self, qAuthClass):
        qAuthClass.setObjectName("qAuthClass")
        qAuthClass.resize(535, 365)
        self.centralwidget = QtWidgets.QWidget(qAuthClass)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, -1, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tblKeys = QtWidgets.QTableWidget(self.centralwidget)
        self.tblKeys.setMaximumSize(QtCore.QSize(500, 16777215))
        self.tblKeys.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.tblKeys.setColumnCount(6)
        self.tblKeys.setObjectName("tblKeys")
        self.tblKeys.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblKeys.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblKeys.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblKeys.setHorizontalHeaderItem(2, item)
        self.horizontalLayout.addWidget(self.tblKeys)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.verticalGroupBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout_3.setContentsMargins(5, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.remainingTime = QtWidgets.QProgressBar(self.verticalGroupBox)
        self.remainingTime.setMaximumSize(QtCore.QSize(100, 16777215))
        self.remainingTime.setProperty("value", 24)
        self.remainingTime.setAlignment(QtCore.Qt.AlignCenter)
        self.remainingTime.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.remainingTime.setObjectName("remainingTime")
        self.verticalLayout_3.addWidget(self.remainingTime)
        self.pushButton = QtWidgets.QPushButton(self.verticalGroupBox)
        self.pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalGroupBox)
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.verticalGroupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        qAuthClass.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(qAuthClass)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 535, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        qAuthClass.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(qAuthClass)
        self.statusbar.setObjectName("statusbar")
        qAuthClass.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(qAuthClass)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(qAuthClass)
        self.actionQuit.triggered.connect(qAuthClass.close)
        QtCore.QMetaObject.connectSlotsByName(qAuthClass)

    def retranslateUi(self, qAuthClass):
        _translate = QtCore.QCoreApplication.translate
        qAuthClass.setWindowTitle(_translate("qAuthClass", "MainWindow"))
        item = self.tblKeys.horizontalHeaderItem(0)
        item.setText(_translate("qAuthClass", "Servicio"))
        item = self.tblKeys.horizontalHeaderItem(1)
        item.setText(_translate("qAuthClass", "OTP"))
        item = self.tblKeys.horizontalHeaderItem(2)
        item.setText(_translate("qAuthClass", "Código 2FA"))
        self.pushButton.setText(_translate("qAuthClass", "Agregar"))
        self.pushButton_2.setText(_translate("qAuthClass", "Quitar"))
        self.menuFile.setTitle(_translate("qAuthClass", "Fi&le"))
        self.actionQuit.setText(_translate("qAuthClass", "&Quit"))

    def insertKeys(self, aConnection):
        strService = input ("Servicio: ")
        strOTP = input("Ingresar llave: " )

        arrayData = (strService, strOTP)

        # Archivo SQL
        strFileName = BASE_DIR + "insert_key.sql"

        # Open and read the file as a single buffer
        fd = open(strFileName, 'r')
        sqlFile = fd.read()
        fd.close()
        
        cur = aConnection.cursor()

        cur.execute(sqlFile, arrayData)
        aConnection.commit()

        lastRowId = cur.lastrowid

        cur.close()

        #return lastRowId


    def getKey(self, aConnection, aIdService):
        """
        Devuelve la llave
        """

        cur = aConnection.cursor()
        cur.execute ("SELECT strOTP FROM keys WHERE idServicio = ?", (aIdService,)) 

        dataServiceKey = cur.fetchone()
        
        if dataServiceKey is None:
            return None
        else:
            strOutKey = dataServiceKey[0]  # Comuna

        cur.close()
        return strOutKey

    def getIdServicio(self, aConnection, aService):
        """
        Devuelve id de Servicio
        """

        cur = aConnection.cursor()
        cur.execute ("SELECT idServicio FROM keys WHERE UPPER(strServicio) = ?", (aService.upper(),)) 

        dataIdServicio = cur.fetchone()
        
        if dataIdServicio is None:
            return None
        else:
            nbrOutId = dataIdServicio[0]  # Comuna

        cur.close()
        return nbrOutId

    def return2FA(self, aKey):
        """
        Imprime valor 2FA dependiendo de una llave
        """
        cmdAuth = "oathtool -b --totp '" + aKey +"'"
        out2FA = os.popen(cmdAuth).read()
        return out2FA

    def print2FA(self):
        strServicio = input ("Servicio a autenticar: ")
        nbrIdServicio = getIdServicio(connQauth, strServicio)

        strKey = getKey(connQauth, nbrIdServicio)
        print(return2FA(strKey))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    qAuthClass = QtWidgets.QMainWindow()
    ui = Ui_qAuthClass()
    ui.setupUi(qAuthClass)
    qAuthClass.show()
    sys.exit(app.exec_())
