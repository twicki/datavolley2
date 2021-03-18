import sys
import os
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog

import datavolley2
from datavolley2.serializer.serializer import Serializer
from datavolley2.uis.playeranalysis import Ui_Form

from datavolley2.statistics import Gameaction
from datavolley2.statistics.Actions.SpecialAction import InitializePlayer
from datavolley2.statistics.Players.players import Team, Player
from datavolley2.analysis.filters import *
from datavolley2.analysis.basic_filter_widget import Basic_Filter


class Player:
    def __init__(self, bar, name, stats):
        super().__init__()
        self.bar = bar
        self.name = name
        self.stats = stats


class Main(QtWidgets.QWidget, Ui_Form, Basic_Filter):
    def __init__(self, game_state=None):
        super().__init__()
        Basic_Filter.__init__(self)
        self.game_state = None
        self.player_widgets = []
        self.intialize_players_with_widgets()

    def intialize_players_with_widgets(self):
        self.player_widgets.append(Player(self.bar1, self.name1, self.stats1))
        self.player_widgets.append(Player(self.bar2, self.name2, self.stats2))
        self.player_widgets.append(Player(self.bar3, self.name3, self.stats3))
        self.player_widgets.append(Player(self.bar4, self.name4, self.stats4))
        self.player_widgets.append(Player(self.bar5, self.name5, self.stats5))
        self.player_widgets.append(Player(self.bar6, self.name6, self.stats6))

    def analyze(self):
        leaders = {}
        total = 0
        for action in self.actions:
            name = str(action.team) + str(action.player)
            total += 1
            if name in leaders:
                leaders[name]["total"] += 1
            else:
                leaders[name] = {"total": 1, "perfect": 0}
        sorted_leaders = []
        for number, amounts in leaders.items():
            name = number
            team = Team.from_string(number[0])
            for player in self.players[int(team)]:
                if player.Number == int(number[1:]):
                    name = player.Name
                    break
            sorted_leaders.append([name, amounts["total"], amounts["perfect"]])
        sorted_leaders = sorted(
            sorted_leaders, key=lambda action: action[1], reverse=True
        )
        for player in self.player_widgets:
            player.bar.hide()
            player.name.hide()
            player.stats.hide()

        for leader, player in zip(sorted_leaders, self.player_widgets):
            player.bar.setValue(int(100 * leader[1] / total))
            player.name.setText(leader[0])
            player.stats.setText(
                str(leader[1]) + "   (" + str(int(100 * leader[2] / leader[1])) + ")%"
            )
            player.bar.show()
            player.name.show()
            player.stats.show()
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())