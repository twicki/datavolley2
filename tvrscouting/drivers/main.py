import sys
import os
import re

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog

import tvrscouting
from tvrscouting.statistics.Players.players import Team
from tvrscouting.statistics import GameState
from tvrscouting.analysis.static import StaticWriter

from tvrscouting.serializer.serializer import Serializer

import matplotlib as mp
import numpy as np
import time

from tvrscouting.uis.first import Ui_TVRScouting
from tvrscouting.uis.second import Ui_Form as commentatorUI
from tvrscouting.uis.third import Ui_Form as thridUI
from tvrscouting.uis.fourth import Ui_Form as fourthUI
from tvrscouting.utils.errors import TVRSyntaxError


class PlayerProfileInView:
    def __init__(
        self,
        name_label,
        other_labels,
        hits_box,
        hit_pct_box,
        serve_box,
        block_box,
        rece_box,
        rece_pct_box,
        error_box,
        max_group=7,
    ):
        self.name_label = name_label
        self.other_labels = other_labels
        self.hits_box = hits_box
        self.hit_pct_box = hit_pct_box
        self.serve_box = serve_box
        self.block_box = block_box
        self.rece_box = rece_box
        self.rece_pct_box = rece_pct_box
        self.error_box = error_box
        self.max_group = max_group

    def update_from_result(self, result):
        self.name_label.setText(result[1]["name"])
        self.hits_box.display(result[1]["hit"]["kill"])
        self.serve_box.display(result[1]["serve"]["kill"])
        self.block_box.display(result[1]["block"])
        self.rece_box.display(result[1]["rece"]["total"])
        self.error_box.display(result[1]["error"])
        if result[1]["hit"]["total"] > 0:
            ratio = int(result[1]["hit"]["kill"] / (result[1]["hit"]["total"]) * 100)
        else:
            ratio = 0
        self.hit_pct_box.display(ratio)
        if result[1]["rece"]["total"] > 0:
            ratio = int(result[1]["rece"]["win"] / (result[1]["rece"]["total"]) * 100)
        else:
            ratio = 0
        self.rece_pct_box.display(ratio)
        self.show_view()

    def hide_view(self):
        self.name_label.hide()
        for label in self.other_labels:
            label.hide()
        self.hits_box.hide()
        self.hit_pct_box.hide()
        self.serve_box.hide()
        self.block_box.hide()
        self.rece_box.hide()
        self.rece_pct_box.hide()
        self.error_box.hide()

    def show_view(self):
        self.name_label.show()
        for label in self.other_labels:
            label.show()
        self.hits_box.show()
        self.hit_pct_box.show()
        self.serve_box.show()
        self.block_box.show()
        self.rece_box.show()
        self.rece_pct_box.show()
        self.error_box.show()


class PositionView:
    def __init__(self, name_label):
        self.name_label = name_label


class TeamView:
    def __init__(self, name_label, serve_box, set_score, point_score):
        self.name_label = name_label
        self.serve_box = serve_box
        self.set_score = set_score
        self.point_score = point_score


