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


from datavolley2.video import Main


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_stats)
        self.pushButton_2.clicked.connect(self.save_and_reset)
        self.pushButton_3.clicked.connect(self.write_analysis)
        self.video_analysis.clicked.connect(self.start_video)
        self.lineEdit.returnPressed.connect(self.update)
        self.lineEdit.textChanged.connect(self.get_times)
        self.saveFile.clicked.connect(self.save_file)
        self.loadFile.clicked.connect(self.load_file)
        self.game_state = GameState()
        self.fullstring = ""
        self.secondWindow = None
        self.ThirdWindow = None
        self.FourthWindow = None
        self.VideoWindow = None
        self.illegal = []

        self.details = []
        self.time_stamps = []

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

    def start_video(self):

        self.VideoWindow = Main(self.game_state)
        self.VideoWindow.show()

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
            ## team 1
            self.secondWindow.label_62.setText(self.game_state.teamnames[0])
            results = self.game_state.collect_stats("*")
            self.secondWindow.lcdNumber_61.display(results["team"]["hit"]["kill"])
            self.secondWindow.lcdNumber_62.display(results["team"]["serve"]["kill"])
            self.secondWindow.lcdNumber_63.display(results["team"]["block"])
            self.secondWindow.lcdNumber_64.display(results["team"]["error"])

            # p1 home
            value = results.popitem(False)
            number = value[0]
            fulltext = str(number)
            for p in self.game_state.players[0]:
                if p.Number == number:
                    fulltext = fulltext + " " + p.Name
            processed = False
            if value and value[1]["group"] < 3:
                processed = True
                self.secondWindow.player_name.setText(fulltext)
                self.secondWindow.hit.display(value[1]["hit"]["kill"])
                self.secondWindow.serve.display(value[1]["serve"]["kill"])
                self.secondWindow.block.display(value[1]["block"])
                self.secondWindow.rece.display(value[1]["rece"]["total"])
                self.secondWindow.error.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct.display(ratio)
                processed = True
                self.secondWindow.player_name.show()
                self.secondWindow.hit.show()
                self.secondWindow.serve.show()
                self.secondWindow.block.show()
                self.secondWindow.rece.show()
                self.secondWindow.error.show()
                self.secondWindow.hit_pct.show()
                self.secondWindow.rece_pct.show()
                self.secondWindow.l_hits.show()
                self.secondWindow.l_serve.show()
                self.secondWindow.l_block.show()
                self.secondWindow.l_rece.show()
                self.secondWindow.l_error.show()
            else:
                self.secondWindow.player_name.hide()
                self.secondWindow.hit.hide()
                self.secondWindow.serve.hide()
                self.secondWindow.block.hide()
                self.secondWindow.rece.hide()
                self.secondWindow.error.hide()
                self.secondWindow.hit_pct.hide()
                self.secondWindow.rece_pct.hide()
                self.secondWindow.l_hits.hide()
                self.secondWindow.l_serve.hide()
                self.secondWindow.l_block.hide()
                self.secondWindow.l_rece.hide()
                self.secondWindow.l_error.hide()

            # p2 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 3:
                self.secondWindow.player_name_2.setText(fulltext)
                self.secondWindow.hit_2.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_2.display(value[1]["serve"]["kill"])
                self.secondWindow.block_2.display(value[1]["block"])
                self.secondWindow.rece_2.display(value[1]["rece"]["total"])
                self.secondWindow.error_2.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_2.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_2.display(ratio)
                processed = True
                self.secondWindow.player_name_2.show()
                self.secondWindow.hit_2.show()
                self.secondWindow.serve_2.show()
                self.secondWindow.block_2.show()
                self.secondWindow.rece_2.show()
                self.secondWindow.error_2.show()
                self.secondWindow.hit_pct_2.show()
                self.secondWindow.rece_pct_2.show()
                self.secondWindow.l_hits_2.show()
                self.secondWindow.l_serve_2.show()
                self.secondWindow.l_block_2.show()
                self.secondWindow.l_rece_2.show()
                self.secondWindow.l_error_2.show()
            else:
                self.secondWindow.player_name_2.hide()
                self.secondWindow.hit_2.hide()
                self.secondWindow.serve_2.hide()
                self.secondWindow.block_2.hide()
                self.secondWindow.rece_2.hide()
                self.secondWindow.error_2.hide()
                self.secondWindow.hit_pct_2.hide()
                self.secondWindow.rece_pct_2.hide()
                self.secondWindow.l_hits_2.hide()
                self.secondWindow.l_serve_2.hide()
                self.secondWindow.l_block_2.hide()
                self.secondWindow.l_rece_2.hide()
                self.secondWindow.l_error_2.hide()

            # p3 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 3:
                self.secondWindow.player_name_3.setText(fulltext)
                self.secondWindow.hit_3.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_3.display(value[1]["serve"]["kill"])
                self.secondWindow.block_3.display(value[1]["block"])
                self.secondWindow.rece_3.display(value[1]["rece"]["total"])
                self.secondWindow.error_3.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_3.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_3.display(ratio)
                processed = True
                self.secondWindow.player_name_3.show()
                self.secondWindow.hit_3.show()
                self.secondWindow.serve_3.show()
                self.secondWindow.block_3.show()
                self.secondWindow.rece_3.show()
                self.secondWindow.error_3.show()
                self.secondWindow.hit_pct_3.show()
                self.secondWindow.rece_pct_3.show()
                self.secondWindow.l_hits_3.show()
                self.secondWindow.l_serve_3.show()
                self.secondWindow.l_block_3.show()
                self.secondWindow.l_rece_3.show()
                self.secondWindow.l_error_3.show()
            else:
                self.secondWindow.player_name_3.hide()
                self.secondWindow.hit_3.hide()
                self.secondWindow.serve_3.hide()
                self.secondWindow.block_3.hide()
                self.secondWindow.rece_3.hide()
                self.secondWindow.error_3.hide()
                self.secondWindow.hit_pct_3.hide()
                self.secondWindow.rece_pct_3.hide()
                self.secondWindow.l_hits_3.hide()
                self.secondWindow.l_serve_3.hide()
                self.secondWindow.l_block_3.hide()
                self.secondWindow.l_rece_3.hide()
                self.secondWindow.l_error_3.hide()
            # p4 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 4:
                self.secondWindow.player_name_4.setText(fulltext)
                self.secondWindow.hit_4.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_4.display(value[1]["serve"]["kill"])
                self.secondWindow.block_4.display(value[1]["block"])
                self.secondWindow.rece_4.display(value[1]["rece"]["total"])
                self.secondWindow.error_4.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_4.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_4.display(ratio)
                processed = True
                self.secondWindow.player_name_4.show()
                self.secondWindow.hit_4.show()
                self.secondWindow.serve_4.show()
                self.secondWindow.block_4.show()
                self.secondWindow.rece_4.show()
                self.secondWindow.error_4.show()
                self.secondWindow.hit_pct_4.show()
                self.secondWindow.rece_pct_4.show()
                self.secondWindow.l_hits_4.show()
                self.secondWindow.l_serve_4.show()
                self.secondWindow.l_block_4.show()
                self.secondWindow.l_rece_4.show()
                self.secondWindow.l_error_4.show()
            else:
                self.secondWindow.player_name_4.hide()
                self.secondWindow.hit_4.hide()
                self.secondWindow.serve_4.hide()
                self.secondWindow.block_4.hide()
                self.secondWindow.rece_4.hide()
                self.secondWindow.error_4.hide()
                self.secondWindow.hit_pct_4.hide()
                self.secondWindow.rece_pct_4.hide()
                self.secondWindow.l_hits_4.hide()
                self.secondWindow.l_serve_4.hide()
                self.secondWindow.l_block_4.hide()
                self.secondWindow.l_rece_4.hide()
                self.secondWindow.l_error_4.hide()
            # p5 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 4:
                self.secondWindow.player_name_5.setText(fulltext)
                self.secondWindow.hit_5.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_5.display(value[1]["serve"]["kill"])
                self.secondWindow.block_5.display(value[1]["block"])
                self.secondWindow.rece_5.display(value[1]["rece"]["total"])
                self.secondWindow.error_5.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_5.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_5.display(ratio)
                processed = True
                self.secondWindow.player_name_5.show()
                self.secondWindow.hit_5.show()
                self.secondWindow.serve_5.show()
                self.secondWindow.block_5.show()
                self.secondWindow.rece_5.show()
                self.secondWindow.error_5.show()
                self.secondWindow.hit_pct_5.show()
                self.secondWindow.rece_pct_5.show()
                self.secondWindow.l_hits_5.show()
                self.secondWindow.l_serve_5.show()
                self.secondWindow.l_block_5.show()
                self.secondWindow.l_rece_5.show()
                self.secondWindow.l_error_5.show()
            else:
                self.secondWindow.player_name_5.hide()
                self.secondWindow.hit_5.hide()
                self.secondWindow.serve_5.hide()
                self.secondWindow.block_5.hide()
                self.secondWindow.rece_5.hide()
                self.secondWindow.error_5.hide()
                self.secondWindow.hit_pct_5.hide()
                self.secondWindow.rece_pct_5.hide()
                self.secondWindow.l_hits_5.hide()
                self.secondWindow.l_serve_5.hide()
                self.secondWindow.l_block_5.hide()
                self.secondWindow.l_rece_5.hide()
                self.secondWindow.l_error_5.hide()
            # p6 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 4:
                self.secondWindow.player_name_6.setText(fulltext)
                self.secondWindow.hit_6.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_6.display(value[1]["serve"]["kill"])
                self.secondWindow.block_6.display(value[1]["block"])
                self.secondWindow.rece_6.display(value[1]["rece"]["total"])
                self.secondWindow.error_6.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_6.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_6.display(ratio)
                processed = True
                self.secondWindow.player_name_6.show()
                self.secondWindow.hit_6.show()
                self.secondWindow.serve_6.show()
                self.secondWindow.block_6.show()
                self.secondWindow.rece_6.show()
                self.secondWindow.error_6.show()
                self.secondWindow.hit_pct_6.show()
                self.secondWindow.rece_pct_6.show()
                self.secondWindow.l_hits_6.show()
                self.secondWindow.l_serve_6.show()
                self.secondWindow.l_block_6.show()
                self.secondWindow.l_rece_6.show()
                self.secondWindow.l_error_6.show()
            else:
                self.secondWindow.player_name_6.hide()
                self.secondWindow.hit_6.hide()
                self.secondWindow.serve_6.hide()
                self.secondWindow.block_6.hide()
                self.secondWindow.rece_6.hide()
                self.secondWindow.error_6.hide()
                self.secondWindow.hit_pct_6.hide()
                self.secondWindow.rece_pct_6.hide()
                self.secondWindow.l_hits_6.hide()
                self.secondWindow.l_serve_6.hide()
                self.secondWindow.l_block_6.hide()
                self.secondWindow.l_rece_6.hide()
                self.secondWindow.l_error_6.hide()
            # p7 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 5:
                self.secondWindow.player_name_7.setText(fulltext)
                self.secondWindow.hit_7.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_7.display(value[1]["serve"]["kill"])
                self.secondWindow.block_7.display(value[1]["block"])
                self.secondWindow.rece_7.display(value[1]["rece"]["total"])
                self.secondWindow.error_7.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_7.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_7.display(ratio)
                processed = True
                self.secondWindow.player_name_7.show()
                self.secondWindow.hit_7.show()
                self.secondWindow.serve_7.show()
                self.secondWindow.block_7.show()
                self.secondWindow.rece_7.show()
                self.secondWindow.error_7.show()
                self.secondWindow.hit_pct_7.show()
                self.secondWindow.rece_pct_7.show()
                self.secondWindow.l_hits_7.show()
                self.secondWindow.l_serve_7.show()
                self.secondWindow.l_block_7.show()
                self.secondWindow.l_rece_7.show()
                self.secondWindow.l_error_7.show()
            else:
                self.secondWindow.player_name_7.hide()
                self.secondWindow.hit_7.hide()
                self.secondWindow.serve_7.hide()
                self.secondWindow.block_7.hide()
                self.secondWindow.rece_7.hide()
                self.secondWindow.error_7.hide()
                self.secondWindow.hit_pct_7.hide()
                self.secondWindow.rece_pct_7.hide()
                self.secondWindow.l_hits_7.hide()
                self.secondWindow.l_serve_7.hide()
                self.secondWindow.l_block_7.hide()
                self.secondWindow.l_rece_7.hide()
                self.secondWindow.l_error_7.hide()
            # p8 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 5:
                self.secondWindow.player_name_8.setText(fulltext)
                self.secondWindow.hit_8.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_8.display(value[1]["serve"]["kill"])
                self.secondWindow.block_8.display(value[1]["block"])
                self.secondWindow.rece_8.display(value[1]["rece"]["total"])
                self.secondWindow.error_8.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_8.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_8.display(ratio)
                processed = True
                self.secondWindow.player_name_8.show()
                self.secondWindow.hit_8.show()
                self.secondWindow.serve_8.show()
                self.secondWindow.block_8.show()
                self.secondWindow.rece_8.show()
                self.secondWindow.error_8.show()
                self.secondWindow.hit_pct_8.show()
                self.secondWindow.rece_pct_8.show()
                self.secondWindow.l_hits_8.show()
                self.secondWindow.l_serve_8.show()
                self.secondWindow.l_block_8.show()
                self.secondWindow.l_rece_8.show()
                self.secondWindow.l_error_8.show()
            else:
                self.secondWindow.player_name_8.hide()
                self.secondWindow.hit_8.hide()
                self.secondWindow.serve_8.hide()
                self.secondWindow.block_8.hide()
                self.secondWindow.rece_8.hide()
                self.secondWindow.error_8.hide()
                self.secondWindow.hit_pct_8.hide()
                self.secondWindow.rece_pct_8.hide()
                self.secondWindow.l_hits_8.hide()
                self.secondWindow.l_serve_8.hide()
                self.secondWindow.l_block_8.hide()
                self.secondWindow.l_rece_8.hide()
                self.secondWindow.l_error_8.hide()
            # p9 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 5:
                self.secondWindow.player_name_9.setText(fulltext)
                self.secondWindow.hit_9.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_9.display(value[1]["serve"]["kill"])
                self.secondWindow.block_9.display(value[1]["block"])
                self.secondWindow.rece_9.display(value[1]["rece"]["total"])
                self.secondWindow.error_9.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_9.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_9.display(ratio)
                processed = True
                self.secondWindow.player_name_9.show()
                self.secondWindow.hit_9.show()
                self.secondWindow.serve_9.show()
                self.secondWindow.block_9.show()
                self.secondWindow.rece_9.show()
                self.secondWindow.error_9.show()
                self.secondWindow.hit_pct_9.show()
                self.secondWindow.rece_pct_9.show()
                self.secondWindow.l_hits_9.show()
                self.secondWindow.l_serve_9.show()
                self.secondWindow.l_block_9.show()
                self.secondWindow.l_rece_9.show()
                self.secondWindow.l_error_9.show()
            else:
                self.secondWindow.player_name_9.hide()
                self.secondWindow.hit_9.hide()
                self.secondWindow.serve_9.hide()
                self.secondWindow.block_9.hide()
                self.secondWindow.rece_9.hide()
                self.secondWindow.error_9.hide()
                self.secondWindow.hit_pct_9.hide()
                self.secondWindow.rece_pct_9.hide()
                self.secondWindow.l_hits_9.hide()
                self.secondWindow.l_serve_9.hide()
                self.secondWindow.l_block_9.hide()
                self.secondWindow.l_rece_9.hide()
                self.secondWindow.l_error_9.hide()
            # p10 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 7:
                self.secondWindow.player_name_10.setText(fulltext)
                self.secondWindow.hit_10.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_10.display(value[1]["serve"]["kill"])
                self.secondWindow.block_10.display(value[1]["block"])
                self.secondWindow.rece_10.display(value[1]["rece"]["total"])
                self.secondWindow.error_10.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_10.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_10.display(ratio)
                processed = True
                self.secondWindow.player_name_10.show()
                self.secondWindow.hit_10.show()
                self.secondWindow.serve_10.show()
                self.secondWindow.block_10.show()
                self.secondWindow.rece_10.show()
                self.secondWindow.error_10.show()
                self.secondWindow.hit_pct_10.show()
                self.secondWindow.rece_pct_10.show()
                self.secondWindow.l_hits_10.show()
                self.secondWindow.l_serve_10.show()
                self.secondWindow.l_block_10.show()
                self.secondWindow.l_rece_10.show()
                self.secondWindow.l_error_10.show()
            else:
                self.secondWindow.player_name_10.hide()
                self.secondWindow.hit_10.hide()
                self.secondWindow.serve_10.hide()
                self.secondWindow.block_10.hide()
                self.secondWindow.rece_10.hide()
                self.secondWindow.error_10.hide()
                self.secondWindow.hit_pct_10.hide()
                self.secondWindow.rece_pct_10.hide()
                self.secondWindow.l_hits_10.hide()
                self.secondWindow.l_serve_10.hide()
                self.secondWindow.l_block_10.hide()
                self.secondWindow.l_rece_10.hide()
                self.secondWindow.l_error_10.hide()
            # p11 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[0]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 7:
                self.secondWindow.player_name_11.setText(fulltext)
                self.secondWindow.hit_11.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_11.display(value[1]["serve"]["kill"])
                self.secondWindow.block_11.display(value[1]["block"])
                self.secondWindow.rece_11.display(value[1]["rece"]["total"])
                self.secondWindow.error_11.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_11.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_11.display(ratio)
                processed = True
                self.secondWindow.player_name_11.show()
                self.secondWindow.hit_11.show()
                self.secondWindow.serve_11.show()
                self.secondWindow.block_11.show()
                self.secondWindow.rece_11.show()
                self.secondWindow.error_11.show()
                self.secondWindow.hit_pct_11.show()
                self.secondWindow.rece_pct_11.show()
                self.secondWindow.l_hits_11.show()
                self.secondWindow.l_serve_11.show()
                self.secondWindow.l_block_11.show()
                self.secondWindow.l_rece_11.show()
                self.secondWindow.l_error_11.show()
            else:
                self.secondWindow.player_name_11.hide()
                self.secondWindow.hit_11.hide()
                self.secondWindow.serve_11.hide()
                self.secondWindow.block_11.hide()
                self.secondWindow.rece_11.hide()
                self.secondWindow.error_11.hide()
                self.secondWindow.hit_pct_11.hide()
                self.secondWindow.rece_pct_11.hide()
                self.secondWindow.l_hits_11.hide()
                self.secondWindow.l_serve_11.hide()
                self.secondWindow.l_block_11.hide()
                self.secondWindow.l_rece_11.hide()
                self.secondWindow.l_error_11.hide()
            # ## team 2
            results = self.game_state.collect_stats("/")
            self.secondWindow.label_61.setText(self.game_state.teamnames[1])
            self.secondWindow.lcdNumber_67.display(results["team"]["hit"]["kill"])
            self.secondWindow.lcdNumber_68.display(results["team"]["serve"]["kill"])
            self.secondWindow.lcdNumber_65.display(results["team"]["block"])
            self.secondWindow.lcdNumber_66.display(results["team"]["error"])

            # p1 away
            value = results.popitem(False)
            number = value[0]
            fulltext = str(number)
            for p in self.game_state.players[1]:
                if p.Number == number:
                    fulltext = fulltext + " " + p.Name
            processed = False
            if value and value[1]["group"] < 3:
                processed = True
                self.secondWindow.player_name_12.setText(fulltext)
                self.secondWindow.hit_12.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_12.display(value[1]["serve"]["kill"])
                self.secondWindow.block_12.display(value[1]["block"])
                self.secondWindow.rece_12.display(value[1]["rece"]["total"])
                self.secondWindow.error_12.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_12.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_12.display(ratio)
                processed = True
                self.secondWindow.player_name_12.show()
                self.secondWindow.player_name_12.show()
                self.secondWindow.hit_12.show()
                self.secondWindow.serve_12.show()
                self.secondWindow.block_12.show()
                self.secondWindow.rece_12.show()
                self.secondWindow.error_12.show()
                self.secondWindow.hit_pct_12.show()
                self.secondWindow.rece_pct_12.show()
                self.secondWindow.l_hits_12.show()
                self.secondWindow.l_serve_12.show()
                self.secondWindow.l_block_12.show()
                self.secondWindow.l_rece_12.show()
                self.secondWindow.l_error_12.show()
            else:
                self.secondWindow.player_name_12.hide()
                self.secondWindow.hit_12.hide()
                self.secondWindow.serve_12.hide()
                self.secondWindow.block_12.hide()
                self.secondWindow.rece_12.hide()
                self.secondWindow.error_12.hide()
                self.secondWindow.hit_pct_12.hide()
                self.secondWindow.rece_pct_12.hide()
                self.secondWindow.l_hits_12.hide()
                self.secondWindow.l_serve_12.hide()
                self.secondWindow.l_block_12.hide()
                self.secondWindow.l_rece_12.hide()
                self.secondWindow.l_error_12.hide()
            # p2 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 3:
                self.secondWindow.player_name_13.setText(fulltext)
                self.secondWindow.hit_13.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_13.display(value[1]["serve"]["kill"])
                self.secondWindow.block_13.display(value[1]["block"])
                self.secondWindow.rece_13.display(value[1]["rece"]["total"])
                self.secondWindow.error_13.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_13.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_13.display(ratio)
                processed = True
                self.secondWindow.player_name_13.show()
                self.secondWindow.hit_13.show()
                self.secondWindow.serve_13.show()
                self.secondWindow.block_13.show()
                self.secondWindow.rece_13.show()
                self.secondWindow.error_13.show()
                self.secondWindow.hit_pct_13.show()
                self.secondWindow.rece_pct_13.show()
                self.secondWindow.l_hits_13.show()
                self.secondWindow.l_serve_13.show()
                self.secondWindow.l_block_13.show()
                self.secondWindow.l_rece_13.show()
                self.secondWindow.l_error_13.show()
            else:
                self.secondWindow.player_name_13.hide()
                self.secondWindow.hit_13.hide()
                self.secondWindow.serve_13.hide()
                self.secondWindow.block_13.hide()
                self.secondWindow.rece_13.hide()
                self.secondWindow.error_13.hide()
                self.secondWindow.hit_pct_13.hide()
                self.secondWindow.rece_pct_13.hide()
                self.secondWindow.l_hits_13.hide()
                self.secondWindow.l_serve_13.hide()
                self.secondWindow.l_block_13.hide()
                self.secondWindow.l_rece_13.hide()
                self.secondWindow.l_error_13.hide()
            # p3 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 3:
                self.secondWindow.player_name_15.setText(fulltext)
                self.secondWindow.hit_15.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_15.display(value[1]["serve"]["kill"])
                self.secondWindow.block_15.display(value[1]["block"])
                self.secondWindow.rece_15.display(value[1]["rece"]["total"])
                self.secondWindow.error_15.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_15.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_15.display(ratio)
                processed = True
                self.secondWindow.player_name_15.show()
                self.secondWindow.hit_15.show()
                self.secondWindow.serve_15.show()
                self.secondWindow.block_15.show()
                self.secondWindow.rece_15.show()
                self.secondWindow.error_15.show()
                self.secondWindow.hit_pct_15.show()
                self.secondWindow.rece_pct_15.show()
                self.secondWindow.l_hits_15.show()
                self.secondWindow.l_serve_15.show()
                self.secondWindow.l_block_15.show()
                self.secondWindow.l_rece_15.show()
                self.secondWindow.l_error_15.show()
            else:
                self.secondWindow.player_name_15.hide()
                self.secondWindow.hit_15.hide()
                self.secondWindow.serve_15.hide()
                self.secondWindow.block_15.hide()
                self.secondWindow.rece_15.hide()
                self.secondWindow.error_15.hide()
                self.secondWindow.hit_pct_15.hide()
                self.secondWindow.rece_pct_15.hide()
                self.secondWindow.l_hits_15.hide()
                self.secondWindow.l_serve_15.hide()
                self.secondWindow.l_block_15.hide()
                self.secondWindow.l_rece_15.hide()
                self.secondWindow.l_error_15.hide()
            # p4 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 4:
                self.secondWindow.player_name_16.setText(fulltext)
                self.secondWindow.hit_16.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_16.display(value[1]["serve"]["kill"])
                self.secondWindow.block_16.display(value[1]["block"])
                self.secondWindow.rece_16.display(value[1]["rece"]["total"])
                self.secondWindow.error_16.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_16.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_16.display(ratio)
                processed = True
                self.secondWindow.player_name_16.show()
                self.secondWindow.hit_16.show()
                self.secondWindow.serve_16.show()
                self.secondWindow.block_16.show()
                self.secondWindow.rece_16.show()
                self.secondWindow.error_16.show()
                self.secondWindow.hit_pct_16.show()
                self.secondWindow.rece_pct_16.show()
                self.secondWindow.l_hits_16.show()
                self.secondWindow.l_serve_16.show()
                self.secondWindow.l_block_16.show()
                self.secondWindow.l_rece_16.show()
                self.secondWindow.l_error_16.show()
            else:
                self.secondWindow.player_name_16.hide()
                self.secondWindow.hit_16.hide()
                self.secondWindow.serve_16.hide()
                self.secondWindow.block_16.hide()
                self.secondWindow.rece_16.hide()
                self.secondWindow.error_16.hide()
                self.secondWindow.hit_pct_16.hide()
                self.secondWindow.rece_pct_16.hide()
                self.secondWindow.l_hits_16.hide()
                self.secondWindow.l_serve_16.hide()
                self.secondWindow.l_block_16.hide()
                self.secondWindow.l_rece_16.hide()
                self.secondWindow.l_error_16.hide()
            # p5 home
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 4:
                self.secondWindow.player_name_17.setText(fulltext)
                self.secondWindow.hit_17.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_17.display(value[1]["serve"]["kill"])
                self.secondWindow.block_17.display(value[1]["block"])
                self.secondWindow.rece_17.display(value[1]["rece"]["total"])
                self.secondWindow.error_17.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_17.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_17.display(ratio)
                processed = True
                self.secondWindow.player_name_17.show()
                self.secondWindow.hit_17.show()
                self.secondWindow.serve_17.show()
                self.secondWindow.block_17.show()
                self.secondWindow.rece_17.show()
                self.secondWindow.error_17.show()
                self.secondWindow.hit_pct_17.show()
                self.secondWindow.rece_pct_17.show()
                self.secondWindow.l_hits_17.show()
                self.secondWindow.l_serve_17.show()
                self.secondWindow.l_block_17.show()
                self.secondWindow.l_rece_17.show()
                self.secondWindow.l_error_17.show()
            else:
                self.secondWindow.player_name_17.hide()
                self.secondWindow.hit_17.hide()
                self.secondWindow.serve_17.hide()
                self.secondWindow.block_17.hide()
                self.secondWindow.rece_17.hide()
                self.secondWindow.error_17.hide()
                self.secondWindow.hit_pct_17.hide()
                self.secondWindow.rece_pct_17.hide()
                self.secondWindow.l_hits_17.hide()
                self.secondWindow.l_serve_17.hide()
                self.secondWindow.l_block_17.hide()
                self.secondWindow.l_rece_17.hide()
                self.secondWindow.l_error_17.hide()

            # p6 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 4:
                self.secondWindow.player_name_18.setText(fulltext)
                self.secondWindow.hit_18.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_18.display(value[1]["serve"]["kill"])
                self.secondWindow.block_18.display(value[1]["block"])
                self.secondWindow.rece_18.display(value[1]["rece"]["total"])
                self.secondWindow.error_18.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_18.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_18.display(ratio)
                processed = True
                self.secondWindow.player_name_18.show()
                self.secondWindow.hit_18.show()
                self.secondWindow.serve_18.show()
                self.secondWindow.block_18.show()
                self.secondWindow.rece_18.show()
                self.secondWindow.error_18.show()
                self.secondWindow.hit_pct_18.show()
                self.secondWindow.rece_pct_18.show()
                self.secondWindow.l_hits_18.show()
                self.secondWindow.l_serve_18.show()
                self.secondWindow.l_block_18.show()
                self.secondWindow.l_rece_18.show()
                self.secondWindow.l_error_18.show()
            else:
                self.secondWindow.player_name_18.hide()
                self.secondWindow.hit_18.hide()
                self.secondWindow.serve_18.hide()
                self.secondWindow.block_18.hide()
                self.secondWindow.rece_18.hide()
                self.secondWindow.error_18.hide()
                self.secondWindow.hit_pct_18.hide()
                self.secondWindow.rece_pct_18.hide()
                self.secondWindow.l_hits_18.hide()
                self.secondWindow.l_serve_18.hide()
                self.secondWindow.l_block_18.hide()
                self.secondWindow.l_rece_18.hide()
                self.secondWindow.l_error_18.hide()

            # p7 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 5:
                self.secondWindow.player_name_19.setText(fulltext)
                self.secondWindow.hit_19.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_19.display(value[1]["serve"]["kill"])
                self.secondWindow.block_19.display(value[1]["block"])
                self.secondWindow.rece_19.display(value[1]["rece"]["total"])
                self.secondWindow.error_19.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_19.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_19.display(ratio)
                processed = True
                self.secondWindow.player_name_19.show()
                self.secondWindow.hit_19.show()
                self.secondWindow.serve_19.show()
                self.secondWindow.block_19.show()
                self.secondWindow.rece_19.show()
                self.secondWindow.error_19.show()
                self.secondWindow.hit_pct_19.show()
                self.secondWindow.rece_pct_19.show()
                self.secondWindow.l_hits_19.show()
                self.secondWindow.l_serve_19.show()
                self.secondWindow.l_block_19.show()
                self.secondWindow.l_rece_19.show()
                self.secondWindow.l_error_19.show()
            else:
                self.secondWindow.player_name_19.hide()
                self.secondWindow.hit_19.hide()
                self.secondWindow.serve_19.hide()
                self.secondWindow.block_19.hide()
                self.secondWindow.rece_19.hide()
                self.secondWindow.error_19.hide()
                self.secondWindow.hit_pct_19.hide()
                self.secondWindow.rece_pct_19.hide()
                self.secondWindow.l_hits_19.hide()
                self.secondWindow.l_serve_19.hide()
                self.secondWindow.l_block_19.hide()
                self.secondWindow.l_rece_19.hide()
                self.secondWindow.l_error_19.hide()

            # p8 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 5:
                self.secondWindow.player_name_20.setText(fulltext)
                self.secondWindow.hit_20.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_20.display(value[1]["serve"]["kill"])
                self.secondWindow.block_20.display(value[1]["block"])
                self.secondWindow.rece_20.display(value[1]["rece"]["total"])
                self.secondWindow.error_20.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_20.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_20.display(ratio)
                processed = True
                self.secondWindow.player_name_20.show()
                self.secondWindow.hit_20.show()
                self.secondWindow.serve_20.show()
                self.secondWindow.block_20.show()
                self.secondWindow.rece_20.show()
                self.secondWindow.error_20.show()
                self.secondWindow.hit_pct_20.show()
                self.secondWindow.rece_pct_20.show()
                self.secondWindow.l_hits_20.show()
                self.secondWindow.l_serve_20.show()
                self.secondWindow.l_block_20.show()
                self.secondWindow.l_rece_20.show()
                self.secondWindow.l_error_20.show()
            else:
                self.secondWindow.player_name_20.hide()
                self.secondWindow.hit_20.hide()
                self.secondWindow.serve_20.hide()
                self.secondWindow.block_20.hide()
                self.secondWindow.rece_20.hide()
                self.secondWindow.error_20.hide()
                self.secondWindow.hit_pct_20.hide()
                self.secondWindow.rece_pct_20.hide()
                self.secondWindow.l_hits_20.hide()
                self.secondWindow.l_serve_20.hide()
                self.secondWindow.l_block_20.hide()
                self.secondWindow.l_rece_20.hide()
                self.secondWindow.l_error_20.hide()

            # p9 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 5:
                self.secondWindow.player_name_21.setText(fulltext)
                self.secondWindow.hit_21.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_21.display(value[1]["serve"]["kill"])
                self.secondWindow.block_21.display(value[1]["block"])
                self.secondWindow.rece_21.display(value[1]["rece"]["total"])
                self.secondWindow.error_21.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_21.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_21.display(ratio)
                processed = True
                self.secondWindow.player_name_21.show()
                self.secondWindow.hit_21.show()
                self.secondWindow.serve_21.show()
                self.secondWindow.block_21.show()
                self.secondWindow.rece_21.show()
                self.secondWindow.error_21.show()
                self.secondWindow.hit_pct_21.show()
                self.secondWindow.rece_pct_21.show()
                self.secondWindow.l_hits_21.show()
                self.secondWindow.l_serve_21.show()
                self.secondWindow.l_block_21.show()
                self.secondWindow.l_rece_21.show()
                self.secondWindow.l_error_21.show()
            else:
                self.secondWindow.player_name_21.hide()
                self.secondWindow.hit_21.hide()
                self.secondWindow.serve_21.hide()
                self.secondWindow.block_21.hide()
                self.secondWindow.rece_21.hide()
                self.secondWindow.error_21.hide()
                self.secondWindow.hit_pct_21.hide()
                self.secondWindow.rece_pct_21.hide()
                self.secondWindow.l_hits_21.hide()
                self.secondWindow.l_serve_21.hide()
                self.secondWindow.l_block_21.hide()
                self.secondWindow.l_rece_21.hide()
                self.secondWindow.l_error_21.hide()

            # p10 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 7:
                self.secondWindow.player_name_22.setText(fulltext)
                self.secondWindow.hit_22.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_22.display(value[1]["serve"]["kill"])
                self.secondWindow.block_22.display(value[1]["block"])
                self.secondWindow.rece_22.display(value[1]["rece"]["total"])
                self.secondWindow.error_22.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_22.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_22.display(ratio)
                processed = True
                self.secondWindow.player_name_22.show()
                self.secondWindow.hit_22.show()
                self.secondWindow.serve_22.show()
                self.secondWindow.block_22.show()
                self.secondWindow.rece_22.show()
                self.secondWindow.error_22.show()
                self.secondWindow.hit_pct_22.show()
                self.secondWindow.rece_pct_22.show()
                self.secondWindow.l_hits_22.show()
                self.secondWindow.l_serve_22.show()
                self.secondWindow.l_block_22.show()
                self.secondWindow.l_rece_22.show()
                self.secondWindow.l_error_22.show()
            else:
                self.secondWindow.player_name_22.hide()
                self.secondWindow.hit_22.hide()
                self.secondWindow.serve_22.hide()
                self.secondWindow.block_22.hide()
                self.secondWindow.rece_22.hide()
                self.secondWindow.error_22.hide()
                self.secondWindow.hit_pct_22.hide()
                self.secondWindow.rece_pct_22.hide()
                self.secondWindow.l_hits_22.hide()
                self.secondWindow.l_serve_22.hide()
                self.secondWindow.l_block_22.hide()
                self.secondWindow.l_rece_22.hide()
                self.secondWindow.l_error_22.hide()

            # p11 away
            if processed:
                value = results.popitem(False)
                number = value[0]
                fulltext = str(number)
                for p in self.game_state.players[1]:
                    if p.Number == number:
                        fulltext = fulltext + " " + p.Name
                processed = False
            if value and value[1]["group"] < 7:
                self.secondWindow.player_name_23.setText(fulltext)
                self.secondWindow.hit_23.display(value[1]["hit"]["kill"])
                self.secondWindow.serve_23.display(value[1]["serve"]["kill"])
                self.secondWindow.block_23.display(value[1]["block"])
                self.secondWindow.rece_23.display(value[1]["rece"]["total"])
                self.secondWindow.error_23.display(value[1]["error"])
                if value[1]["hit"]["total"] > 0:
                    ratio = int(
                        value[1]["hit"]["kill"] / (value[1]["hit"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.hit_pct_23.display(ratio)
                if value[1]["rece"]["total"] > 0:
                    ratio = int(
                        value[1]["rece"]["win"] / (value[1]["rece"]["total"]) * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.rece_pct_23.display(ratio)
                processed = True
                self.secondWindow.player_name_23.show()
                self.secondWindow.hit_23.show()
                self.secondWindow.serve_23.show()
                self.secondWindow.block_23.show()
                self.secondWindow.rece_23.show()
                self.secondWindow.error_23.show()
                self.secondWindow.hit_pct_23.show()
                self.secondWindow.rece_pct_23.show()
                self.secondWindow.l_hits_23.show()
                self.secondWindow.l_serve_23.show()
                self.secondWindow.l_block_23.show()
                self.secondWindow.l_rece_23.show()
                self.secondWindow.l_error_23.show()
            else:
                self.secondWindow.player_name_23.hide()
                self.secondWindow.hit_23.hide()
                self.secondWindow.serve_23.hide()
                self.secondWindow.block_23.hide()
                self.secondWindow.rece_23.hide()
                self.secondWindow.error_23.hide()
                self.secondWindow.hit_pct_23.hide()
                self.secondWindow.rece_pct_23.hide()
                self.secondWindow.l_hits_23.hide()
                self.secondWindow.l_serve_23.hide()
                self.secondWindow.l_block_23.hide()
                self.secondWindow.l_rece_23.hide()
                self.secondWindow.l_error_23.hide()

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
