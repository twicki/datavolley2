import sys
import os
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog

import tvrscouting
from tvrscouting.serializer.serializer import Serializer
from tvrscouting.uis.zoneanalysis import Ui_Form

from tvrscouting.statistics import Gameaction
from tvrscouting.statistics.Actions.SpecialAction import InitializePlayer
from tvrscouting.statistics.Players.players import Team, Player
from tvrscouting.analysis.filters import *
from tvrscouting.analysis.basic_filter_widget import Basic_Filter


class Position:
    def __init__(self, total, percentage, first, second, thrid, fourth, fifth):
        super().__init__()
        self.total = total
        self.percentage = percentage
        self.leaders = [first, second, thrid, fourth, fifth]


def keyPressed(evt):
    print("Key pressed")


class Main(QtWidgets.QWidget, Ui_Form, Basic_Filter):
    sigKeyPress = QtCore.pyqtSignal(object)

    def __init__(self, game_state=None):
        super().__init__()
        Basic_Filter.__init__(self)

        self.analyze_from.setChecked(True)
        self.analyze_from.clicked.connect(self.check_from)
        self.analyze_to.setChecked(False)
        self.analyze_to.clicked.connect(self.check_to)

        self.reset_all_filters()
        self.court = []
        self.intialize_court_with_widgets()

    def check_from(self):
        self.analyze_from.setChecked(True)
        self.analyze_to.setChecked(False)
        self.position_to_check = 0
        self.apply_all_filters()

    def check_to(self):
        self.analyze_from.setChecked(False)
        self.analyze_to.setChecked(True)
        self.position_to_check = 1
        self.apply_all_filters()

    def intialize_court_with_widgets(self):
        self.court.append(
            Position(
                self.total_1,
                self.total_perc_1,
                self.lead_1,
                self.second_1,
                self.third_1,
                self.fourth_1,
                self.fifth_1,
            )
        )
        self.court.append(
            Position(
                self.total_2,
                self.total_perc_2,
                self.lead_2,
                self.second_2,
                self.third_2,
                self.fourth_2,
                self.fifth_2,
            )
        )
        self.court.append(
            Position(
                self.total_3,
                self.total_perc_3,
                self.lead_3,
                self.second_3,
                self.third_3,
                self.fourth_3,
                self.fifth_3,
            )
        )
        self.court.append(
            Position(
                self.total_4,
                self.total_perc_4,
                self.lead_4,
                self.second_4,
                self.third_4,
                self.fourth_4,
                self.fifth_4,
            )
        )
        self.court.append(
            Position(
                self.total_5,
                self.total_perc_5,
                self.lead_5,
                self.second_5,
                self.third_5,
                self.fourth_5,
                self.fifth_5,
            )
        )
        self.court.append(
            Position(
                self.total_6,
                self.total_perc_6,
                self.lead_6,
                self.second_6,
                self.third_6,
                self.fourth_6,
                self.fifth_6,
            )
        )
        self.court.append(
            Position(
                self.total_7,
                self.total_perc_7,
                self.lead_7,
                self.second_7,
                self.third_7,
                self.fourth_7,
                self.fifth_7,
            )
        )
        self.court.append(
            Position(
                self.total_8,
                self.total_perc_8,
                self.lead_8,
                self.second_8,
                self.third_8,
                self.fourth_8,
                self.fifth_8,
            )
        )
        self.court.append(
            Position(
                self.total_9,
                self.total_perc_9,
                self.lead_9,
                self.second_9,
                self.third_9,
                self.fourth_9,
                self.fifth_9,
            )
        )
        self.court.append(
            Position(
                self.total_10,
                self.total_perc_10,
                self.lead_10,
                self.second_10,
                self.third_10,
                self.fourth_10,
                self.fifth_10,
            )
        )

    def analyze(self):
        for position in range(9):
            total = 0
            leaders = {}
            for action in self.actions:
                if int(action.direction[self.position_to_check]) == (position + 1):
                    total += 1
                    name = str(action.team) + str(action.player)
                    if name in leaders:
                        leaders[name] += 1
                    else:
                        leaders[name] = 1
            sorted_leaders = []
            for number, amount in leaders.items():
                name = number
                team = Team.from_string(number[0])
                for player in self.players[int(team)]:
                    if player.Number == int(number[1:]):
                        name = player.Name
                        break
                sorted_leaders.append([name, amount])
            sorted_leaders = sorted(
                sorted_leaders, key=lambda action: action[1], reverse=True
            )
            for leader in self.court[position].leaders:
                leader.setText("")
            self.court[position].total.setText("")
            self.court[position].percentage.setText("")
            self.court[position].total.setText(str(total) if total > 0 else "")
            self.court[position].percentage.setText(
                str(int(100 * (total / len(self.actions)))) + " %"
                if len(self.actions) and int(100 * (total / len(self.actions))) > 0
                else ""
            )
            for label, leader in zip(self.court[position].leaders, sorted_leaders):
                label.setText(str(leader[0]) + " : " + str(leader[1]))

        total = 0
        leaders = {}
        for action in self.actions:
            if int(action.direction[self.position_to_check]) == 0:
                total += 1
                name = str(action.team) + str(action.player)
                if name in leaders:
                    leaders[name] += 1
                else:
                    leaders[name] = 1
        sorted_leaders = []
        for number, amount in leaders.items():
            name = number
            team = Team.from_string(number[0])
            for player in self.players[int(team)]:
                if player.Number == int(number[1:]):
                    name = player.Name
                    break
            sorted_leaders.append([name, amount])
        sorted_leaders = sorted(
            sorted_leaders, key=lambda action: action[1], reverse=True
        )
        for leader in self.court[9].leaders:
            leader.setText("")
        self.court[9].total.setText("")
        self.court[9].percentage.setText("")
        self.court[9].total.setText(str(total) if total > 0 else "")
        self.court[9].percentage.setText(
            str(int(100 * (total / len(self.actions)))) + " %"
            if len(self.actions) and int(100 * (total / len(self.actions))) > 0
            else ""
        )
        for label, leader in zip(self.court[9].leaders, sorted_leaders):
            label.setText(str(leader[0]) + " : " + str(leader[1]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Main()
    w.show()
    w.sigKeyPress.connect(keyPressed)
    sys.exit(app.exec())