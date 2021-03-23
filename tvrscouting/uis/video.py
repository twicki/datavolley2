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
        Dialog.resize(1000, 817)
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
        self.saveFile_button = QtWidgets.QPushButton(Dialog)
        self.saveFile_button.setObjectName("saveFile_button")
        self.gridLayout.addWidget(self.saveFile_button, 0, 6, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.load_button = QtWidgets.QPushButton(Dialog)
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 0, 4, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setColumnStretch(6, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 6, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.court_filter_button = QtWidgets.QPushButton(Dialog)
        self.court_filter_button.setObjectName("court_filter_button")
        self.gridLayout_2.addWidget(self.court_filter_button, 0, 1, 1, 1)
        self.rally_button = QtWidgets.QPushButton(Dialog)
        self.rally_button.setObjectName("rally_button")
        self.gridLayout_2.addWidget(self.rally_button, 1, 0, 1, 1)
        self.action_reel_box = QtWidgets.QCheckBox(Dialog)
        self.action_reel_box.setChecked(True)
        self.action_reel_box.setObjectName("action_reel_box")
        self.gridLayout_2.addWidget(self.action_reel_box, 3, 0, 1, 2)
        self.reset_time_button = QtWidgets.QPushButton(Dialog)
        self.reset_time_button.setObjectName("reset_time_button")
        self.gridLayout_2.addWidget(self.reset_time_button, 2, 0, 1, 1)
        self.subaction_filter_button = QtWidgets.QPushButton(Dialog)
        self.subaction_filter_button.setObjectName("subaction_filter_button")
        self.gridLayout_2.addWidget(self.subaction_filter_button, 1, 1, 1, 1)
        self.action_filter_button = QtWidgets.QPushButton(Dialog)
        self.action_filter_button.setObjectName("action_filter_button")
        self.gridLayout_2.addWidget(self.action_filter_button, 0, 0, 1, 1)
        self.reset_button = QtWidgets.QPushButton(Dialog)
        self.reset_button.setObjectName("reset_button")
        self.gridLayout_2.addWidget(self.reset_button, 2, 1, 1, 1)
        self.jump_on_select_box = QtWidgets.QCheckBox(Dialog)
        self.jump_on_select_box.setChecked(True)
        self.jump_on_select_box.setObjectName("jump_on_select_box")
        self.gridLayout_2.addWidget(self.jump_on_select_box, 4, 0, 1, 2)
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
        Dialog.setWindowTitle(_translate("Dialog", "Video Analysis"))
        self.saveFile_button.setText(_translate("Dialog", "Save File"))
        self.pushButton_2.setText(_translate("Dialog", "Play"))
        self.load_button.setText(_translate("Dialog", "Load File"))
        self.pushButton.setText(_translate("Dialog", "Open Video"))
        self.court_filter_button.setText(_translate("Dialog", "Court Filter"))
        self.rally_button.setText(_translate("Dialog", "Rally Filter"))
        self.action_reel_box.setText(_translate("Dialog", "view action reel"))
        self.reset_time_button.setText(_translate("Dialog", "Leadup Time"))
        self.subaction_filter_button.setText(_translate("Dialog", "Subaction Filter"))
        self.action_filter_button.setText(_translate("Dialog", "Action Filter"))
        self.reset_button.setText(_translate("Dialog", "Reset Filters"))
        self.jump_on_select_box.setText(_translate("Dialog", "jump on select"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
