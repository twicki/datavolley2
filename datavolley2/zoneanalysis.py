import sys
import os
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog

import datavolley2
from datavolley2.serializer.serializer import Serializer
from datavolley2.uis.zoneanalysis import Ui_Form

from datavolley2.statistics import Gameaction
from datavolley2.analysis.filters import *


class Main(QtWidgets.QWidget, Ui_Form):
    def __init__(self, game_state=None):
        super().__init__()
        self.setupUi(self)
        self.game_state = None

        self.action_filter_button.clicked.connect(self.store_action_filter)
        self.court_filter_button.clicked.connect(self.store_court_filter)
        self.rally_button.clicked.connect(self.store_rally_filter)
        self.reset_button.clicked.connect(self.reset_filters_and_apply)
        self.load_button.clicked.connect(self.load_file)

        self.reset_all_filters()

    def initialize_players(self):
        # TODO add this somehow???
        # p = Player(action.number, action.position, action.name)
        # self.players[int(action.team)].append(p)
        pass

    def initialize_table(self):
        self.filter_table.setRowCount(2)
        self.filter_table.setColumnCount(4)
        for i, what, filter_string in zip(
            range(4),
            ["Action", "Rally", "Court", "SubAction"],
            [
                self.action_filter,
                self.rally_filter,
                self.court_filter,
                self.sub_action_filter,
            ],
        ):
            self.filter_table.setItem(0, i, QtWidgets.QTableWidgetItem(what))
            self.filter_table.setItem(1, i, QtWidgets.QTableWidgetItem(filter_string))

    def reset_all_filters(self):
        self.action_filter = "@@@@@"
        self.rally_filter = "@@@@@@@@"
        self.court_filter = "@@@@@@@@@@@@@"
        self.sub_action_filter = "@@@@@"
        self.initialize_table()

    def reset_filters_and_apply(self):
        self.reset_all_filters()
        self.apply_all_filters()

    def store_rally_filter(self):
        self.rally_filter = self.lineEdit.text()
        self.filter_table.setItem(1, 1, QtWidgets.QTableWidgetItem(self.rally_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def store_court_filter(self):
        self.court_filter = self.lineEdit.text()
        self.filter_table.setItem(1, 2, QtWidgets.QTableWidgetItem(self.court_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def store_action_filter(self):
        self.action_filter = self.lineEdit.text()
        self.filter_table.setItem(1, 0, QtWidgets.QTableWidgetItem(self.action_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def apply_all_filters(self):
        self.actions = []
        for rally in self.game_state.rallies:
            if compare_ralley_to_string(
                self.rally_filter, rally
            ) and compare_court_to_string(rally[1], self.court_filter):
                for action in rally[0]:
                    if isinstance(action, Gameaction):
                        current_action = str(action)
                        if compare_action_to_string(current_action, self.action_filter):
                            self.actions.append(action)
        self.analyze()

    def analyze(self):
        # for position in range(9):
        #     total = 0
        #     leaders = {}
        #     for action in self.actions:
        #         if action.direciton == (position + 1):
        #             total += 1
        #             if action.player in leaders:
        #                 leaders[action.player] += 1
        #             else:
        #                 leaders[action.player] = 1

        total = 0
        leaders = {}
        for action in self.actions:
            # if action.direciton == (-1):
            total += 1
            name = str(action.team) + str(action.player)
            if name in leaders:
                leaders[name] += 1
            else:
                leaders[name] = 1
        self.total_perc_1.setText(str(int(100 * (total / len(self.actions)))))
        self.total_1.setText(str(total))
        sorted_leaders = []
        for number, amount in leaders.items():
            sorted_leaders.append([number, amount])
        sorted_leaders = sorted(
            sorted_leaders, key=lambda action: action[1], reverse=True
        )
        # TODO: sort them
        item = sorted_leaders[0]
        self.lead_1.setText(str(item[0]) + " : " + str(item[1]))
        # TODO: add leader etc in container
        # TODO: add second etc

    def load_file(self):
        filename = QFileDialog.getOpenFileName(
            self, "Open File", os.path.expanduser("~")
        )[0]
        if not filename:
            return
        ser = Serializer()
        self.game_state = ser.deserialize(filename)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())