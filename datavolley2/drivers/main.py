import sys
import os
import re

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog

import datavolley2
from datavolley2.statistics.Players.players import Team
from datavolley2.statistics import GameState
from datavolley2.analysis.static import StaticWriter

from datavolley2.serializer.serializer import Serializer

import matplotlib as mp
import numpy as np
import time

from datavolley2.uis.first import Ui_MainWindow
from datavolley2.uis.second import Ui_Form
from datavolley2.uis.third import Ui_Form as thridUI
from datavolley2.uis.fourth import Ui_Form as fourthUI


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


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_stats)
        self.pushButton_2.clicked.connect(self.save_and_reset)
        self.pushButton_3.clicked.connect(self.write_analysis)
        self.lineEdit.returnPressed.connect(self.update)
        self.lineEdit.textChanged.connect(self.get_times)
        self.saveFile.clicked.connect(self.save_file)
        self.loadFile.clicked.connect(self.load_file)
        self.game_state = GameState()
        self.fullstring = ""
        self.secondWindow = None
        self.ThirdWindow = None
        self.FourthWindow = None
        self.illegal = []

        self.details = []
        self.time_stamps = []

        self.player_profiles = [[], []]

    def setup_player_view(self):
        self.player_profiles = [[], []]
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name,
                [
                    self.secondWindow.l_hits,
                    self.secondWindow.l_serve,
                    self.secondWindow.l_block,
                    self.secondWindow.l_rece,
                    self.secondWindow.l_error,
                ],
                self.secondWindow.hit,
                self.secondWindow.hit_pct,
                self.secondWindow.serve,
                self.secondWindow.block,
                self.secondWindow.rece,
                self.secondWindow.rece_pct,
                self.secondWindow.error,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_2,
                [
                    self.secondWindow.l_hits_2,
                    self.secondWindow.l_serve_2,
                    self.secondWindow.l_block_2,
                    self.secondWindow.l_rece_2,
                    self.secondWindow.l_error_2,
                ],
                self.secondWindow.hit_2,
                self.secondWindow.hit_pct_2,
                self.secondWindow.serve_2,
                self.secondWindow.block_2,
                self.secondWindow.rece_2,
                self.secondWindow.rece_pct_2,
                self.secondWindow.error_2,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_3,
                [
                    self.secondWindow.l_hits_3,
                    self.secondWindow.l_serve_3,
                    self.secondWindow.l_block_3,
                    self.secondWindow.l_rece_3,
                    self.secondWindow.l_error_3,
                ],
                self.secondWindow.hit_3,
                self.secondWindow.hit_pct_3,
                self.secondWindow.serve_3,
                self.secondWindow.block_3,
                self.secondWindow.rece_3,
                self.secondWindow.rece_pct_3,
                self.secondWindow.error_3,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_4,
                [
                    self.secondWindow.l_hits_4,
                    self.secondWindow.l_serve_4,
                    self.secondWindow.l_block_4,
                    self.secondWindow.l_rece_4,
                    self.secondWindow.l_error_4,
                ],
                self.secondWindow.hit_4,
                self.secondWindow.hit_pct_4,
                self.secondWindow.serve_4,
                self.secondWindow.block_4,
                self.secondWindow.rece_4,
                self.secondWindow.rece_pct_4,
                self.secondWindow.error_4,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_5,
                [
                    self.secondWindow.l_hits_5,
                    self.secondWindow.l_serve_5,
                    self.secondWindow.l_block_5,
                    self.secondWindow.l_rece_5,
                    self.secondWindow.l_error_5,
                ],
                self.secondWindow.hit_5,
                self.secondWindow.hit_pct_5,
                self.secondWindow.serve_5,
                self.secondWindow.block_5,
                self.secondWindow.rece_5,
                self.secondWindow.rece_pct_5,
                self.secondWindow.error_5,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_6,
                [
                    self.secondWindow.l_hits_6,
                    self.secondWindow.l_serve_6,
                    self.secondWindow.l_block_6,
                    self.secondWindow.l_rece_6,
                    self.secondWindow.l_error_6,
                ],
                self.secondWindow.hit_6,
                self.secondWindow.hit_pct_6,
                self.secondWindow.serve_6,
                self.secondWindow.block_6,
                self.secondWindow.rece_6,
                self.secondWindow.rece_pct_6,
                self.secondWindow.error_6,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_7,
                [
                    self.secondWindow.l_hits_7,
                    self.secondWindow.l_serve_7,
                    self.secondWindow.l_block_7,
                    self.secondWindow.l_rece_7,
                    self.secondWindow.l_error_7,
                ],
                self.secondWindow.hit_7,
                self.secondWindow.hit_pct_7,
                self.secondWindow.serve_7,
                self.secondWindow.block_7,
                self.secondWindow.rece_7,
                self.secondWindow.rece_pct_7,
                self.secondWindow.error_7,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_8,
                [
                    self.secondWindow.l_hits_8,
                    self.secondWindow.l_serve_8,
                    self.secondWindow.l_block_8,
                    self.secondWindow.l_rece_8,
                    self.secondWindow.l_error_8,
                ],
                self.secondWindow.hit_8,
                self.secondWindow.hit_pct_8,
                self.secondWindow.serve_8,
                self.secondWindow.block_8,
                self.secondWindow.rece_8,
                self.secondWindow.rece_pct_8,
                self.secondWindow.error_8,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_9,
                [
                    self.secondWindow.l_hits_9,
                    self.secondWindow.l_serve_9,
                    self.secondWindow.l_block_9,
                    self.secondWindow.l_rece_9,
                    self.secondWindow.l_error_9,
                ],
                self.secondWindow.hit_9,
                self.secondWindow.hit_pct_9,
                self.secondWindow.serve_9,
                self.secondWindow.block_9,
                self.secondWindow.rece_9,
                self.secondWindow.rece_pct_9,
                self.secondWindow.error_9,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_10,
                [
                    self.secondWindow.l_hits_10,
                    self.secondWindow.l_serve_10,
                    self.secondWindow.l_block_10,
                    self.secondWindow.l_rece_10,
                    self.secondWindow.l_error_10,
                ],
                self.secondWindow.hit_10,
                self.secondWindow.hit_pct_10,
                self.secondWindow.serve_10,
                self.secondWindow.block_10,
                self.secondWindow.rece_10,
                self.secondWindow.rece_pct_10,
                self.secondWindow.error_10,
                7,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_11,
                [
                    self.secondWindow.l_hits_11,
                    self.secondWindow.l_serve_11,
                    self.secondWindow.l_block_11,
                    self.secondWindow.l_rece_11,
                    self.secondWindow.l_error_11,
                ],
                self.secondWindow.hit_11,
                self.secondWindow.hit_pct_11,
                self.secondWindow.serve_11,
                self.secondWindow.block_11,
                self.secondWindow.rece_11,
                self.secondWindow.rece_pct_11,
                self.secondWindow.error_11,
                7,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.secondWindow.player_name_12,
                [
                    self.secondWindow.l_hits_12,
                    self.secondWindow.l_serve_12,
                    self.secondWindow.l_block_12,
                    self.secondWindow.l_rece_12,
                    self.secondWindow.l_error_12,
                ],
                self.secondWindow.hit_12,
                self.secondWindow.hit_pct_12,
                self.secondWindow.serve_12,
                self.secondWindow.block_12,
                self.secondWindow.rece_12,
                self.secondWindow.rece_pct_12,
                self.secondWindow.error_12,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_13,
                [
                    self.secondWindow.l_hits_13,
                    self.secondWindow.l_serve_13,
                    self.secondWindow.l_block_13,
                    self.secondWindow.l_rece_13,
                    self.secondWindow.l_error_13,
                ],
                self.secondWindow.hit_13,
                self.secondWindow.hit_pct_13,
                self.secondWindow.serve_13,
                self.secondWindow.block_13,
                self.secondWindow.rece_13,
                self.secondWindow.rece_pct_13,
                self.secondWindow.error_13,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_14,
                [
                    self.secondWindow.l_hits_14,
                    self.secondWindow.l_serve_14,
                    self.secondWindow.l_block_14,
                    self.secondWindow.l_rece_14,
                    self.secondWindow.l_error_14,
                ],
                self.secondWindow.hit_14,
                self.secondWindow.hit_pct_14,
                self.secondWindow.serve_14,
                self.secondWindow.block_14,
                self.secondWindow.rece_14,
                self.secondWindow.rece_pct_14,
                self.secondWindow.error_14,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_15,
                [
                    self.secondWindow.l_hits_15,
                    self.secondWindow.l_serve_15,
                    self.secondWindow.l_block_15,
                    self.secondWindow.l_rece_15,
                    self.secondWindow.l_error_15,
                ],
                self.secondWindow.hit_15,
                self.secondWindow.hit_pct_15,
                self.secondWindow.serve_15,
                self.secondWindow.block_15,
                self.secondWindow.rece_15,
                self.secondWindow.rece_pct_15,
                self.secondWindow.error_15,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_16,
                [
                    self.secondWindow.l_hits_16,
                    self.secondWindow.l_serve_16,
                    self.secondWindow.l_block_16,
                    self.secondWindow.l_rece_16,
                    self.secondWindow.l_error_16,
                ],
                self.secondWindow.hit_16,
                self.secondWindow.hit_pct_16,
                self.secondWindow.serve_16,
                self.secondWindow.block_16,
                self.secondWindow.rece_16,
                self.secondWindow.rece_pct_16,
                self.secondWindow.error_16,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_17,
                [
                    self.secondWindow.l_hits_17,
                    self.secondWindow.l_serve_17,
                    self.secondWindow.l_block_17,
                    self.secondWindow.l_rece_17,
                    self.secondWindow.l_error_17,
                ],
                self.secondWindow.hit_17,
                self.secondWindow.hit_pct_17,
                self.secondWindow.serve_17,
                self.secondWindow.block_17,
                self.secondWindow.rece_17,
                self.secondWindow.rece_pct_17,
                self.secondWindow.error_17,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_18,
                [
                    self.secondWindow.l_hits_18,
                    self.secondWindow.l_serve_18,
                    self.secondWindow.l_block_18,
                    self.secondWindow.l_rece_18,
                    self.secondWindow.l_error_18,
                ],
                self.secondWindow.hit_18,
                self.secondWindow.hit_pct_18,
                self.secondWindow.serve_18,
                self.secondWindow.block_18,
                self.secondWindow.rece_18,
                self.secondWindow.rece_pct_18,
                self.secondWindow.error_18,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_19,
                [
                    self.secondWindow.l_hits_19,
                    self.secondWindow.l_serve_19,
                    self.secondWindow.l_block_19,
                    self.secondWindow.l_rece_19,
                    self.secondWindow.l_error_19,
                ],
                self.secondWindow.hit_19,
                self.secondWindow.hit_pct_19,
                self.secondWindow.serve_19,
                self.secondWindow.block_19,
                self.secondWindow.rece_19,
                self.secondWindow.rece_pct_19,
                self.secondWindow.error_19,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_20,
                [
                    self.secondWindow.l_hits_20,
                    self.secondWindow.l_serve_20,
                    self.secondWindow.l_block_20,
                    self.secondWindow.l_rece_20,
                    self.secondWindow.l_error_20,
                ],
                self.secondWindow.hit_20,
                self.secondWindow.hit_pct_20,
                self.secondWindow.serve_20,
                self.secondWindow.block_20,
                self.secondWindow.rece_20,
                self.secondWindow.rece_pct_20,
                self.secondWindow.error_20,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_21,
                [
                    self.secondWindow.l_hits_21,
                    self.secondWindow.l_serve_21,
                    self.secondWindow.l_block_21,
                    self.secondWindow.l_rece_21,
                    self.secondWindow.l_error_21,
                ],
                self.secondWindow.hit_21,
                self.secondWindow.hit_pct_21,
                self.secondWindow.serve_21,
                self.secondWindow.block_21,
                self.secondWindow.rece_21,
                self.secondWindow.rece_pct_21,
                self.secondWindow.error_21,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_22,
                [
                    self.secondWindow.l_hits_22,
                    self.secondWindow.l_serve_22,
                    self.secondWindow.l_block_22,
                    self.secondWindow.l_rece_22,
                    self.secondWindow.l_error_22,
                ],
                self.secondWindow.hit_22,
                self.secondWindow.hit_pct_22,
                self.secondWindow.serve_22,
                self.secondWindow.block_22,
                self.secondWindow.rece_22,
                self.secondWindow.rece_pct_22,
                self.secondWindow.error_22,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_23,
                [
                    self.secondWindow.l_hits_23,
                    self.secondWindow.l_serve_23,
                    self.secondWindow.l_block_23,
                    self.secondWindow.l_rece_23,
                    self.secondWindow.l_error_23,
                ],
                self.secondWindow.hit_23,
                self.secondWindow.hit_pct_23,
                self.secondWindow.serve_23,
                self.secondWindow.block_23,
                self.secondWindow.rece_23,
                self.secondWindow.rece_pct_23,
                self.secondWindow.error_23,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.secondWindow.player_name_24,
                [
                    self.secondWindow.l_hits_24,
                    self.secondWindow.l_serve_24,
                    self.secondWindow.l_block_24,
                    self.secondWindow.l_rece_24,
                    self.secondWindow.l_error_24,
                ],
                self.secondWindow.hit_24,
                self.secondWindow.hit_pct_24,
                self.secondWindow.serve_24,
                self.secondWindow.block_24,
                self.secondWindow.rece_24,
                self.secondWindow.rece_pct_24,
                self.secondWindow.error_24,
                7,
            )
        )

    def save_file(self):
        ser = Serializer(self.game_state)
        ser.serialize("output.tvr")

    def load_file(self):
        filename = QFileDialog.getOpenFileName(
            self, "Open File", os.path.expanduser("~")
        )[0]
        if not filename:
            return
        ser = Serializer()
        self.game_state = ser.deserialize(filename)
        self.fullstring = ""
        for rally in self.game_state.rallies:
            for action in rally[0]:
                if not action.auto_generated:
                    self.fullstring += str(action) + " "
            self.fullstring += "\n"
        self.update()

    @staticmethod
    def no_actions_performed(player_details):
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

    def get_times(self):
        if len(self.lineEdit.text()):
            last_character = self.lineEdit.text()[-1]
            if last_character == " ":
                self.time_stamps.append(time.time())

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
            except:
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
            for m in re.finditer(illegal_string, fulltext):
                positions.append((m.start(), m.end()))
        cursor = QtGui.QTextCursor(self.textEdit.document())
        formatting = QtGui.QTextCharFormat()
        color = QtGui.QColor("red")
        formatting.setBackground(color)
        for position in positions:
            cursor.setPosition(position[0], QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(position[1], QtGui.QTextCursor.KeepAnchor)
            cursor.setCharFormat(formatting)

    def update(self):
        self.time_stamps.append(time.time())
        text = self.lineEdit.text()
        self.fullstring = self.fullstring + text + "\n"
        s = text.split(" ")
        if len(self.time_stamps) == len(s):
            for command, action_time in zip(s, self.time_stamps):
                try:
                    self.game_state.add_string(command, action_time)
                except:
                    self.illegal.append(command)
        elif len(self.time_stamps):
            for command in s:
                try:
                    self.game_state.add_string(command, self.time_stamps[0])
                except:
                    self.illegal.append(command)
        else:
            for command in s:
                try:
                    self.game_state.add_string(command)
                except:
                    self.illegal.append(command)

        self.time_stamps.clear()
        self.textEdit.setText(self.fullstring)
        self.highlight_errors()
        self.textEdit.moveCursor(QtGui.QTextCursor.End)

        ## update my view:
        self.lineEdit.clear()
        self.label_14.setText(self.game_state.teamnames[0])
        self.label_13.setText(self.game_state.teamnames[1])
        if self.game_state._last_serve == Team.from_string("*"):
            self.checkBox.setChecked(True)
            self.checkBox_2.setChecked(False)
        elif self.game_state._last_serve == Team.from_string("/"):
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(True)
        else:
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox.setEnabled(False)

        # home team
        number = self.game_state.court.fields[0].players[0].Number
        fulltext = str(number)
        for p in self.game_state.players[0]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        self.label.setText(fulltext)

        number = self.game_state.court.fields[0].players[1].Number
        fulltext = str(number)
        for p in self.game_state.players[0]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[0]:
            fulltext = fulltext + " " + self.game_state.players[0][number].Name
        self.label_5.setText(fulltext)

        number = self.game_state.court.fields[0].players[2].Number
        fulltext = str(number)
        for p in self.game_state.players[0]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[0]:
            fulltext = fulltext + " " + self.game_state.players[0][number].Name
        self.label_4.setText(fulltext)

        number = self.game_state.court.fields[0].players[3].Number
        fulltext = str(number)
        for p in self.game_state.players[0]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[0]:
            fulltext = fulltext + " " + self.game_state.players[0][number].Name
        self.label_6.setText(fulltext)

        number = self.game_state.court.fields[0].players[4].Number
        fulltext = str(number)
        for p in self.game_state.players[0]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[0]:
            fulltext = fulltext + " " + self.game_state.players[0][number].Name
        self.label_3.setText(fulltext)

        number = self.game_state.court.fields[0].players[5].Number
        fulltext = str(number)
        for p in self.game_state.players[0]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[0]:
            fulltext = fulltext + " " + self.game_state.players[0][number].Name
        self.label_2.setText(fulltext)

        # away team team
        number = self.game_state.court.fields[1].players[0].Number
        fulltext = str(number)
        for p in self.game_state.players[1]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[1]:
            fulltext = fulltext + " " + self.game_state.players[1][number]
        self.label_12.setText(fulltext)

        number = self.game_state.court.fields[1].players[1].Number
        fulltext = str(number)
        for p in self.game_state.players[1]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[1]:
            fulltext = fulltext + " " + self.game_state.players[1][number]
        self.label_8.setText(fulltext)

        number = self.game_state.court.fields[1].players[2].Number
        fulltext = str(number)
        for p in self.game_state.players[1]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[1]:
            fulltext = fulltext + " " + self.game_state.players[1][number]
        self.label_7.setText(fulltext)

        number = self.game_state.court.fields[1].players[3].Number
        fulltext = str(number)
        for p in self.game_state.players[1]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[1]:
            fulltext = fulltext + " " + self.game_state.players[1][number]
        self.label_9.setText(fulltext)

        number = self.game_state.court.fields[1].players[4].Number
        fulltext = str(number)
        for p in self.game_state.players[1]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[1]:
            fulltext = fulltext + " " + self.game_state.players[1][number]
        self.label_11.setText(fulltext)

        number = self.game_state.court.fields[1].players[5].Number
        fulltext = str(number)
        for p in self.game_state.players[1]:
            if p.Number == number:
                fulltext = fulltext + " " + p.Name
        if number in self.game_state.players[1]:
            fulltext = fulltext + " " + self.game_state.players[1][number]
        self.label_10.setText(fulltext)

        ## set up score
        self.lcdNumber.display(self.game_state.score[0])
        self.lcdNumber_2.display(self.game_state.score[1])
        self.lcdNumber_4.display(self.game_state.set_score[0])
        self.lcdNumber_3.display(self.game_state.set_score[1])

        # set up detailed view
        self.tableWidget.setRowCount(10000)
        self.tableWidget.setColumnCount(1)
        i = 0
        for rally in self.game_state.rallies:
            for action in rally[0]:
                self.tableWidget.setItem(0, i, QtGui.QTableWidgetItem(str(action)))
                i += 1
        self.tableWidget.setRowCount(i)
        self.tableWidget.scrollToBottom()

        ## update the other view:
        if self.secondWindow is not None:
            self.secondWindow.l_team_home.setText(self.game_state.teamnames[0])
            results = self.game_state.collect_stats("*")
            self.secondWindow.home_hits.display(results["team"]["hit"]["kill"])
            self.secondWindow.home_serve.display(results["team"]["serve"]["kill"])
            self.secondWindow.home_block.display(results["team"]["block"])
            self.secondWindow.home_error.display(results["team"]["error"])
            processed = True
            for player_view in self.player_profiles[0]:
                if processed:
                    candidate_found = False
                    while candidate_found == False:
                        value = results.popitem(False)
                        if value == None:
                            candidate_found = True
                        elif not self.no_actions_performed(value[1]):
                            number = value[0]
                            fulltext = str(number)
                            for p in self.game_state.players[0]:
                                if p.Number == number:
                                    fulltext = fulltext + " " + p.Name
                            processed = False
                            candidate_found = True
                if value and value[1]["group"] < player_view.max_group:
                    processed = True
                    player_view.name_label.setText(fulltext)
                    player_view.hits_box.display(value[1]["hit"]["kill"])
                    player_view.serve_box.display(value[1]["serve"]["kill"])
                    player_view.block_box.display(value[1]["block"])
                    player_view.rece_box.display(value[1]["rece"]["total"])
                    player_view.error_box.display(value[1]["error"])
                    if value[1]["hit"]["total"] > 0:
                        ratio = int(
                            value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                        )
                    else:
                        ratio = 0
                    player_view.hit_pct_box.display(ratio)
                    if value[1]["rece"]["total"] > 0:
                        ratio = int(
                            value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                        )
                    else:
                        ratio = 0
                    player_view.rece_pct_box.display(ratio)
                    player_view.show_view()
                else:
                    player_view.hide_view()

            results = self.game_state.collect_stats("/")
            self.secondWindow.l_team_guest.setText(self.game_state.teamnames[1])
            self.secondWindow.guest_hits.display(results["team"]["hit"]["kill"])
            self.secondWindow.guest_serve.display(results["team"]["serve"]["kill"])
            self.secondWindow.guest_block.display(results["team"]["block"])
            self.secondWindow.guest_error.display(results["team"]["error"])
            processed = True
            for player_view in self.player_profiles[1]:
                if processed:
                    candidate_found = False
                    while candidate_found == False:
                        value = results.popitem(False)
                        if value == None:
                            candidate_found = True
                        elif not self.no_actions_performed(value[1]):
                            number = value[0]
                            fulltext = str(number)
                            for p in self.game_state.players[1]:
                                if p.Number == number:
                                    fulltext = fulltext + " " + p.Name
                            processed = False
                            candidate_found = True
                if value and value[1]["group"] < player_view.max_group:
                    processed = True
                    player_view.name_label.setText(fulltext)
                    player_view.hits_box.display(value[1]["hit"]["kill"])
                    player_view.serve_box.display(value[1]["serve"]["kill"])
                    player_view.block_box.display(value[1]["block"])
                    player_view.rece_box.display(value[1]["rece"]["total"])
                    player_view.error_box.display(value[1]["error"])
                    if value[1]["hit"]["total"] > 0:
                        ratio = int(
                            value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                        )
                    else:
                        ratio = 0
                    player_view.hit_pct_box.display(ratio)
                    if value[1]["rece"]["total"] > 0:
                        ratio = int(
                            value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                        )
                    else:
                        ratio = 0
                    player_view.rece_pct_box.display(ratio)
                    player_view.show_view()
                else:
                    player_view.hide_view()

        if self.ThirdWindow:
            totals, delta = self.game_state.return_timeline()
            self.ThirdWindow.graphicsView.clear()
            self.ThirdWindow.graphicsView.plot(totals, delta)
            self.ThirdWindow.graphicsView.showGrid(True, True, 0.8)

        if self.FourthWindow:
            score = self.game_state.return_truncated_scores()
            self.game_state.teamnames[0]
            self.FourthWindow.label.setText(self.game_state.teamnames[0])
            self.FourthWindow.label_2.setText(self.game_state.teamnames[1])
            self.FourthWindow.lcdNumber_21.display(self.game_state.score[0])
            self.FourthWindow.lcdNumber_22.display(self.game_state.score[1])
            for i in range(len(self.FourthWindow.home_scores)):
                self.FourthWindow.home_scores[i].hide()
                self.FourthWindow.guest_scores[i].hide()
            for i in range(len(score) - 1):
                self.FourthWindow.home_scores[i].show()
                self.FourthWindow.guest_scores[i].show()
                if score[i][0] != score[i + 1][0]:
                    self.FourthWindow.home_scores[i].display(score[i + 1][0])
                    self.FourthWindow.home_scores[i].setStyleSheet(
                        """QLCDNumber {background-color: green}"""
                    )
                    self.FourthWindow.guest_scores[i].display(" ")
                    self.FourthWindow.guest_scores[i].setStyleSheet(
                        """QLCDNumber {background-color: rgb(114, 159, 207);}"""
                    )
                else:
                    self.FourthWindow.guest_scores[i].display(score[i + 1][1])
                    self.FourthWindow.guest_scores[i].setStyleSheet(
                        """QLCDNumber {background-color: green}"""
                    )
                    self.FourthWindow.home_scores[i].display(" ")
                    self.FourthWindow.home_scores[i].setStyleSheet(
                        """QLCDNumber {background-color: rgb(114, 159, 207);}"""
                    )

    def print_stats(self):
        if self.secondWindow is None:
            self.secondWindow = SecondWindow()
            s = SecondWindow()
            self.setup_player_view()
        self.secondWindow.show()
        if self.ThirdWindow is None:
            self.ThirdWindow = ThirdWindow()
        self.ThirdWindow.show()
        if self.FourthWindow is None:
            self.FourthWindow = FourthWindow()
        self.FourthWindow.show()


class SecondWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ThirdWindow(QtWidgets.QWidget, thridUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class FourthWindow(QtWidgets.QWidget, fourthUI):
    home_scores = []
    guest_scores = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
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


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