class MainWindow(QtWidgets.QMainWindow, Ui_TVRScouting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ICON_PATH = os.path.join(os.path.dirname(__file__), "icon/")
        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
        self.game_state = GameState()
        self.fullstring = ""
        self.secondWindow = None
        self.ThirdWindow = None
        self.FourthWindow = None
        self.illegal = []

        self.details = []
        self.time_stamps = []
        self.player_profiles = [[], []]

        self.qt_setup()

    def log_change(self, item):
        # TODO: this is still a bit messy, maybe we can clean it up? -> see idea from update in video
        gamestate = GameState()
        for action_number in range(self.action_view.rowCount()):
            action_str = self.action_view.item(action_number, 0).text()
            gamestate.add_plain_from_string(action_str)
        gamestate.fix_time_stamps(self.game_state)
        self.game_state = gamestate
        self.fullstring = ""
        for rally in self.game_state.rallies:
            for action in rally[0]:
                if not action.auto_generated:
                    self.fullstring += str(action) + " "
            if self.fullstring[-1] != "\n":
                self.fullstring += "\n"
        self.update()

    def save_file(self):
        ser = Serializer(self, self.game_state)
        ser.serialize()

    def load_file(self):
        ser = Serializer(self)
        self.game_state = ser.deserialize()
        self.fullstring = ""
        for rally in self.game_state.rallies:
            for action in rally[0]:
                if not action.auto_generated:
                    self.fullstring += str(action) + " "
            if self.fullstring[-1] != "\n":
                self.fullstring += "\n"
        self.update()

    def write_analysis(self):
        sw = StaticWriter(self.game_state)
        sw.analyze()
        print("stat file written")

    def save_and_reset(self):
        userdata = self.textEdit.toPlainText()
        s = userdata.split()
        oldstate = self.game_state
        self.game_state = GameState()
        self.fullstring = userdata
        self.illegal.clear()

        for command in s:
            try:
                self.game_state.add_string(command)
            except TVRSyntaxError:
                self.illegal.append(command)

        self.game_state.fix_time_stamps(oldstate)
        self.textEdit.setText(self.fullstring)
        self.lineEdit.clear()
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.update()

    def highlight_errors(self):
        fulltext = self.textEdit.toPlainText()
        positions = []
        for illegal_string in self.illegal:
            # TODO: clean up
            output_string = ""
            for c in illegal_string:
                if c == "*":
                    output_string = output_string + "\*"
                else:
                    output_string = output_string + c
            for m in re.finditer(output_string, fulltext):
                positions.append((m.start(), m.end()))
        cursor = QtGui.QTextCursor(self.textEdit.document())
        formatting = QtGui.QTextCharFormat()
        color = QtGui.QColor("red")
        formatting.setBackground(color)
        for position in positions:
            cursor.setPosition(position[0], QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(position[1], QtGui.QTextCursor.KeepAnchor)
            cursor.setCharFormat(formatting)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)

    def add_action_to_game_action(self, command, action_time=None):
        try:
            self.game_state.add_string(command, action_time)
        except:
            self.illegal.append(command)

    def update_full_text_view(self):
        text = self.lineEdit.text()
        self.fullstring = self.fullstring + text + "\n"
        self.textEdit.setText(self.fullstring)
        cursor = QtGui.QTextCursor(self.textEdit.document())
        formatting = QtGui.QTextCharFormat()
        color = QtGui.QColor("white")
        formatting.setBackground(color)
        cursor.setPosition(0, QtGui.QTextCursor.MoveAnchor)
        cursor.setPosition(len(self.fullstring), QtGui.QTextCursor.KeepAnchor)
        cursor.setCharFormat(formatting)
        self.lineEdit.clear()

    def add_input_to_game_state(self):
        self.time_stamps.append(time.time())
        text = self.lineEdit.text()
        actions = text.split(" ")
        if len(self.time_stamps) == len(actions):
            for command, action_time in zip(actions, self.time_stamps):
                self.add_action_to_game_action(command, action_time)
        elif len(self.time_stamps):
            for command in actions:
                self.add_action_to_game_action(command, self.time_stamps[0])
        else:
            for command in actions:
                self.add_action_to_game_action(command)

        self.time_stamps.clear()

    def display_team_info(self):
        for team in range(2):
            self.fieldView["teams"][team].name_label.setText(
                self.game_state.teamnames[team]
            )
            self.fieldView["teams"][team].point_score.display(
                self.game_state.score[team]
            )
            self.fieldView["teams"][team].set_score.display(
                self.game_state.set_score[team]
            )

    def display_serving_teams(self):
        if self.game_state._last_serve == Team.from_string("*"):
            self.fieldView["teams"][0].serve_box.setChecked(True)
            self.fieldView["teams"][1].serve_box.setChecked(False)

        elif self.game_state._last_serve == Team.from_string("/"):
            self.fieldView["teams"][0].serve_box.setChecked(False)
            self.fieldView["teams"][1].serve_box.setChecked(True)

        else:
            self.fieldView["teams"][0].serve_box.setChecked(False)
            self.fieldView["teams"][1].serve_box.setChecked(False)

    def display_players_on_court(self):
        for team in range(2):
            for player, positionview in zip(
                self.game_state.court.fields[team].players,
                self.fieldView["field"][team],
            ):
                number = player.Number
                full_label = str(number) if number > 0 else ""
                for player_in_list in self.game_state.players[team]:
                    if player_in_list.Number == number:
                        full_label = str(number) + " " + player_in_list.Name
                        break
                positionview.name_label.setText(full_label)

    def display_detailed_actions(self):
        self.action_view.itemChanged.connect(self.log_change)
        self.action_view.itemChanged.disconnect()
        self.action_view.setRowCount(10000)
        self.action_view.setColumnCount(1)
        i = 0
        for rally in self.game_state.rallies:
            for action in rally[0]:
                self.action_view.setItem(0, i, QtGui.QTableWidgetItem(str(action)))
                i += 1
        self.action_view.setRowCount(i)
        self.action_view.scrollToBottom()
        self.action_view.itemChanged.connect(self.log_change)

    def update_main_view(self):
        self.update_full_text_view()
        self.highlight_errors()
        self.display_team_info()
        self.display_serving_teams()
        self.display_players_on_court()
        self.display_detailed_actions()

    def update_player_stats(self):
        results = [
            self.game_state.collect_stats("*"),
            self.game_state.collect_stats("/"),
        ]
        self.secondWindow.update_view_from_results(results)

    def update_timeline(self):
        totals, delta = self.game_state.return_timeline()
        self.ThirdWindow.update_timeline(totals, delta)

    def update_recent_scores_view(self):
        score = {
            "score": self.game_state.return_truncated_scores(),
            "team_details": [
                {
                    "name": self.game_state.teamnames[0],
                    "score": self.game_state.score[0],
                },
                {
                    "name": self.game_state.teamnames[1],
                    "score": self.game_state.score[1],
                },
            ],
        }
        self.FourthWindow.update_view_from_results(score)

    def update_commentator_view(self):
        if self.secondWindow is not None:
            self.update_player_stats()
        if self.ThirdWindow:
            self.update_timeline()
        if self.FourthWindow:
            self.update_recent_scores_view()

    def update(self):
        self.add_input_to_game_state()
        self.update_main_view()
        self.update_commentator_view()

    def display_commentator_windows(self):
        if self.secondWindow is None:
            self.secondWindow = SecondWindow()
            s = SecondWindow()
        self.secondWindow.show()
        if self.ThirdWindow is None:
            self.ThirdWindow = ThirdWindow()
        self.ThirdWindow.show()
        if self.FourthWindow is None:
            self.FourthWindow = FourthWindow()
        self.FourthWindow.show()

    def qt_setup(self):
        self.pushButton.clicked.connect(self.display_commentator_windows)
        self.pushButton_2.clicked.connect(self.save_and_reset)
        self.pushButton_3.clicked.connect(self.write_analysis)
        self.lineEdit.returnPressed.connect(self.update)
        self.lineEdit.textChanged.connect(self.get_times)
        self.saveFile.clicked.connect(self.save_file)
        self.loadFile.clicked.connect(self.load_file)
        self.checkBox_2.setEnabled(False)
        self.checkBox.setEnabled(False)

        self.fieldView = {"field": [[], []], "teams": []}
        self.fieldView["teams"].append(
            TeamView(self.label_14, self.checkBox, self.lcdNumber_4, self.lcdNumber)
        )
        self.fieldView["teams"].append(
            TeamView(self.label_13, self.checkBox_2, self.lcdNumber_3, self.lcdNumber_2)
        )
        self.fieldView["field"][0].append(PositionView(self.label))
        self.fieldView["field"][0].append(PositionView(self.label_5))
        self.fieldView["field"][0].append(PositionView(self.label_4))
        self.fieldView["field"][0].append(PositionView(self.label_6))
        self.fieldView["field"][0].append(PositionView(self.label_3))
        self.fieldView["field"][0].append(PositionView(self.label_2))
        self.fieldView["field"][1].append(PositionView(self.label_12))
        self.fieldView["field"][1].append(PositionView(self.label_8))
        self.fieldView["field"][1].append(PositionView(self.label_7))
        self.fieldView["field"][1].append(PositionView(self.label_9))
        self.fieldView["field"][1].append(PositionView(self.label_11))
        self.fieldView["field"][1].append(PositionView(self.label_10))

    def get_times(self):
        if len(self.lineEdit.text()):
            last_character = self.lineEdit.text()[-1]
            if last_character == " ":
                self.time_stamps.append(time.time())


class SecondWindow(QtWidgets.QWidget, commentatorUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.player_profiles = [[], []]
        self.team_profiles = [{}, {}]
        self.qt_setup()

    def qt_setup(self):
        self.team_profiles = [{}, {}]
        self.team_profiles[0]["name"] = self.l_team_home
        self.team_profiles[0]["hit"] = self.home_hits
        self.team_profiles[0]["serve"] = self.home_serve
        self.team_profiles[0]["block"] = self.home_block
        self.team_profiles[0]["error"] = self.home_error
        self.team_profiles[1]["name"] = self.l_team_guest
        self.team_profiles[1]["hit"] = self.guest_hits
        self.team_profiles[1]["serve"] = self.guest_serve
        self.team_profiles[1]["block"] = self.guest_block
        self.team_profiles[1]["error"] = self.guest_error
        self.player_profiles = [[], []]
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name,
                [
                    self.l_hits,
                    self.l_serve,
                    self.l_block,
                    self.l_rece,
                    self.l_error,
                ],
                self.hit,
                self.hit_pct,
                self.serve,
                self.block,
                self.rece,
                self.rece_pct,
                self.error,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_2,
                [
                    self.l_hits_2,
                    self.l_serve_2,
                    self.l_block_2,
                    self.l_rece_2,
                    self.l_error_2,
                ],
                self.hit_2,
                self.hit_pct_2,
                self.serve_2,
                self.block_2,
                self.rece_2,
                self.rece_pct_2,
                self.error_2,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_3,
                [
                    self.l_hits_3,
                    self.l_serve_3,
                    self.l_block_3,
                    self.l_rece_3,
                    self.l_error_3,
                ],
                self.hit_3,
                self.hit_pct_3,
                self.serve_3,
                self.block_3,
                self.rece_3,
                self.rece_pct_3,
                self.error_3,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_4,
                [
                    self.l_hits_4,
                    self.l_serve_4,
                    self.l_block_4,
                    self.l_rece_4,
                    self.l_error_4,
                ],
                self.hit_4,
                self.hit_pct_4,
                self.serve_4,
                self.block_4,
                self.rece_4,
                self.rece_pct_4,
                self.error_4,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_5,
                [
                    self.l_hits_5,
                    self.l_serve_5,
                    self.l_block_5,
                    self.l_rece_5,
                    self.l_error_5,
                ],
                self.hit_5,
                self.hit_pct_5,
                self.serve_5,
                self.block_5,
                self.rece_5,
                self.rece_pct_5,
                self.error_5,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_6,
                [
                    self.l_hits_6,
                    self.l_serve_6,
                    self.l_block_6,
                    self.l_rece_6,
                    self.l_error_6,
                ],
                self.hit_6,
                self.hit_pct_6,
                self.serve_6,
                self.block_6,
                self.rece_6,
                self.rece_pct_6,
                self.error_6,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_7,
                [
                    self.l_hits_7,
                    self.l_serve_7,
                    self.l_block_7,
                    self.l_rece_7,
                    self.l_error_7,
                ],
                self.hit_7,
                self.hit_pct_7,
                self.serve_7,
                self.block_7,
                self.rece_7,
                self.rece_pct_7,
                self.error_7,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_8,
                [
                    self.l_hits_8,
                    self.l_serve_8,
                    self.l_block_8,
                    self.l_rece_8,
                    self.l_error_8,
                ],
                self.hit_8,
                self.hit_pct_8,
                self.serve_8,
                self.block_8,
                self.rece_8,
                self.rece_pct_8,
                self.error_8,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_9,
                [
                    self.l_hits_9,
                    self.l_serve_9,
                    self.l_block_9,
                    self.l_rece_9,
                    self.l_error_9,
                ],
                self.hit_9,
                self.hit_pct_9,
                self.serve_9,
                self.block_9,
                self.rece_9,
                self.rece_pct_9,
                self.error_9,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_10,
                [
                    self.l_hits_10,
                    self.l_serve_10,
                    self.l_block_10,
                    self.l_rece_10,
                    self.l_error_10,
                ],
                self.hit_10,
                self.hit_pct_10,
                self.serve_10,
                self.block_10,
                self.rece_10,
                self.rece_pct_10,
                self.error_10,
                7,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_11,
                [
                    self.l_hits_11,
                    self.l_serve_11,
                    self.l_block_11,
                    self.l_rece_11,
                    self.l_error_11,
                ],
                self.hit_11,
                self.hit_pct_11,
                self.serve_11,
                self.block_11,
                self.rece_11,
                self.rece_pct_11,
                self.error_11,
                7,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_12,
                [
                    self.l_hits_12,
                    self.l_serve_12,
                    self.l_block_12,
                    self.l_rece_12,
                    self.l_error_12,
                ],
                self.hit_12,
                self.hit_pct_12,
                self.serve_12,
                self.block_12,
                self.rece_12,
                self.rece_pct_12,
                self.error_12,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_13,
                [
                    self.l_hits_13,
                    self.l_serve_13,
                    self.l_block_13,
                    self.l_rece_13,
                    self.l_error_13,
                ],
                self.hit_13,
                self.hit_pct_13,
                self.serve_13,
                self.block_13,
                self.rece_13,
                self.rece_pct_13,
                self.error_13,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_14,
                [
                    self.l_hits_14,
                    self.l_serve_14,
                    self.l_block_14,
                    self.l_rece_14,
                    self.l_error_14,
                ],
                self.hit_14,
                self.hit_pct_14,
                self.serve_14,
                self.block_14,
                self.rece_14,
                self.rece_pct_14,
                self.error_14,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_15,
                [
                    self.l_hits_15,
                    self.l_serve_15,
                    self.l_block_15,
                    self.l_rece_15,
                    self.l_error_15,
                ],
                self.hit_15,
                self.hit_pct_15,
                self.serve_15,
                self.block_15,
                self.rece_15,
                self.rece_pct_15,
                self.error_15,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_16,
                [
                    self.l_hits_16,
                    self.l_serve_16,
                    self.l_block_16,
                    self.l_rece_16,
                    self.l_error_16,
                ],
                self.hit_16,
                self.hit_pct_16,
                self.serve_16,
                self.block_16,
                self.rece_16,
                self.rece_pct_16,
                self.error_16,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_17,
                [
                    self.l_hits_17,
                    self.l_serve_17,
                    self.l_block_17,
                    self.l_rece_17,
                    self.l_error_17,
                ],
                self.hit_17,
                self.hit_pct_17,
                self.serve_17,
                self.block_17,
                self.rece_17,
                self.rece_pct_17,
                self.error_17,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_18,
                [
                    self.l_hits_18,
                    self.l_serve_18,
                    self.l_block_18,
                    self.l_rece_18,
                    self.l_error_18,
                ],
                self.hit_18,
                self.hit_pct_18,
                self.serve_18,
                self.block_18,
                self.rece_18,
                self.rece_pct_18,
                self.error_18,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_19,
                [
                    self.l_hits_19,
                    self.l_serve_19,
                    self.l_block_19,
                    self.l_rece_19,
                    self.l_error_19,
                ],
                self.hit_19,
                self.hit_pct_19,
                self.serve_19,
                self.block_19,
                self.rece_19,
                self.rece_pct_19,
                self.error_19,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_20,
                [
                    self.l_hits_20,
                    self.l_serve_20,
                    self.l_block_20,
                    self.l_rece_20,
                    self.l_error_20,
                ],
                self.hit_20,
                self.hit_pct_20,
                self.serve_20,
                self.block_20,
                self.rece_20,
                self.rece_pct_20,
                self.error_20,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_21,
                [
                    self.l_hits_21,
                    self.l_serve_21,
                    self.l_block_21,
                    self.l_rece_21,
                    self.l_error_21,
                ],
                self.hit_21,
                self.hit_pct_21,
                self.serve_21,
                self.block_21,
                self.rece_21,
                self.rece_pct_21,
                self.error_21,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_22,
                [
                    self.l_hits_22,
                    self.l_serve_22,
                    self.l_block_22,
                    self.l_rece_22,
                    self.l_error_22,
                ],
                self.hit_22,
                self.hit_pct_22,
                self.serve_22,
                self.block_22,
                self.rece_22,
                self.rece_pct_22,
                self.error_22,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_23,
                [
                    self.l_hits_23,
                    self.l_serve_23,
                    self.l_block_23,
                    self.l_rece_23,
                    self.l_error_23,
                ],
                self.hit_23,
                self.hit_pct_23,
                self.serve_23,
                self.block_23,
                self.rece_23,
                self.rece_pct_23,
                self.error_23,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_24,
                [
                    self.l_hits_24,
                    self.l_serve_24,
                    self.l_block_24,
                    self.l_rece_24,
                    self.l_error_24,
                ],
                self.hit_24,
                self.hit_pct_24,
                self.serve_24,
                self.block_24,
                self.rece_24,
                self.rece_pct_24,
                self.error_24,
                7,
            )
        )

    def update_team_view(self, results):
        for team in range(2):
            self.team_profiles[team]["name"].setText(results[team]["team"]["name"])
            self.team_profiles[team]["hit"].display(
                results[team]["team"]["hit"]["kill"]
            )
            self.team_profiles[team]["serve"].display(
                results[team]["team"]["serve"]["kill"]
            )
            self.team_profiles[team]["block"].display(results[team]["team"]["block"])
            self.team_profiles[team]["error"].display(results[team]["team"]["error"])

    @staticmethod
    def no_actions_performed(player_details):
        if player_details["group"] < 7:
            if player_details["hit"]["kill"] > 0:
                return False
            if player_details["serve"]["kill"] > 0:
                return False
            if player_details["block"] > 0:
                return False
            if player_details["rece"]["total"] > 0:
                return False
            if player_details["error"] > 0:
                return False
        return True

    def find_candidate_results_in_team(self, result):
        candidate_found = False
        while candidate_found == False:
            if len(result) == 0:
                value = None
                candidate_found = True
            else:
                value = result.popitem(False)
                if value == None:
                    candidate_found = True
                elif not SecondWindow.no_actions_performed(value[1]):
                    candidate_found = True
        return value

    def update_player_views(self, results):
        for team in range(2):
            processed = True
            for player_view in self.player_profiles[team]:
                if processed:
                    candidate_results = self.find_candidate_results_in_team(
                        results[team]
                    )
                    processed = False

                if (
                    candidate_results
                    and candidate_results[1]["group"] < player_view.max_group
                ):
                    processed = True
                    player_view.update_from_result(candidate_results)
                else:
                    player_view.hide_view()

    def update_view_from_results(self, results):
        self.update_team_view(results)
        self.update_player_views(results)


