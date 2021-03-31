import os
import pickle
import re
import socket
import sys
import time

from PyQt5 import QtGui, QtWidgets

from tvrscouting.analysis.playerview import DetailedPlayerStatistics
from tvrscouting.analysis.point_graph import PointGraph
from tvrscouting.analysis.recent_scores_view import RecentScores
from tvrscouting.analysis.static import StaticWriter
from tvrscouting.serializer.serializer import Serializer
from tvrscouting.statistics import GameState
from tvrscouting.statistics.Players.players import Team
from tvrscouting.uis.first import Ui_TVRScouting
from tvrscouting.utils.errors import TVRSyntaxError


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
        # TODO: this is still a bit messy, maybe we can clean it up?->see idea from update in video
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
        self.game_state.fix_time_stamps(self.game_state)
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
        except TVRSyntaxError:
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
            self.fieldView["teams"][team].name_label.setText(self.game_state.teamnames[team])
            self.fieldView["teams"][team].point_score.display(self.game_state.score[team])
            self.fieldView["teams"][team].set_score.display(self.game_state.set_score[team])

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
            self.secondWindow = DetailedPlayerStatistics()
            s = DetailedPlayerStatistics()
        self.secondWindow.show()
        if self.ThirdWindow is None:
            self.ThirdWindow = PointGraph()
        self.ThirdWindow.show()
        if self.FourthWindow is None:
            self.FourthWindow = RecentScores()
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

        # TODO: remove
        self.remote_stats.pressed.connect(self.send_data)

    def send_data(self):
        host = "0.0.0.0"  # client ip
        port = 4005

        server = ("192.168.101.157", 4000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        data = {
            "results": [
                self.game_state.collect_stats("*"),
                self.game_state.collect_stats("/"),
            ],
            "timeline": self.game_state.return_timeline(),
            "score": {
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
            },
        }
        test = pickle.dumps(data)
        s.sendto(test, server)
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
