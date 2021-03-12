# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(899, 752)
        self.gridLayout_4 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setMaximum(10000)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_3.addWidget(self.horizontalSlider, 5, 0, 1, 1)
        self.widget = QVideoWidget(Dialog)
        self.widget.setObjectName("widget")
        self.gridLayout_3.addWidget(self.widget, 0, 0, 5, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 0, 2, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.loadFile_button = QtWidgets.QPushButton(Dialog)
        self.loadFile_button.setObjectName("loadFile_button")
        self.gridLayout.addWidget(self.loadFile_button, 0, 4, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.saveFile_button = QtWidgets.QPushButton(Dialog)
        self.saveFile_button.setObjectName("saveFile_button")
        self.gridLayout.addWidget(self.saveFile_button, 0, 6, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 5, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 12)
        self.gridLayout.setColumnStretch(4, 2)
        self.gridLayout.setColumnStretch(6, 2)
        self.gridLayout_3.addLayout(self.gridLayout, 6, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.add_contain_filter = QtWidgets.QPushButton(Dialog)
        self.add_contain_filter.setObjectName("add_contain_filter")
        self.gridLayout_2.addWidget(self.add_contain_filter, 1, 1, 1, 1)
        self.reset_filters = QtWidgets.QPushButton(Dialog)
        self.reset_filters.setObjectName("reset_filters")
        self.gridLayout_2.addWidget(self.reset_filters, 2, 1, 1, 1)
        self.add_action_filter = QtWidgets.QPushButton(Dialog)
        self.add_action_filter.setObjectName("add_action_filter")
        self.gridLayout_2.addWidget(self.add_action_filter, 0, 0, 1, 1)
        self.apply_filters_button = QtWidgets.QPushButton(Dialog)
        self.apply_filters_button.setObjectName("apply_filters_button")
        self.gridLayout_2.addWidget(self.apply_filters_button, 2, 0, 1, 1)
        self.add_court_filter = QtWidgets.QPushButton(Dialog)
        self.add_court_filter.setObjectName("add_court_filter")
        self.gridLayout_2.addWidget(self.add_court_filter, 0, 1, 1, 1)
        self.add_rally_filter = QtWidgets.QPushButton(Dialog)
        self.add_rally_filter.setObjectName("add_rally_filter")
        self.gridLayout_2.addWidget(self.add_rally_filter, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget, 4, 2, 3, 1)
        self.filter_table = QtWidgets.QTableWidget(Dialog)
        self.filter_table.setObjectName("filter_table")
        self.filter_table.setColumnCount(0)
        self.filter_table.setRowCount(0)
        self.gridLayout_3.addWidget(self.filter_table, 3, 2, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 10)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.gridLayout_3.setRowStretch(0, 1)
        self.gridLayout_3.setRowStretch(2, 1)
        self.gridLayout_3.setRowStretch(3, 1)
        self.gridLayout_3.setRowStretch(4, 10)
        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.loadFile_button.setText(_translate("Dialog", "load file"))
        self.pushButton.setText(_translate("Dialog", "open video"))
        self.saveFile_button.setText(_translate("Dialog", "save file"))
        self.pushButton_2.setText(_translate("Dialog", "pause"))
        self.add_contain_filter.setText(_translate("Dialog", "SubActionFilter"))
        self.reset_filters.setText(_translate("Dialog", "Reset Filters"))
        self.add_action_filter.setText(_translate("Dialog", "ActionFilter"))
        self.apply_filters_button.setText(_translate("Dialog", "Apply Filters"))
        self.add_court_filter.setText(_translate("Dialog", "CourtFilter"))
        self.add_rally_filter.setText(_translate("Dialog", "RallyFilter"))
from PyQt5.QtMultimediaWidgets import QVideoWidget