class ThirdWindow(QtWidgets.QWidget, thridUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def update_timeline(self, totals, delta):
        self.graphicsView.clear()
        self.graphicsView.plot(totals, delta)
        self.graphicsView.showGrid(True, True, 0.8)


class FourthWindow(QtWidgets.QWidget, fourthUI):
    home_scores = []
    guest_scores = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qt_setup()

    def qt_setup(self):
        self.home_scores = [
            self.lcdNumber,
            self.lcdNumber_2,
            self.lcdNumber_3,
            self.lcdNumber_4,
            self.lcdNumber_5,
            self.lcdNumber_6,
            self.lcdNumber_7,
            self.lcdNumber_8,
            self.lcdNumber_9,
            self.lcdNumber_10,
        ]
        self.guest_scores = [
            self.lcdNumber_11,
            self.lcdNumber_12,
            self.lcdNumber_13,
            self.lcdNumber_14,
            self.lcdNumber_15,
            self.lcdNumber_16,
            self.lcdNumber_17,
            self.lcdNumber_18,
            self.lcdNumber_19,
            self.lcdNumber_20,
        ]

    def update_view_from_results(self, results):
        self.label.setText(results["team_details"][0]["name"])
        self.label_2.setText(results["team_details"][1]["name"])
        self.lcdNumber_21.display(results["team_details"][0]["score"])
        self.lcdNumber_22.display(results["team_details"][1]["score"])
        for i in range(len(self.home_scores)):
            self.home_scores[i].hide()
            self.guest_scores[i].hide()
        for i in range(len(results["score"]) - 1):
            self.home_scores[i].show()
            self.guest_scores[i].show()
            if results["score"][i][0] != results["score"][i + 1][0]:
                self.home_scores[i].display(results["score"][i + 1][0])
                self.home_scores[i].setStyleSheet(
                    """QLCDNumber {background-color: green}"""
                )
                self.guest_scores[i].display(" ")
                self.guest_scores[i].setStyleSheet(
                    """QLCDNumber {background-color: rgb(114, 159, 207);}"""
                )
            else:
                self.guest_scores[i].display(results["score"][i + 1][1])
                self.guest_scores[i].setStyleSheet(
                    """QLCDNumber {background-color: green}"""
                )
                self.home_scores[i].display(" ")
                self.home_scores[i].setStyleSheet(
                    """QLCDNumber {background-color: rgb(114, 159, 207);}"""
                )


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
