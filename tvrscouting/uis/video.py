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
        Dialog.resize(1127, 893)
        self.gridLayout_4 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 3, 1, 1)
        self.horizontalSlider_2 = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.gridLayout.addWidget(self.horizontalSlider_2, 0, 10, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.lcdNumber = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(6)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setProperty("value", 0.0)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridLayout.addWidget(self.lcdNumber, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.saveFile_button = QtWidgets.QPushButton(Dialog)
        self.saveFile_button.setObjectName("saveFile_button")
        self.gridLayout.addWidget(self.saveFile_button, 1, 10, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.load_button = QtWidgets.QPushButton(Dialog)
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 1, 6, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 8, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 7, 1, 3)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 2)
        self.gridLayout.setColumnStretch(5, 1)
        self.gridLayout.setColumnStretch(6, 2)
        self.gridLayout.setColumnStretch(8, 1)
        self.gridLayout.setColumnStretch(9, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 9, 0, 1, 1)
        self.filter_table = QtWidgets.QTableWidget(Dialog)
        self.filter_table.setObjectName("filter_table")
        self.filter_table.setColumnCount(0)
        self.filter_table.setRowCount(0)
        self.gridLayout_3.addWidget(self.filter_table, 3, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.court_filter_button = QtWidgets.QPushButton(Dialog)
        self.court_filter_button.setObjectName("court_filter_button")
        self.gridLayout_2.addWidget(self.court_filter_button, 0, 1, 1, 1)
        self.action_filter_button = QtWidgets.QPushButton(Dialog)
        self.action_filter_button.setObjectName("action_filter_button")
        self.gridLayout_2.addWidget(self.action_filter_button, 0, 0, 1, 1)
        self.reset_time_button = QtWidgets.QPushButton(Dialog)
        self.reset_time_button.setObjectName("reset_time_button")
        self.gridLayout_2.addWidget(self.reset_time_button, 2, 0, 1, 1)
        self.reset_button = QtWidgets.QPushButton(Dialog)
        self.reset_button.setObjectName("reset_button")
        self.gridLayout_2.addWidget(self.reset_button, 2, 1, 1, 1)
        self.subaction_filter_button = QtWidgets.QPushButton(Dialog)
        self.subaction_filter_button.setObjectName("subaction_filter_button")
        self.gridLayout_2.addWidget(self.subaction_filter_button, 1, 1, 1, 1)
        self.rally_button = QtWidgets.QPushButton(Dialog)
        self.rally_button.setObjectName("rally_button")
        self.gridLayout_2.addWidget(self.rally_button, 1, 0, 1, 1)
        self.jump_on_select_box = QtWidgets.QCheckBox(Dialog)
        self.jump_on_select_box.setChecked(False)
        self.jump_on_select_box.setObjectName("jump_on_select_box")
        self.gridLayout_2.addWidget(self.jump_on_select_box, 3, 1, 1, 1)
        self.action_reel_box = QtWidgets.QCheckBox(Dialog)
        self.action_reel_box.setChecked(False)
        self.action_reel_box.setObjectName("action_reel_box")
        self.gridLayout_2.addWidget(self.action_reel_box, 3, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 1, 1, 1)
        self.widget = QVideoWidget(Dialog)
        self.widget.setObjectName("widget")
        self.gridLayout_3.addWidget(self.widget, 0, 0, 8, 1)
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setMaximum(10000)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_3.addWidget(self.horizontalSlider, 8, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.insert_action = QtWidgets.QPushButton(Dialog)
        self.insert_action.setObjectName("insert_action")
        self.gridLayout_5.addWidget(self.insert_action, 0, 1, 1, 1)
        self.delete_action = QtWidgets.QPushButton(Dialog)
        self.delete_action.setObjectName("delete_action")
        self.gridLayout_5.addWidget(self.delete_action, 1, 1, 1, 1)
        self.hideactions = QtWidgets.QCheckBox(Dialog)
        self.hideactions.setChecked(True)
        self.hideactions.setObjectName("hideactions")
        self.gridLayout_5.addWidget(self.hideactions, 2, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_5, 9, 1, 1, 1)
        self.action_view = QtWidgets.QTableWidget(Dialog)
        self.action_view.setObjectName("action_view")
        self.action_view.setColumnCount(0)
        self.action_view.setRowCount(0)
        self.gridLayout_3.addWidget(self.action_view, 4, 1, 5, 1)
        self.gridLayout_3.setColumnStretch(0, 10)
        self.gridLayout_3.setRowStretch(0, 1)
        self.gridLayout_3.setRowStretch(2, 1)
        self.gridLayout_3.setRowStretch(3, 2)
        self.gridLayout_3.setRowStretch(4, 1)
        self.gridLayout_3.setRowStretch(5, 1)
        self.gridLayout_3.setRowStretch(6, 8)
        self.gridLayout_4.addLayout(self.gridLayout_3, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Video Analysis"))
        self.pushButton_3.setText(_translate("Dialog", "Start Timer"))
        self.pushButton_2.setText(_translate("Dialog", "Play"))
        self.saveFile_button.setText(_translate("Dialog", "Save File"))
        self.pushButton.setText(_translate("Dialog", "Open Video"))
        self.load_button.setText(_translate("Dialog", "Load File"))
        self.label.setText(_translate("Dialog", "Volume"))
        self.court_filter_button.setText(_translate("Dialog", "Court Filter"))
        self.action_filter_button.setText(_translate("Dialog", "Action Filter"))
        self.reset_time_button.setText(_translate("Dialog", "Leadup Time"))
        self.reset_button.setText(_translate("Dialog", "Reset Filters"))
        self.subaction_filter_button.setText(_translate("Dialog", "Subaction Filter"))
        self.rally_button.setText(_translate("Dialog", "Rally Filter"))
        self.jump_on_select_box.setText(_translate("Dialog", "jump on select"))
        self.action_reel_box.setText(_translate("Dialog", "view action reel"))
        self.insert_action.setText(_translate("Dialog", "Insert Action"))
        self.delete_action.setText(_translate("Dialog", "Delete Action"))
        self.hideactions.setText(_translate("Dialog", "hide non-game actions"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
