# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_team.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(713, 558)
        self.Teamname = QtWidgets.QLineEdit(Form)
        self.Teamname.setGeometry(QtCore.QRect(50, 20, 621, 25))
        self.Teamname.setObjectName("Teamname")
        self.table = QtWidgets.QTableWidget(Form)
        self.table.setGeometry(QtCore.QRect(40, 90, 631, 192))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.minus = QtWidgets.QPushButton(Form)
        self.minus.setGeometry(QtCore.QRect(619, 290, 21, 25))
        self.minus.setObjectName("minus")
        self.plus = QtWidgets.QPushButton(Form)
        self.plus.setGeometry(QtCore.QRect(640, 290, 31, 21))
        self.plus.setObjectName("plus")
        self.save = QtWidgets.QPushButton(Form)
        self.save.setGeometry(QtCore.QRect(560, 340, 89, 25))
        self.save.setObjectName("save")
        self.HC = QtWidgets.QLineEdit(Form)
        self.HC.setGeometry(QtCore.QRect(170, 310, 113, 25))
        self.HC.setObjectName("HC")
        self.AC = QtWidgets.QLineEdit(Form)
        self.AC.setGeometry(QtCore.QRect(170, 340, 113, 25))
        self.AC.setObjectName("AC")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(76, 310, 81, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(50, 340, 111, 20))
        self.label_2.setObjectName("label_2")
        self.load = QtWidgets.QPushButton(Form)
        self.load.setGeometry(QtCore.QRect(560, 370, 89, 25))
        self.load.setObjectName("load")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.minus.setText(_translate("Form", "-"))
        self.plus.setText(_translate("Form", "+"))
        self.save.setText(_translate("Form", "Save"))
        self.label.setText(_translate("Form", "Head Coach"))
        self.label_2.setText(_translate("Form", "Assistant Coach"))
        self.load.setText(_translate("Form", "Load"))
