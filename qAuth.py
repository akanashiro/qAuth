#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import os
import sqlite3
import time

# Rutas
#sys.path.append(".")

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox, QLineEdit, QFileDialog

from addService import Ui_Dialog

# This class syncs timer with progress bar
class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    def run(self):          
        nbrCount = 0
        while nbrCount < TIME_LIMIT:
            nbrCount += 1
            time.sleep(1)
            self.countChanged.emit(nbrCount)

# Main window class
class Ui_qAuthClass(object):


    def onCountChanged(self, aValue):
        """
        Increases % in progress bar.
        When counter reaches to 100 then the OTP are re-read.
        """

        # As time counter is set to 30 seconds, I solved doing this division
        # Any better way?
        self.remainingTime.setValue(aValue*100/30)
        
        # will look for a better way to reset it
        if aValue == 30:

            self.build2FA(True)

            # This reload of data prevents recently added new data not being showed
            # when timer resets. Should check for a more performant way to do this
            # self.loadData() 

    
    def return2FA(self, aKey):
        """
        Generates Time-based One-time Password using oathtool
        """
        cmdAuth = "oathtool -b --totp '" + aKey +"'"
        out2FA = os.popen(cmdAuth).read()
        return out2FA.rstrip()
    
    def build2FA(self, boolReset):
        """
        Generates Time-based One-time Password
        """

        for intRow in range(int(self.tblKeys.rowCount())):

            strOTPhidden = self.tblKeys.item(intRow,3)
            strOTP = self.tblKeys.item(intRow,1)
            

            str2FA = self.return2FA(strOTP.text()) 
            self.tblKeys.setItem(intRow, 2, QtWidgets.QTableWidgetItem(str(str2FA)))
            #col = self.tblKeys.item(intRow, 2)
            #col.setText(str2FA)
            self.tblKeys.item(intRow,2).setTextAlignment(QtCore.Qt.AlignCenter)

            strOTP.setText("*********")

        # As the counter is using threads, this boolean prevents counter going crazy
        # when adding other accounts before the counter gets reset
        if boolReset:
            # Resets remaining time
            self.remainingTime.setProperty("value", 0)

            # Calls function to increase time
            self.calc = External()
            self.calc.countChanged.connect(self.onCountChanged)
            self.calc.start()  


    def loadData(self):

        global dbPath

        connQauth = sqlite3.connect(dbPath)
        strQuery = "SELECT strServicio, strOTP from keys"
        resultQuery = connQauth.execute(strQuery)
        
        # fill table
        self.tblKeys.setRowCount(0)
        for row_number, row_data in enumerate(resultQuery):
            self.tblKeys.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                #self.tblKeys.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                
                if column_number == 0:
                    self.tblKeys.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(data)))
                if column_number == 1:
                    print(str(data))
                    self.tblKeys.setItem(row_number, 1, QtWidgets.QTableWidgetItem(str(data)))
                    self.tblKeys.setItem(row_number, 3, QtWidgets.QTableWidgetItem(str(data)))

         # close connection
        connQauth.close()
        
        # Generates Time-based One-time Password
        self.build2FA(True)

    # File Dialog box
    def callOpenDialog(self):
        """
        Opens a keys database
        """

        self.openFileNamesDialog()

    def openFileNamesDialog(self, dir=None):
        """
        Opens file name dialog
        """

        if dir is None:
            dir = './'

        fname = QFileDialog.getOpenFileName(None, "Open Database...",
                                            dir, filter="Sqlite DB (*.db)")

        if fname:
            self.setDBName(fname[0])

    def setDBName(self, aFilename):
        """
        Sets database name
        """
        global dbPath

        srcFile = aFilename.split("/")[-1]
        srcFolder = aFilename.split(srcFile, 1)[0]
        lenSplit = len(srcFolder.split("/")) - 2


        # Base de datos
        #BASE_DIR = srcFolder
        dbPath = os.path.join(srcFolder, srcFile)
        #print (srcFile)
        #print ("directorio " + srcFolder)
        self.loadData()
       

    def insertKey(self, anArrayData):
        """
        Inserts OTP to database
        """
        global dbPath

        connOTP = sqlite3.connect(dbPath)

        # SQL file
        strFileName = BASE_DIR + "insert_key.sql"
        fd = open(strFileName, 'r')
        sqlFile = fd.read()
        fd.close()
        
        # Inserts OTP
        cur = connOTP.cursor()
        cur.execute(sqlFile, anArrayData)
        connOTP.commit()

        cur.close()


    # Remove OTP
    def removeOTP(self):

        """
        Deletes OTP from database
        """

        global dbPath

        # Current row
        intCurrRow = self.tblKeys.currentRow()
        print("current row " + str(intCurrRow))
        
        strService = self.tblKeys.item(intCurrRow,0)
        strOTP = self.tblKeys.item(intCurrRow,3)
        anArrayData = (strService.text(), strOTP.text())

        print(strService.text())
        print(strOTP.text())
        connOTP = sqlite3.connect(dbPath)

        # SQL file
        strFileName = BASE_DIR + "delete_key.sql"
        fd = open(strFileName, 'r')
        sqlFile = fd.read()
        fd.close()

        # Deletes OTP
        cur = connOTP.cursor()
        cur.execute(sqlFile, (anArrayData))
        connOTP.commit()

        cur.close()

        self.tblKeys.removeRow(intCurrRow)

    def showOTP(self):
        """
        Shows/Hides OTP
        """
        for intRow in range(int(self.tblKeys.rowCount())):

            strOTPhidden = self.tblKeys.item(intRow,3)
            strOTP = self.tblKeys.item(intRow,1)

            if not strOTP.text() == "*********":
                strOTP.setText("*********")
            else:
                #if strOTP.text() == "*********":
                strOTP.setText(strOTPhidden.text())


    def addService(self):
        """
        Calls a pop-up window to add a new OTP
        """
        
        popAddService = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(popAddService)
        popAddService.show()
        result = popAddService.exec_()

        if result == QtWidgets.QDialog.Accepted:

            # Catches entered values
            strService =  ui.lineService.text()
            strOTP = ui.lineOTP.text()

            # And inserts into database
            arrayData = (strService, strOTP)
            self.insertKey(arrayData)

            # Add a new row with entered values
            intRow = int(self.tblKeys.rowCount())
            self.tblKeys.insertRow(intRow)
            self.tblKeys.setItem(intRow, 0, QtWidgets.QTableWidgetItem(str(strService).upper()))
            self.tblKeys.setItem(intRow, 1, QtWidgets.QTableWidgetItem(str(strOTP).upper()))

            # Generates Time-based One-time Password for all files again
            self.build2FA(False)

    # About Dialog
    def showAbout(self):
        aboutBox = QtWidgets.QMessageBox()
        aboutBox.about(qAuthClass, "About", "Agustín Kanashiro - 2020<br/>"
                       "<a href=\"https://github.com/akanashiro/qAuth\">Github qAuth</a>")
    
    def setupUi(self, qAuthClass):
        qAuthClass.setObjectName("qAuthClass")
        qAuthClass.resize(700, 365)
        
        self.centralwidget = QtWidgets.QWidget(qAuthClass)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, -1, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # ************** TABLE **************
        self.tblKeys = QtWidgets.QTableWidget(self.centralwidget)
        self.tblKeys.setMaximumSize(QtCore.QSize(540, 16777215))
        self.tblKeys.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.tblKeys.setColumnCount(4)
        self.tblKeys.setObjectName("tblKeys")
        self.tblKeys.setRowCount(0)
        self.tblKeys.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblKeys.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tblKeys.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
   
        # Column Definition: Service
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        self.tblKeys.setHorizontalHeaderItem(0, item)
        self.tblKeys.setColumnWidth(0,200)
        
        # Column Definition: OTP
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        self.tblKeys.setHorizontalHeaderItem(1, item)
        self.tblKeys.setColumnWidth(1,180)
       
        # Column Definition: 2FA
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tblKeys.setHorizontalHeaderItem(2, item)
        self.tblKeys.setColumnWidth(2,70)

        # Column Definition: OTP 2 (hidden)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        self.tblKeys.setHorizontalHeaderItem(3, item)
        self.tblKeys.setColumnWidth(3,10)

        # Hide OTP 2
        self.tblKeys.hideColumn(3)

        # Remove Button
        #item = QtWidgets.QTableWidgetItem()
        #item.setTextAlignment(QtCore.Qt.AlignRight)
        #self.tblKeys.setHorizontalHeaderItem(3, item)
        #self.tblKeys.setColumnWidth(3,50)

        self.horizontalLayout.addWidget(self.tblKeys)
        
       # spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
       # self.horizontalLayout.addItem(spacerItem)
        
        self.verticalGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.verticalGroupBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout_3.setContentsMargins(5, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # remaining time
        self.timeLayout = QtWidgets.QHBoxLayout()
        self.timeLayout.setObjectName("timeLayout")
        self.timeLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.remainingTime = QtWidgets.QProgressBar(self.verticalGroupBox)
        self.remainingTime.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.remainingTime.setProperty("value", 0)
        self.remainingTime.setAlignment(QtCore.Qt.AlignCenter)
        self.remainingTime.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.remainingTime.setObjectName("remainingTime")
        self.timeLayout.addWidget(self.remainingTime,0)

        self.verticalLayout_3.addLayout(self.timeLayout)
        
        # Buttons Layout
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setObjectName("buttonsLayout")
        
        # Add OTP Pushbutton
        self.btn_Add = QtWidgets.QPushButton(self.verticalGroupBox)
        self.btn_Add.setObjectName("btn_Add")        
        self.btn_Add.setMaximumWidth(34)
        self.btn_Add.setIcon(QtGui.QIcon.fromTheme('list-add-symbolic'))        
        self.buttonsLayout.addWidget(self.btn_Add)
        self.btn_Add.clicked.connect(self.addService)

        # Remove OTP button
        self.removeButton = QtWidgets.QPushButton(self.verticalGroupBox)
        #self.removeButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.removeButton.setObjectName("removeButton")
        self.removeButton.setMaximumWidth(34)
        self.removeButton.setIcon(QtGui.QIcon.fromTheme('edit-delete-symbolic'))        
        self.buttonsLayout.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.removeOTP)

        # Show Pushbutton
        self.showButton = QtWidgets.QPushButton(self.verticalGroupBox)
        self.showButton.setObjectName("showButton")     
        self.showButton.setMaximumWidth(34)
        self.showButton.setIcon(QtGui.QIcon.fromTheme('view-visible'))        
        self.buttonsLayout.addWidget(self.showButton)
        self.showButton.clicked.connect(self.showOTP)

        # Clipboard Pushbutton
        # is it necessary?

        self.verticalLayout_3.addLayout(self.buttonsLayout)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)

        self.horizontalLayout.addWidget(self.verticalGroupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        qAuthClass.setCentralWidget(self.centralwidget)


        # ************** MENU **************
        self.menubar = QtWidgets.QMenuBar(qAuthClass)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 535, 26))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        qAuthClass.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(qAuthClass)
        self.statusbar.setObjectName("statusbar")
        qAuthClass.setStatusBar(self.statusbar)

        # Force reloading all data
        self.openDB = QtWidgets.QAction(qAuthClass)
        self.openDB.setObjectName("openDB")
        self.openDB.triggered.connect(self.callOpenDialog)
        self.menuFile.addAction(self.openDB)

        # About
        self.aboutAction = QtWidgets.QAction(qAuthClass)
        self.aboutAction.setObjectName("aboutAction")
        self.aboutAction.triggered.connect(self.showAbout)
        self.menuFile.addAction(self.aboutAction)

        # Quit
        self.actionQuit = QtWidgets.QAction(qAuthClass)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(qAuthClass)

        self.actionQuit.triggered.connect(qAuthClass.close)
        
        QtCore.QMetaObject.connectSlotsByName(qAuthClass)

        #self.loadData()


    def retranslateUi(self, qAuthClass):
        _translate = QtCore.QCoreApplication.translate
        qAuthClass.setWindowTitle(_translate("qAuthClass", "qAuth - 2 Steps Authentication"))
        
        # Columns
        item = self.tblKeys.horizontalHeaderItem(0)
        item.setText(_translate("qAuthClass", "Service Name"))
        
        item = self.tblKeys.horizontalHeaderItem(1)
        item.setText(_translate("qAuthClass", "OTP"))
        
        item = self.tblKeys.horizontalHeaderItem(2)
        item.setText(_translate("qAuthClass", "2FA"))

        #item = self.tblKeys.horizontalHeaderItem(3)
        #item.setText(_translate("qAuthClass", ""))
        
        # Buttons
        # self.btn_load.setText(_translate("qAuthClass", "Cargar"))
        #self.btn_Add.setText(_translate("qAuthClass", "Agregar"))

        # Menu
        self.menuFile.setTitle(_translate("qAuthClass", "Fi&le"))
        self.openDB.setText(_translate("qAuthClass", "&Open database"))
        self.aboutAction.setText(_translate("qAuthClass", "&About"))
        self.actionQuit.setText(_translate("qAuthClass", "&Quit"))

 
if __name__ == "__main__":

    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/db/"
    #dbPath = os.path.join(BASE_DIR, "qauth.db")
    global dbPath

    # Time limit
    TIME_LIMIT = 30

    app = QtWidgets.QApplication(sys.argv)
    qAuthClass = QtWidgets.QMainWindow()
    ui = Ui_qAuthClass()
    ui.setupUi(qAuthClass)
    qAuthClass.show()
     
    sys.exit(app.exec_())
