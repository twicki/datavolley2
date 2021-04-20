import os
import sys

from PyQt5 import QtGui, QtWidgets

from tvrscouting.analysis.basic_filter_widget import Basic_Filter
from tvrscouting.statistics.Actions.GameAction import Quality
from tvrscouting.statistics.Players.players import Team
from tvrscouting.uis.playeranalysis import Ui_Form


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
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/")
        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
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
            if action.quality == Quality.Perfect or action.quality == Quality.Kill:
                leaders[name]["perfect"] += 1
        sorted_leaders = []
        for number, amounts in leaders.items():
            name = number
            team = Team.from_string(number[0])
            for player in self.players[int(team)]:
                if player.Number == int(number[1:]):
                    name = player.Name
                    break
            sorted_leaders.append([name, amounts["total"], amounts["perfect"]])
        sorted_leaders = sorted(sorted_leaders, key=lambda action: action[1], reverse=True)
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
