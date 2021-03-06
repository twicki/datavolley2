# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'playeranalysis.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1206, 842)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.action_filter_button = QtWidgets.QPushButton(Form)
        self.action_filter_button.setObjectName("action_filter_button")
        self.gridLayout.addWidget(self.action_filter_button, 0, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bar6 = QtWidgets.QProgressBar(Form)
        self.bar6.setProperty("value", 10)
        self.bar6.setOrientation(QtCore.Qt.Vertical)
        self.bar6.setObjectName("bar6")
        self.gridLayout_2.addWidget(self.bar6, 0, 5, 1, 1)
        self.name1 = QtWidgets.QLabel(Form)
        self.name1.setObjectName("name1")
        self.gridLayout_2.addWidget(self.name1, 1, 0, 1, 1)
        self.bar2 = QtWidgets.QProgressBar(Form)
        self.bar2.setProperty("value", 20)
        self.bar2.setOrientation(QtCore.Qt.Vertical)
        self.bar2.setObjectName("bar2")
        self.gridLayout_2.addWidget(self.bar2, 0, 1, 1, 1)
        self.name2 = QtWidgets.QLabel(Form)
        self.name2.setObjectName("name2")
        self.gridLayout_2.addWidget(self.name2, 1, 1, 1, 1)
        self.name4 = QtWidgets.QLabel(Form)
        self.name4.setObjectName("name4")
        self.gridLayout_2.addWidget(self.name4, 1, 3, 1, 1)
        self.name5 = QtWidgets.QLabel(Form)
        self.name5.setObjectName("name5")
        self.gridLayout_2.addWidget(self.name5, 1, 4, 1, 1)
        self.bar3 = QtWidgets.QProgressBar(Form)
        self.bar3.setProperty("value", 15)
        self.bar3.setOrientation(QtCore.Qt.Vertical)
        self.bar3.setObjectName("bar3")
        self.gridLayout_2.addWidget(self.bar3, 0, 2, 1, 1)
        self.bar5 = QtWidgets.QProgressBar(Form)
        self.bar5.setProperty("value", 15)
        self.bar5.setOrientation(QtCore.Qt.Vertical)
        self.bar5.setObjectName("bar5")
        self.gridLayout_2.addWidget(self.bar5, 0, 4, 1, 1)
        self.bar1 = QtWidgets.QProgressBar(Form)
        self.bar1.setProperty("value", 35)
        self.bar1.setOrientation(QtCore.Qt.Vertical)
        self.bar1.setObjectName("bar1")
        self.gridLayout_2.addWidget(self.bar1, 0, 0, 1, 1)
        self.bar4 = QtWidgets.QProgressBar(Form)
        self.bar4.setProperty("value", 15)
        self.bar4.setOrientation(QtCore.Qt.Vertical)
        self.bar4.setObjectName("bar4")
        self.gridLayout_2.addWidget(self.bar4, 0, 3, 1, 1)
        self.name6 = QtWidgets.QLabel(Form)
        self.name6.setObjectName("name6")
        self.gridLayout_2.addWidget(self.name6, 1, 5, 1, 1)
        self.name3 = QtWidgets.QLabel(Form)
        self.name3.setObjectName("name3")
        self.gridLayout_2.addWidget(self.name3, 1, 2, 1, 1)
        self.stats6 = QtWidgets.QLabel(Form)
        self.stats6.setObjectName("stats6")
        self.gridLayout_2.addWidget(self.stats6, 2, 5, 1, 1)
        self.stats5 = QtWidgets.QLabel(Form)
        self.stats5.setObjectName("stats5")
        self.gridLayout_2.addWidget(self.stats5, 2, 4, 1, 1)
        self.stats4 = QtWidgets.QLabel(Form)
        self.stats4.setObjectName("stats4")
        self.gridLayout_2.addWidget(self.stats4, 2, 3, 1, 1)
        self.stats3 = QtWidgets.QLabel(Form)
        self.stats3.setObjectName("stats3")
        self.gridLayout_2.addWidget(self.stats3, 2, 2, 1, 1)
        self.stats2 = QtWidgets.QLabel(Form)
        self.stats2.setObjectName("stats2")
        self.gridLayout_2.addWidget(self.stats2, 2, 1, 1, 1)
        self.stats1 = QtWidgets.QLabel(Form)
        self.stats1.setObjectName("stats1")
        self.gridLayout_2.addWidget(self.stats1, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 3, 0, 1, 6)
        self.load_button = QtWidgets.QPushButton(Form)
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 0, 5, 1, 1)
        self.filter_table = QtWidgets.QTableWidget(Form)
        self.filter_table.setObjectName("filter_table")
        self.filter_table.setColumnCount(0)
        self.filter_table.setRowCount(0)
        self.gridLayout.addWidget(self.filter_table, 2, 0, 1, 6)
        self.court_filter_button = QtWidgets.QPushButton(Form)
        self.court_filter_button.setObjectName("court_filter_button")
        self.gridLayout.addWidget(self.court_filter_button, 0, 3, 1, 1)
        self.subaction_filter_button = QtWidgets.QPushButton(Form)
        self.subaction_filter_button.setObjectName("subaction_filter_button")
        self.gridLayout.addWidget(self.subaction_filter_button, 0, 4, 1, 1)
        self.rally_button = QtWidgets.QPushButton(Form)
        self.rally_button.setObjectName("rally_button")
        self.gridLayout.addWidget(self.rally_button, 0, 2, 1, 1)
        self.reset_button = QtWidgets.QPushButton(Form)
        self.reset_button.setObjectName("reset_button")
        self.gridLayout.addWidget(self.reset_button, 1, 5, 1, 1)
        self.gridLayout.setColumnStretch(0, 8)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 8)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Player Analysis"))
        self.action_filter_button.setText(_translate("Form", "ActionFilter"))
        self.name1.setText(_translate("Form", "Player 1"))
        self.name2.setText(_translate("Form", "Player 2"))
        self.name4.setText(_translate("Form", "Player 4"))
        self.name5.setText(_translate("Form", "Player 5"))
        self.name6.setText(_translate("Form", "Player 6"))
        self.name3.setText(_translate("Form", "Player 3"))
        self.stats6.setText(_translate("Form", "Total (perfect)"))
        self.stats5.setText(_translate("Form", "Total (perfect)"))
        self.stats4.setText(_translate("Form", "Total (perfect)"))
        self.stats3.setText(_translate("Form", "Total (perfect)"))
        self.stats2.setText(_translate("Form", "Total (perfect)"))
        self.stats1.setText(_translate("Form", "Total (perfect)"))
        self.load_button.setText(_translate("Form", "Load File"))
        self.court_filter_button.setText(_translate("Form", "CourtFilter"))
        self.subaction_filter_button.setText(_translate("Form", "SubactionFilter"))
        self.rally_button.setText(_translate("Form", "RallyFilter"))
        self.reset_button.setText(_translate("Form", "Reset"))
