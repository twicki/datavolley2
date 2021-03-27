import sys
import os

# import contextlib

from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog

import tvrscouting
from tvrscouting.serializer.serializer import Serializer

from tvrscouting.statistics import Gameaction
from tvrscouting.statistics.Actions.SpecialAction import InitializePlayer
from tvrscouting.statistics.Players.players import Team, Player
from tvrscouting.analysis.filters import *


# class ActionWithInfo:
#     def __init__(
#         self,
#         action,
#         rally,
#         index=0,
#     ):
#         super().__init__()
#         self.action = action
#         self.from_rally = rally
#         self.action_index = index


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
        self.subaction_filter_button.clicked.connect(self.store_subaction_filter)

        self.reset_all_filters()
        self.players = [[], []]
        self.position_to_check = 0
        # self.actions = []
        # self.displayed_actions = []
        # self.players = [[], []]

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
        self.rally_filters = ["@@@@@@@@@@@@"]
        self.court_filters = ["@@@@@@@@@@@@@"]
        self.sub_action_filters = ["@@@@@"]
        self.initialize_table()

    def reset_filters_and_apply(self):
        self.reset_all_filters()
        self.apply_all_filters()

    def update_filter_table_from_filters(self, filters, index):
        self.filter_table.setRowCount(
            max(
                len(self.rally_filters),
                len(self.sub_action_filters),
                len(self.court_filters),
                len(self.action_filters),
            )
            + 1
        )
        self.filter_table.setItem(
            len(self.rally_filters), index, QtWidgets.QTableWidgetItem(filters[-1])
        )

    def store_rally_filter(self):
        rally_filter = self.lineEdit.text()
        self.lineEdit.clear()
        if len(self.rally_filters) == 1 and self.rally_filters[0] == "@@@@@@@@@@@@":
            self.rally_filters.clear()
        self.rally_filters.append(rally_filter)
        self.update_filter_table_from_filters(self.rally_filters, 1)
        self.apply_all_filters()

    def store_subaction_filter(self):
        subaction_filter = self.lineEdit.text()
        self.lineEdit.clear()
        if len(self.sub_action_filters) == 1 and self.sub_action_filters[0] == "@@@@@":
            self.sub_action_filters.clear()
        self.sub_action_filters.append(subaction_filter)
        self.update_filter_table_from_filters(self.sub_action_filters, 3)
        self.apply_all_filters()

    def store_court_filter(self):
        court_filter = self.lineEdit.text()
        self.lineEdit.clear()
        if len(self.court_filters) == 1 and self.court_filters[0] == "@@@@@@@@@@@@@":
            self.court_filters.clear()
        self.court_filters.append(court_filter)
        self.update_filter_table_from_filters(self.court_filters, 2)
        self.apply_all_filters()

    def store_action_filter(self):
        action_filter = self.lineEdit.text()
        self.lineEdit.clear()
        if len(self.action_filters) == 1 and self.action_filters[0] == "@@@@@":
            self.action_filters.clear()
        self.action_filters.append(action_filter)
        self.update_filter_table_from_filters(self.action_filters, 0)
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

    def check_all_subaction_filters(self, rally):
        for subaction_filter in self.sub_action_filters:
            if rally_filter_from_action_string(subaction_filter, rally):
                return True
        return False

    def check_all_action_filters(self, action):
        for action_filter in self.action_filters:
            if compare_action_to_string(action, action_filter):
                return True
        return False

    # def set_total_number_of_actions(self):
    #     self.total_nuber_of_actions = len(self.displayed_actions)

    # @contextlib.contextmanager
    # def edit_table(self):
    #     self.action_view.itemChanged.connect(lambda: None)
    #     self.action_view.itemChanged.disconnect()
    #     yield
    #     self.action_view.itemChanged.connect(self.save_modified_version)

    # def save_modified_version(self, item):
    #     row = item.row()
    #     col = item.column()
    #     changed_action_index = self.displayed_actions[row].action_index
    #     # new_game_state = GameState()
    #     # for new_action in self.all_actions:
    #     #     if new_action.action_index == changed_action_index:
    #     #         action_str = item.text()
    #     #         new_game_state.add_plain_from_string(
    #     #             action_str, new_action.absolute_timestamp
    #     #         )
    #     #     else:
    #     #         new_action.action.time_stamp = new_action.absolute_timestamp
    #     #         new_game_state.add_plain([new_action.action])

    # def fill_action_view(self):
    #     self.set_total_number_of_actions()
    #     with self.edit_table():
    #         self.action_view.setRowCount(self.total_nuber_of_actions)
    #         self.action_view.setColumnCount(1)
    #         index = 0
    #         for action_with_info in self.displayed_actions:
    #             self.action_view.setItem(
    #                 0, index, QtWidgets.QTableWidgetItem(str(action_with_info.action))
    #             )
    #             index += 1
    #         self.action_view.setRowCount(index)
    #         self.action_view.scrollToBottom()

    def apply_all_filters(self):
        self.actions = []
        # self.displayed_actions = []
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
                if (
                    self.check_all_rally_filters(rally)
                    and self.check_all_court_filters(rally[1])
                    and self.check_all_subaction_filters(rally)
                ):
                    if isinstance(action, Gameaction):
                        current_action = str(action)
                        if self.check_all_action_filters(current_action):
                            self.actions.append(action)

        # index = 0
        # for action_with_info in self.all_actions:
        #     if isinstance(action_with_info.action, InitializePlayer):
        #         p = Player(
        #             action_with_info.action.number,
        #             action_with_info.action.position,
        #             action_with_info.action.name,
        #         )
        #         self.players[int(action_with_info.action.team)].append(p)
        #     if (
        #         self.check_all_rally_filters(rally)
        #         and self.check_all_court_filters(rally[1])
        #         and self.check_all_subaction_filters(rally)
        #     ):
        #         if isinstance(action_with_info.action, Gameaction):
        #             current_action = str(action_with_info.action)
        #             if self.check_all_action_filters(current_action):
        #                 self.actions.append(action_with_info.action)
        #         self.action_view.setItem(
        #             0, index, QtWidgets.QTableWidgetItem(current_action)
        #         )
        #         self.displayed_actions.append(action)
        #         index += 1
        # self.fill_action_view()
        self.analyze()

    def analyze(self):
        raise NotImplementedError()

    def load_file(self):
        ser = Serializer(self)
        self.game_state = ser.deserialize()
        self.apply_all_filters()
        # self.fill_action_view()
