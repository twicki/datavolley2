# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zoneanalysis.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1208, 842)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_6 = QtWidgets.QFrame(Form)
        self.frame_6.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.frame_6)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.header_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.header_6.setContentsMargins(0, 0, 0, 0)
        self.header_6.setObjectName("header_6")
        self.total_6 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_6.setFont(font)
        self.total_6.setText("")
        self.total_6.setObjectName("total_6")
        self.header_6.addWidget(self.total_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_6.addItem(spacerItem)
        self.total_perc_6 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_6.setFont(font)
        self.total_perc_6.setText("")
        self.total_perc_6.setObjectName("total_perc_6")
        self.header_6.addWidget(self.total_perc_6)
        self.header_6.setStretch(0, 5)
        self.header_6.setStretch(1, 1)
        self.header_6.setStretch(2, 5)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.frame_6)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.leads_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.leads_6.setContentsMargins(0, 0, 0, 0)
        self.leads_6.setObjectName("leads_6")
        self.lead_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.lead_6.setText("")
        self.lead_6.setObjectName("lead_6")
        self.leads_6.addWidget(self.lead_6)
        self.second_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.second_6.setText("")
        self.second_6.setObjectName("second_6")
        self.leads_6.addWidget(self.second_6)
        self.third_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.third_6.setText("")
        self.third_6.setObjectName("third_6")
        self.leads_6.addWidget(self.third_6)
        self.fourth_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.fourth_6.setText("")
        self.fourth_6.setObjectName("fourth_6")
        self.leads_6.addWidget(self.fourth_6)
        self.fifth_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.fifth_6.setText("")
        self.fifth_6.setObjectName("fifth_6")
        self.leads_6.addWidget(self.fifth_6)
        self.gridLayout.addWidget(self.frame_6, 6, 2, 1, 4)
        self.action_filter_button = QtWidgets.QPushButton(Form)
        self.action_filter_button.setObjectName("action_filter_button")
        self.gridLayout.addWidget(self.action_filter_button, 0, 2, 1, 1)
        self.frame_1 = QtWidgets.QFrame(Form)
        self.frame_1.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.frame_1)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.header_1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.header_1.setContentsMargins(0, 0, 0, 0)
        self.header_1.setObjectName("header_1")
        self.total_1 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_1.setFont(font)
        self.total_1.setText("")
        self.total_1.setObjectName("total_1")
        self.header_1.addWidget(self.total_1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_1.addItem(spacerItem1)
        self.total_perc_1 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_1.setFont(font)
        self.total_perc_1.setText("")
        self.total_perc_1.setObjectName("total_perc_1")
        self.header_1.addWidget(self.total_perc_1)
        self.header_1.setStretch(0, 5)
        self.header_1.setStretch(1, 1)
        self.header_1.setStretch(2, 5)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.frame_1)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.leads_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.leads_1.setContentsMargins(0, 0, 0, 0)
        self.leads_1.setObjectName("leads_1")
        self.lead_1 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.lead_1.setText("")
        self.lead_1.setObjectName("lead_1")
        self.leads_1.addWidget(self.lead_1)
        self.second_1 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.second_1.setText("")
        self.second_1.setObjectName("second_1")
        self.leads_1.addWidget(self.second_1)
        self.third_1 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.third_1.setText("")
        self.third_1.setObjectName("third_1")
        self.leads_1.addWidget(self.third_1)
        self.fourth_1 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.fourth_1.setText("")
        self.fourth_1.setObjectName("fourth_1")
        self.leads_1.addWidget(self.fourth_1)
        self.fifth_1 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.fifth_1.setText("")
        self.fifth_1.setObjectName("fifth_1")
        self.leads_1.addWidget(self.fifth_1)
        self.gridLayout.addWidget(self.frame_1, 6, 6, 1, 2)
        self.rally_button = QtWidgets.QPushButton(Form)
        self.rally_button.setObjectName("rally_button")
        self.gridLayout.addWidget(self.rally_button, 0, 3, 1, 1)
        self.court_filter_button = QtWidgets.QPushButton(Form)
        self.court_filter_button.setObjectName("court_filter_button")
        self.gridLayout.addWidget(self.court_filter_button, 0, 4, 1, 1)
        self.reset_button = QtWidgets.QPushButton(Form)
        self.reset_button.setObjectName("reset_button")
        self.gridLayout.addWidget(self.reset_button, 1, 7, 1, 1)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.frame_2)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.header_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.header_2.setContentsMargins(0, 0, 0, 0)
        self.header_2.setObjectName("header_2")
        self.total_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_2.setFont(font)
        self.total_2.setText("")
        self.total_2.setObjectName("total_2")
        self.header_2.addWidget(self.total_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_2.addItem(spacerItem2)
        self.total_perc_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_2.setFont(font)
        self.total_perc_2.setText("")
        self.total_perc_2.setObjectName("total_perc_2")
        self.header_2.addWidget(self.total_perc_2)
        self.header_2.setStretch(0, 5)
        self.header_2.setStretch(1, 1)
        self.header_2.setStretch(2, 5)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.frame_2)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.leads_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.leads_2.setContentsMargins(0, 0, 0, 0)
        self.leads_2.setObjectName("leads_2")
        self.lead_2 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.lead_2.setText("")
        self.lead_2.setObjectName("lead_2")
        self.leads_2.addWidget(self.lead_2)
        self.second_2 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.second_2.setText("")
        self.second_2.setObjectName("second_2")
        self.leads_2.addWidget(self.second_2)
        self.third_2 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.third_2.setText("")
        self.third_2.setObjectName("third_2")
        self.leads_2.addWidget(self.third_2)
        self.fourth_2 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.fourth_2.setText("")
        self.fourth_2.setObjectName("fourth_2")
        self.leads_2.addWidget(self.fourth_2)
        self.fifth_2 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.fifth_2.setText("")
        self.fifth_2.setObjectName("fifth_2")
        self.leads_2.addWidget(self.fifth_2)
        self.gridLayout.addWidget(self.frame_2, 4, 6, 1, 2)
        self.frame_8 = QtWidgets.QFrame(Form)
        self.frame_8.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(self.frame_8)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.header_8 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.header_8.setContentsMargins(0, 0, 0, 0)
        self.header_8.setObjectName("header_8")
        self.total_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_8)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_8.setFont(font)
        self.total_8.setText("")
        self.total_8.setObjectName("total_8")
        self.header_8.addWidget(self.total_8)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_8.addItem(spacerItem3)
        self.total_perc_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_8)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_8.setFont(font)
        self.total_perc_8.setText("")
        self.total_perc_8.setObjectName("total_perc_8")
        self.header_8.addWidget(self.total_perc_8)
        self.header_8.setStretch(0, 5)
        self.header_8.setStretch(1, 1)
        self.header_8.setStretch(2, 5)
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.frame_8)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.leads_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.leads_8.setContentsMargins(0, 0, 0, 0)
        self.leads_8.setObjectName("leads_8")
        self.lead_8 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.lead_8.setText("")
        self.lead_8.setObjectName("lead_8")
        self.leads_8.addWidget(self.lead_8)
        self.second_8 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.second_8.setText("")
        self.second_8.setObjectName("second_8")
        self.leads_8.addWidget(self.second_8)
        self.third_8 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.third_8.setText("")
        self.third_8.setObjectName("third_8")
        self.leads_8.addWidget(self.third_8)
        self.fourth_8 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.fourth_8.setText("")
        self.fourth_8.setObjectName("fourth_8")
        self.leads_8.addWidget(self.fourth_8)
        self.fifth_8 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.fifth_8.setText("")
        self.fifth_8.setObjectName("fifth_8")
        self.leads_8.addWidget(self.fifth_8)
        self.gridLayout.addWidget(self.frame_8, 5, 2, 1, 4)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(10)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 8)
        self.frame_7 = QtWidgets.QFrame(Form)
        self.frame_7.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(self.frame_7)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.header_7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.header_7.setContentsMargins(0, 0, 0, 0)
        self.header_7.setObjectName("header_7")
        self.total_7 = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_7.setFont(font)
        self.total_7.setText("")
        self.total_7.setObjectName("total_7")
        self.header_7.addWidget(self.total_7)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_7.addItem(spacerItem4)
        self.total_perc_7 = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_7.setFont(font)
        self.total_perc_7.setText("")
        self.total_perc_7.setObjectName("total_perc_7")
        self.header_7.addWidget(self.total_perc_7)
        self.header_7.setStretch(0, 5)
        self.header_7.setStretch(1, 1)
        self.header_7.setStretch(2, 5)
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(self.frame_7)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.leads_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.leads_7.setContentsMargins(0, 0, 0, 0)
        self.leads_7.setObjectName("leads_7")
        self.lead_7 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.lead_7.setText("")
        self.lead_7.setObjectName("lead_7")
        self.leads_7.addWidget(self.lead_7)
        self.second_7 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.second_7.setText("")
        self.second_7.setObjectName("second_7")
        self.leads_7.addWidget(self.second_7)
        self.third_7 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.third_7.setText("")
        self.third_7.setObjectName("third_7")
        self.leads_7.addWidget(self.third_7)
        self.fourth_7 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.fourth_7.setText("")
        self.fourth_7.setObjectName("fourth_7")
        self.leads_7.addWidget(self.fourth_7)
        self.fifth_7 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.fifth_7.setText("")
        self.fifth_7.setObjectName("fifth_7")
        self.leads_7.addWidget(self.fifth_7)
        self.gridLayout.addWidget(self.frame_7, 5, 6, 1, 2)
        self.subaction_filter_button = QtWidgets.QPushButton(Form)
        self.subaction_filter_button.setObjectName("subaction_filter_button")
        self.gridLayout.addWidget(self.subaction_filter_button, 0, 5, 1, 1)
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(self.frame_3)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.header_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.header_3.setContentsMargins(0, 0, 0, 0)
        self.header_3.setObjectName("header_3")
        self.total_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_3.setFont(font)
        self.total_3.setText("")
        self.total_3.setObjectName("total_3")
        self.header_3.addWidget(self.total_3)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_3.addItem(spacerItem5)
        self.total_perc_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_3.setFont(font)
        self.total_perc_3.setText("")
        self.total_perc_3.setObjectName("total_perc_3")
        self.header_3.addWidget(self.total_perc_3)
        self.header_3.setStretch(0, 5)
        self.header_3.setStretch(1, 1)
        self.header_3.setStretch(2, 5)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.frame_3)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.leads_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.leads_3.setContentsMargins(0, 0, 0, 0)
        self.leads_3.setObjectName("leads_3")
        self.lead_3 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.lead_3.setText("")
        self.lead_3.setObjectName("lead_3")
        self.leads_3.addWidget(self.lead_3)
        self.second_3 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.second_3.setText("")
        self.second_3.setObjectName("second_3")
        self.leads_3.addWidget(self.second_3)
        self.third_3 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.third_3.setText("")
        self.third_3.setObjectName("third_3")
        self.leads_3.addWidget(self.third_3)
        self.fourth_3 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.fourth_3.setText("")
        self.fourth_3.setObjectName("fourth_3")
        self.leads_3.addWidget(self.fourth_3)
        self.fifth_3 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.fifth_3.setText("")
        self.fifth_3.setObjectName("fifth_3")
        self.leads_3.addWidget(self.fifth_3)
        self.gridLayout.addWidget(self.frame_3, 4, 2, 1, 4)
        self.load_button = QtWidgets.QPushButton(Form)
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 0, 7, 1, 1)
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_4)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.leads_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.leads_4.setContentsMargins(0, 0, 0, 0)
        self.leads_4.setObjectName("leads_4")
        self.lead_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lead_4.setText("")
        self.lead_4.setObjectName("lead_4")
        self.leads_4.addWidget(self.lead_4)
        self.second_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.second_4.setText("")
        self.second_4.setObjectName("second_4")
        self.leads_4.addWidget(self.second_4)
        self.third_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.third_4.setText("")
        self.third_4.setObjectName("third_4")
        self.leads_4.addWidget(self.third_4)
        self.fourth_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.fourth_4.setText("")
        self.fourth_4.setObjectName("fourth_4")
        self.leads_4.addWidget(self.fourth_4)
        self.fifth_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.fifth_4.setText("")
        self.fifth_4.setObjectName("fifth_4")
        self.leads_4.addWidget(self.fifth_4)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame_4)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.header_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.header_4.setContentsMargins(0, 0, 0, 0)
        self.header_4.setObjectName("header_4")
        self.total_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_4.setFont(font)
        self.total_4.setText("")
        self.total_4.setObjectName("total_4")
        self.header_4.addWidget(self.total_4)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_4.addItem(spacerItem6)
        self.total_perc_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_4.setFont(font)
        self.total_perc_4.setText("")
        self.total_perc_4.setObjectName("total_perc_4")
        self.header_4.addWidget(self.total_perc_4)
        self.header_4.setStretch(0, 5)
        self.header_4.setStretch(1, 1)
        self.header_4.setStretch(2, 5)
        self.gridLayout.addWidget(self.frame_4, 4, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.frame_5 = QtWidgets.QFrame(Form)
        self.frame_5.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.frame_5)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.header_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.header_5.setContentsMargins(0, 0, 0, 0)
        self.header_5.setObjectName("header_5")
        self.total_5 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_5.setFont(font)
        self.total_5.setText("")
        self.total_5.setObjectName("total_5")
        self.header_5.addWidget(self.total_5)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_5.addItem(spacerItem7)
        self.total_perc_5 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_5.setFont(font)
        self.total_perc_5.setText("")
        self.total_perc_5.setObjectName("total_perc_5")
        self.header_5.addWidget(self.total_perc_5)
        self.header_5.setStretch(0, 5)
        self.header_5.setStretch(1, 1)
        self.header_5.setStretch(2, 5)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame_5)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.leads_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.leads_5.setContentsMargins(0, 0, 0, 0)
        self.leads_5.setObjectName("leads_5")
        self.lead_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.lead_5.setText("")
        self.lead_5.setObjectName("lead_5")
        self.leads_5.addWidget(self.lead_5)
        self.second_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.second_5.setText("")
        self.second_5.setObjectName("second_5")
        self.leads_5.addWidget(self.second_5)
        self.third_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.third_5.setText("")
        self.third_5.setObjectName("third_5")
        self.leads_5.addWidget(self.third_5)
        self.fourth_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.fourth_5.setText("")
        self.fourth_5.setObjectName("fourth_5")
        self.leads_5.addWidget(self.fourth_5)
        self.fifth_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.fifth_5.setText("")
        self.fifth_5.setObjectName("fifth_5")
        self.leads_5.addWidget(self.fifth_5)
        self.gridLayout.addWidget(self.frame_5, 6, 0, 1, 1)
        self.filter_table = QtWidgets.QTableWidget(Form)
        self.filter_table.setObjectName("filter_table")
        self.filter_table.setColumnCount(0)
        self.filter_table.setRowCount(0)
        self.gridLayout.addWidget(self.filter_table, 2, 0, 1, 8)
        self.frame_9 = QtWidgets.QFrame(Form)
        self.frame_9.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayoutWidget_9 = QtWidgets.QWidget(self.frame_9)
        self.horizontalLayoutWidget_9.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.horizontalLayoutWidget_9.setObjectName("horizontalLayoutWidget_9")
        self.header_9 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_9)
        self.header_9.setContentsMargins(0, 0, 0, 0)
        self.header_9.setObjectName("header_9")
        self.total_9 = QtWidgets.QLabel(self.horizontalLayoutWidget_9)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_9.setFont(font)
        self.total_9.setText("")
        self.total_9.setObjectName("total_9")
        self.header_9.addWidget(self.total_9)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_9.addItem(spacerItem8)
        self.total_perc_9 = QtWidgets.QLabel(self.horizontalLayoutWidget_9)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_9.setFont(font)
        self.total_perc_9.setText("")
        self.total_perc_9.setObjectName("total_perc_9")
        self.header_9.addWidget(self.total_perc_9)
        self.header_9.setStretch(0, 5)
        self.header_9.setStretch(1, 1)
        self.header_9.setStretch(2, 5)
        self.verticalLayoutWidget_9 = QtWidgets.QWidget(self.frame_9)
        self.verticalLayoutWidget_9.setGeometry(QtCore.QRect(10, 60, 251, 141))
        self.verticalLayoutWidget_9.setObjectName("verticalLayoutWidget_9")
        self.leads_9 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_9)
        self.leads_9.setContentsMargins(0, 0, 0, 0)
        self.leads_9.setObjectName("leads_9")
        self.lead_9 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.lead_9.setText("")
        self.lead_9.setObjectName("lead_9")
        self.leads_9.addWidget(self.lead_9)
        self.second_9 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.second_9.setText("")
        self.second_9.setObjectName("second_9")
        self.leads_9.addWidget(self.second_9)
        self.third_9 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.third_9.setText("")
        self.third_9.setObjectName("third_9")
        self.leads_9.addWidget(self.third_9)
        self.fourth_9 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.fourth_9.setText("")
        self.fourth_9.setObjectName("fourth_9")
        self.leads_9.addWidget(self.fourth_9)
        self.fifth_9 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.fifth_9.setText("")
        self.fifth_9.setObjectName("fifth_9")
        self.leads_9.addWidget(self.fifth_9)
        self.gridLayout.addWidget(self.frame_9, 5, 0, 1, 1)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setStyleSheet("background-color: rgb(48, 136, 145);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget_10 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_10.setGeometry(QtCore.QRect(20, 10, 251, 31))
        self.horizontalLayoutWidget_10.setObjectName("horizontalLayoutWidget_10")
        self.header_10 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_10)
        self.header_10.setContentsMargins(0, 0, 0, 0)
        self.header_10.setObjectName("header_10")
        self.total_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_10)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_10.setFont(font)
        self.total_10.setText("")
        self.total_10.setObjectName("total_10")
        self.header_10.addWidget(self.total_10)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_10.addItem(spacerItem9)
        self.total_perc_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_10)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.total_perc_10.setFont(font)
        self.total_perc_10.setText("")
        self.total_perc_10.setObjectName("total_perc_10")
        self.header_10.addWidget(self.total_perc_10)
        self.header_10.setStretch(0, 5)
        self.header_10.setStretch(1, 1)
        self.header_10.setStretch(2, 5)
        self.horizontalLayoutWidget_11 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_11.setGeometry(QtCore.QRect(290, 10, 831, 31))
        self.horizontalLayoutWidget_11.setObjectName("horizontalLayoutWidget_11")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_11)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lead_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_11)
        self.lead_10.setText("")
        self.lead_10.setObjectName("lead_10")
        self.horizontalLayout.addWidget(self.lead_10)
        self.second_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_11)
        self.second_10.setText("")
        self.second_10.setObjectName("second_10")
        self.horizontalLayout.addWidget(self.second_10)
        self.third_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_11)
        self.third_10.setText("")
        self.third_10.setObjectName("third_10")
        self.horizontalLayout.addWidget(self.third_10)
        self.fourth_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_11)
        self.fourth_10.setText("")
        self.fourth_10.setObjectName("fourth_10")
        self.horizontalLayout.addWidget(self.fourth_10)
        self.fifth_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_11)
        self.fifth_10.setText("")
        self.fifth_10.setObjectName("fifth_10")
        self.horizontalLayout.addWidget(self.fifth_10)
        self.gridLayout.addWidget(self.frame, 7, 0, 1, 8)
        self.gridLayout.setColumnStretch(0, 8)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 2)
        self.gridLayout.setColumnStretch(5, 2)
        self.gridLayout.setColumnStretch(6, 6)
        self.gridLayout.setColumnStretch(7, 2)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 12)
        self.gridLayout.setRowStretch(5, 12)
        self.gridLayout.setRowStretch(6, 12)
        self.gridLayout.setRowStretch(7, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.action_filter_button.setText(_translate("Form", "ActionFilter"))
        self.rally_button.setText(_translate("Form", "RallyFilter"))
        self.court_filter_button.setText(_translate("Form", "CourtFilter"))
        self.reset_button.setText(_translate("Form", "Reset"))
        self.subaction_filter_button.setText(_translate("Form", "SubactionFilter"))
        self.load_button.setText(_translate("Form", "Load File"))
