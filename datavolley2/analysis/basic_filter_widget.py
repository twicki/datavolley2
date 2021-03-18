import sys
import os
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog

import datavolley2
from datavolley2.serializer.serializer import Serializer

from datavolley2.statistics import Gameaction
from datavolley2.statistics.Actions.SpecialAction import InitializePlayer
from datavolley2.statistics.Players.players import Team, Player
from datavolley2.analysis.filters import *


class Basic_Filter:
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.game_state = None

        self.action_filter_button.clicked.connect(self.store_action_filter)
        self.court_filter_button.clicked.connect(self.store_court_filter)
        self.rally_button.clicked.connect(self.store_rally_filter)
        self.reset_button.clicked.connect(self.reset_filters_and_apply)
        self.load_button.clicked.connect(self.load_file)

        self.reset_all_filters()
        self.players = [[], []]
        self.position_to_check = 0

    def initialize_table(self):
        self.filter_table.setRowCount(2)
        self.filter_table.setColumnCount(4)
        for i, what, filter_string in zip(
            range(4),
            ["Action", "Rally", "Court", "SubAction"],
            [
                self.action_filters[0],
                self.rally_filters[0],
                self.court_filters[0],
                self.sub_action_filters[0],
            ],
        ):
            self.filter_table.setItem(0, i, QtWidgets.QTableWidgetItem(what))
            self.filter_table.setItem(1, i, QtWidgets.QTableWidgetItem(filter_string))

    def reset_all_filters(self):
        self.action_filters = ["@@@@@"]
        self.rally_filters = ["@@@@@@@@"]
        self.court_filters = ["@@@@@@@@@@@@@"]
        self.sub_action_filters = ["@@@@@"]
        self.initialize_table()

    def reset_filters_and_apply(self):
        self.reset_all_filters()
        self.apply_all_filters()

    def store_rally_filter(self):
        rally_filter = self.lineEdit.text()
        if len(self.rally_filters) == 1 and self.rally_filters[0] == "@@@@@@@@":
            self.rally_filters.clear()
        self.rally_filters.append(rally_filter)
        self.filter_table.setItem(1, 1, QtWidgets.QTableWidgetItem(rally_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def store_court_filter(self):
        court_filter = self.lineEdit.text()
        if len(self.court_filters) == 1 and self.court_filters[0] == "@@@@@@@@@@@@@":
            self.court_filters.clear()
        self.court_filters.append(court_filter)
        self.filter_table.setItem(1, 2, QtWidgets.QTableWidgetItem(court_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def store_action_filter(self):
        action_filter = self.lineEdit.text()
        if len(self.action_filters) == 1 and self.action_filters[0] == "@@@@@":
            self.action_filters.clear()
        self.action_filters.append(action_filter)
        self.filter_table.setItem(1, 0, QtWidgets.QTableWidgetItem(action_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def check_all_rally_filters(self, rally):
        for rally_filter in self.rally_filters:
            if compare_ralley_to_string(rally_filter, rally):
                return True
        return False

    def check_all_court_filters(self, court):
        for court_filter in self.court_filters:
            if compare_court_to_string(court, court_filter):
                return True
        return False

    def check_all_action_filters(self, action):
        for action_filter in self.action_filters:
            if compare_action_to_string(action, action_filter):
                return True
        return False

    def apply_all_filters(self):
        self.actions = []
        self.players = [[], []]
        if self.game_state is None:
            self.load_file()
            if self.game_state is None:
                return
        for rally in self.game_state.rallies:
            for action in rally[0]:
                if isinstance(action, InitializePlayer):
                    p = Player(action.number, action.position, action.name)
                    self.players[int(action.team)].append(p)
                if self.check_all_rally_filters(rally) and self.check_all_court_filters(
                    rally[1]
                ):
                    if isinstance(action, Gameaction):
                        current_action = str(action)
                        if self.check_all_action_filters(current_action):
                            self.actions.append(action)
        self.analyze()

    def analyze(self):
        raise NotImplementedError()

    def load_file(self):
        filename = QFileDialog.getOpenFileName(
            self, "Open File", os.path.expanduser("~")
        )[0]
        if not filename:
            return
        ser = Serializer()
        self.game_state = ser.deserialize(filename)
