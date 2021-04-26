from typing import List, Optional

from PyQt5 import QtWidgets

from tvrscouting.analysis.filters import (
    compare_action_to_string,
    compare_court_to_string,
    compare_rally_to_string,
    rally_filter_from_action_string,
)
from tvrscouting.serializer.serializer import Serializer
from tvrscouting.statistics.Actions.GameAction import Gameaction
from tvrscouting.statistics.Actions.SpecialAction import InitializePlayer
from tvrscouting.statistics.Gamestate.game_state import GameState
from tvrscouting.statistics.Players.players import Player


class Basic_Filter:
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.game_state: Optional[GameState] = None

        self.action_filter_button.clicked.connect(self.store_action_filter)
        self.court_filter_button.clicked.connect(self.store_court_filter)
        self.rally_button.clicked.connect(self.store_rally_filter)
        self.reset_button.clicked.connect(self.reset_filters_and_apply)
        self.load_button.clicked.connect(self.load_file)
        self.subaction_filter_button.clicked.connect(self.store_subaction_filter)

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
        self.filter_table.setItem(len(filters), index, QtWidgets.QTableWidgetItem(filters[-1]))

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
            if compare_rally_to_string(rally_filter, rally):
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

    def apply_all_filters(self):
        self.actions: List[Gameaction] = []
        self.players: List[List[Player]] = [[], []]
        if self.game_state is None:
            self.load_file()
            if self.game_state is None:
                return
        self.players = self.game_state.get_players_from_game_state()
        for rally in self.game_state.rallies:
            for action in rally.actions:
                # if isinstance(action, InitializePlayer):
                #     p = Player(action.number, action.position, action.name)
                #     self.players[int(action.team)].append(p)
                if (
                    self.check_all_rally_filters(rally)
                    and self.check_all_court_filters(rally.court)
                    and self.check_all_subaction_filters(rally)
                ):
                    if isinstance(action, Gameaction):
                        current_action = str(action)
                        if self.check_all_action_filters(current_action):
                            self.actions.append(action)
        self.analyze()

    def analyze(self):
        raise NotImplementedError()

    def load_file(self):
        ser = Serializer(self)
        game = ser.deserialize()
        if game:
            self.game_state = game.game_state
            self.apply_all_filters()
        # self.fill_action_view()
