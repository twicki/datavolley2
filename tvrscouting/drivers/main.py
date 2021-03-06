#!/usr/bin/env python3
import copy
import os
import pickle
import re
import socket
import sys
import time
from typing import List, OrderedDict

from PyQt5 import QtGui, QtWidgets

from tvrscouting.analysis.comments import CommentView
from tvrscouting.analysis.playbyplay import PlayByPlay
from tvrscouting.analysis.playerview import TeamViews
from tvrscouting.analysis.point_graph import PointGraph
from tvrscouting.analysis.recent_scores_view import RecentScores
from tvrscouting.analysis.scoreboard import Scoreboard
from tvrscouting.analysis.static import StaticWriter
from tvrscouting.live_stats.results_to_js import write_results_to_js
from tvrscouting.organization.edit_game import EditGame
from tvrscouting.serializer.serializer import Serializer
from tvrscouting.statistics.Gamestate.game import Game
from tvrscouting.statistics.Gamestate.game_state import GameState
from tvrscouting.uis.first import Ui_TVRScouting
from tvrscouting.utils.errors import TVRSyntaxError


class MainWindow(QtWidgets.QMainWindow, Ui_TVRScouting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/")

        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
        self.game = Game(game_state=GameState())

        self.fullstring = ""
        self.secondWindow = None
        self.ThirdWindow = None
        self.FourthWindow = None
        self.CommentsWindow = None
        self.Scoreboard: Scoreboard = Scoreboard()

        self.write_live_stat: bool = False
        """determines if we write the stats to the javascript file"""

        self.illegal = []

        self.details = []
        self.time_stamps = []
        self.player_profiles = [[], []]
        self.remote_server = None

        self.qt_setup()

    def get_match_info(self):
        self.game_edit = EditGame(self, self.game.meta_info)
        self.game_edit.show()

    def log_change(self, item):
        raise NotImplementedError()

    def save_file(self):
        ser = Serializer(self, self.game)
        ser.serialize()

    def load_file(self):
        ser = Serializer(self)
        self.game = ser.deserialize()
        self.fullstring = ""
        for rally in self.game.game_state.rallies:
            for action in rally.actions:
                if not action.auto_generated:
                    self.fullstring += str(action) + " "
            if self.fullstring[-1] != "\n":
                self.fullstring += "\n"
        self.game.game_state.fix_time_stamps(self.game.game_state)
        self.update()

    def write_analysis(self):
        if len(self.select_set.text()):
            set_number = int(self.select_set.text())
        else:
            set_number = -1
        sw = StaticWriter(self.game.game_state, self.game.meta_info)
        sw.analyze(set_number)
        self.select_set.clear()

    def save_and_reset(self):
        userdata = self.textEdit.toPlainText()
        if self.game:
            oldstate = self.game.game_state
        else:
            oldstate = None
        self.game.game_state = GameState()
        self.fullstring = userdata

        self.illegal.clear()
        self.time_stamps.clear()

        rallies = userdata.split("\n")
        for rally_string in rallies:
            if "team" in rally_string or "player" in rally_string:
                self.add_stings_to_game_state([rally_string])
            else:
                actions = rally_string.split()
                self.add_stings_to_game_state(actions)

        if oldstate:
            self.game.game_state.fix_time_stamps(oldstate)

        if self.fullstring[-1] == "\n":
            self.fullstring = self.fullstring[:-1]
        self.textEdit.setText(self.fullstring)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.update()

    def reset_highlighting(self):
        cursor = QtGui.QTextCursor(self.textEdit.document())
        formatting = QtGui.QTextCharFormat()
        color = QtGui.QColor("white")
        formatting.setBackground(color)
        cursor.setPosition(0, QtGui.QTextCursor.MoveAnchor)
        cursor.setPosition(len(self.fullstring), QtGui.QTextCursor.KeepAnchor)
        cursor.setCharFormat(formatting)

    def find_illegal_positions_from_strings(self):
        fulltext = self.textEdit.toPlainText()
        positions = []
        for illegal_string in self.illegal:
            output_string = ""
            for c in illegal_string:
                if c == "*":
                    output_string = output_string + "\\*"
                elif c == "+":
                    output_string = output_string + "\\+"
                elif c == ".":
                    output_string = output_string + "\\."
                else:
                    output_string = output_string + c
            for m in re.finditer(output_string, fulltext):
                positions.append((m.start(), m.end()))
        return positions

    def highlight_error_positions(self, positions):
        cursor = QtGui.QTextCursor(self.textEdit.document())
        formatting = QtGui.QTextCharFormat()
        highlight_color = QtGui.QColor("red")
        formatting.setBackground(highlight_color)
        for position in positions:
            cursor.setPosition(position[0], QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(position[1], QtGui.QTextCursor.KeepAnchor)
            cursor.setCharFormat(formatting)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)

    def highlight_errors(self):
        self.reset_highlighting()
        positions = self.find_illegal_positions_from_strings()
        self.highlight_error_positions(positions)

    def add_action_to_game_action(self, command, action_time=None):
        try:
            self.game.game_state.add_string(command, action_time)
        except TVRSyntaxError:
            self.illegal.append(command)

    def update_full_text_view(self):
        text = self.lineEdit.text()
        self.fullstring = self.fullstring + text + "\n"
        self.textEdit.setText(self.fullstring)
        self.lineEdit.clear()

    def add_stings_to_game_state(self, inputs):
        if len(self.time_stamps) == len(inputs):
            for command, action_time in zip(inputs, self.time_stamps):
                self.add_action_to_game_action(command, action_time)
        elif len(self.time_stamps):
            for command in inputs:
                self.add_action_to_game_action(command, self.time_stamps[0])
        else:
            for command in inputs:
                self.add_action_to_game_action(command)
        self.game.game_state.flush_actions()

    def add_input_to_game_state(self):
        self.time_stamps.append(time.time())
        text = self.lineEdit.text()
        actions = text.split(" ")
        self.add_stings_to_game_state(actions)
        self.time_stamps.clear()

    def display_detailed_actions(self):
        self.action_view.itemChanged.connect(self.log_change)
        self.action_view.itemChanged.disconnect()
        self.action_view.setRowCount(10000)
        self.action_view.setColumnCount(1)
        i = 0
        for rally in self.game.game_state.rallies:
            for action in rally.actions:
                self.action_view.setItem(0, i, QtGui.QTableWidgetItem(str(action)))
                self.action_view.setColumnWidth(i, 200)
                i += 1
        self.action_view.setRowCount(i)
        self.action_view.scrollToBottom()
        self.action_view.itemChanged.connect(self.log_change)

    def update_buttons(self):
        if self.remote_server:
            self.remote_on.setChecked(True)
            if self.CommentsWindow is None:
                self.CommentsWindow = CommentView()
            self.CommentsWindow.show()
        else:
            self.remote_on.setChecked(False)
            if self.CommentsWindow is not None:
                self.CommentsWindow.hide()

    def update_main_view(self):
        self.update_full_text_view()
        self.highlight_errors()
        self.display_detailed_actions()
        self.update_buttons()

    def update_player_stats(self, input_results: List[OrderedDict]):
        results = copy.deepcopy(input_results)
        self.secondWindow.update_view_from_results(results)

    def update_timeline(self):
        totals, delta = self.game.game_state.return_timeline()
        self.ThirdWindow.update_timeline(totals, delta)

    def update_recent_scores_view(self):
        score = {
            "score": self.game.game_state.return_truncated_scores(),
            "team_details": [
                {
                    "name": self.game.game_state.teamnames[0],
                    "score": self.game.game_state.score[0],
                },
                {
                    "name": self.game.game_state.teamnames[1],
                    "score": self.game.game_state.score[1],
                },
            ],
        }
        self.FourthWindow.update_view_from_results(score)

    def update_commentator_view(self, stats: List[OrderedDict]):
        if self.secondWindow is not None:
            self.update_player_stats(stats)
        if self.ThirdWindow:
            self.update_timeline()
        if self.FourthWindow:
            self.update_recent_scores_view()

    def update_scoreboard(self):
        if self.Scoreboard is None:
            self.Scoreboard = Scoreboard()
        self.Scoreboard.update_from_gamestate(self.game.game_state)
        self.Scoreboard.show()

    def write_data_to_js(self, results):
        if self.write_live_stat:
            # TODO: ideally don't pass in the full gs but only the required thing for scores
            write_results_to_js(
                results,
                self.game.game_state,
                self.game.game_state.court,
                self.game.game_state.players,
            )

    def collect_player_stats(self) -> List[OrderedDict]:
        return [
            self.game.game_state.collect_stats("*"),
            self.game.game_state.collect_stats("/"),
        ]

    def update(self):
        self.add_input_to_game_state()
        self.update_main_view()
        self.update_scoreboard()
        stats = self.collect_player_stats()
        self.update_commentator_view(stats)
        self.send_data_to_remote_server(stats)
        self.write_data_to_js(stats)

    def display_commentator_windows(self):
        if self.secondWindow is None:
            self.secondWindow = TeamViews()
        self.secondWindow.show()
        if self.ThirdWindow is None:
            self.ThirdWindow = PointGraph()
        self.ThirdWindow.show()
        if self.FourthWindow is None:
            self.FourthWindow = RecentScores()
        self.FourthWindow.show()

    def turn_on_or_off_remote(self):
        remote = self.remote_on.isChecked()

        if remote and self.remote_server is None:
            self.setup_remote_server()
        if not remote:
            self.remote_server = None
        self.update_buttons()

    def print_play_by_play(self):
        if len(self.select_set.text()):
            set_number = int(self.select_set.text())
        else:
            set_number = self.game.game_state.set_score[0] + self.game.game_state.set_score[1]
        analyzer = PlayByPlay(self.game)
        analyzer.analyze(set_number)
        self.select_set.clear()

    def qt_setup(self):
        self.pushButton.clicked.connect(self.display_commentator_windows)
        self.pushButton_2.clicked.connect(self.save_and_reset)
        self.pushButton_3.clicked.connect(self.write_analysis)
        self.lineEdit.returnPressed.connect(self.update)
        self.lineEdit.textChanged.connect(self.get_times)
        self.saveFile.clicked.connect(self.save_file)
        self.loadFile.clicked.connect(self.load_file)
        self.remote_stats.pressed.connect(self.setup_remote_server)
        self.remote_on.clicked.connect(self.turn_on_or_off_remote)
        self.matchInfo.clicked.connect(self.get_match_info)
        self.livehost.clicked.connect(self.turn_on_or_off_live_stats)
        self.playbyplay.clicked.connect(self.print_play_by_play)
        self.Scoreboard.show()

    def turn_on_or_off_live_stats(self):
        self.write_live_stat = self.livehost.isChecked()

    def setup_remote_server(self):
        # TODO: don't read from lineEdit but have a popup
        self.remote_server = self.lineEdit.text()
        self.lineEdit.clear()
        self.update()

    def send_data_to_remote_server(self, results: List[OrderedDict]):
        if self.remote_server:
            host = "0.0.0.0"  # client ip
            port = 4005

            # server = ("192.168.101.157", 4000)
            server = (self.remote_server, 4000)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((host, port))
            data = {
                "results": results,
                "timeline": self.game.game_state.return_timeline(),
                "score": {
                    "score": self.game.game_state.return_truncated_scores(),
                    "team_details": [
                        {
                            "name": self.game.game_state.teamnames[0],
                            "score": self.game.game_state.score[0],
                        },
                        {
                            "name": self.game.game_state.teamnames[1],
                            "score": self.game.game_state.score[1],
                        },
                    ],
                },
                "comments": "",
            }
            if self.CommentsWindow:
                comments = self.CommentsWindow.text_box.toPlainText()
                data["comments"] = comments
            compressed_data = pickle.dumps(data)
            s.sendto(compressed_data, server)
            s.close()

    def get_times(self):
        if len(self.lineEdit.text()):
            last_character = self.lineEdit.text()[-1]
            if last_character == " ":
                self.time_stamps.append(time.time())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
