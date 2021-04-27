import os
import pickle
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from tvrscouting.organization.team_info import TeamInfo
from tvrscouting.statistics.Players.players import Player
from tvrscouting.uis.edit_team import Ui_Form as Widget


class EditTeam(QtWidgets.QWidget, Widget):
    STORED_DATA_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        ".persistent/",
    )

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_table()
        self.qt_setup()

    def qt_setup(self):
        self.save.clicked.connect(self.save_to_file)
        self.load.clicked.connect(self.load_from_file)
        self.plus.clicked.connect(self.add_row)

    def add_row(self):
        self.table.setRowCount(self.table.rowCount() + 1)

    def setup_table(self):
        self.table.setRowCount(15)
        self.table.setColumnCount(5)
        self.table.setColumnWidth(0, 3)
        self.table.setColumnWidth(1, 3)
        self.table.setColumnWidth(2, 3)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 50)

    def save_to_file(self, *, filename: str = None):
        team = TeamInfo()
        team.name = self.Teamname.text()
        team.head_coach = self.HC.text()
        team.assistant_coach = self.AC.text()
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0) and len(self.table.item(row, 0).text()):
                player_name = ""
                position = Player.PlayerPosition.Universal
                isCapitain = False
                if self.table.item(row, 3):
                    player_name = str(self.table.item(row, 3).text())
                if self.table.item(row, 1):
                    position = Player.PlayerPosition.from_string(self.table.item(row, 1).text())
                if self.table.item(row, 2):
                    isCapitain = True if str(self.table.item(row, 2).text()) == "C" else False
                player = Player(
                    int(self.table.item(row, 0).text()), position, player_name, isCapitain
                )
                player.is_las = False
                if self.table.item(row, 4) and str(self.table.item(row, 4).text()) == "LAS":
                    player.is_las = True
                team.players.append(player)
        if filename is None:
            filename = QFileDialog.getSaveFileName(
                self, "Save File", self.STORED_DATA_PATH, "*.tvrt"
            )[0]
            if not filename:
                return
        with open(filename, "wb") as picklefile:
            pickle.dump(team, picklefile)

    def load_from_file(self, *, filename: str = None):
        if filename is None:
            filename = QFileDialog.getOpenFileName(
                self, "Open File", self.STORED_DATA_PATH, "*.tvrt"
            )[0]
            if not filename:
                return
        with open(filename, "rb") as picklefile:
            team = pickle.load(picklefile)
            self.fill_view_from_team(team)

    def fill_view_from_team(self, team: TeamInfo):
        self.Teamname.setText(team.name)
        self.HC.setText(team.head_coach)
        self.AC.setText(team.assistant_coach)

        self.table.setRowCount(len(team.players))
        for index, player in enumerate(team.players):
            self.table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(player.Number)))
            self.table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(player.Position)))
            self.table.setItem(
                index, 2, QtWidgets.QTableWidgetItem("C" if player.is_capitain else "")
            )
            self.table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(player.name)))
            self.table.setItem(
                index, 4, QtWidgets.QTableWidgetItem("LAS" if player.is_las else "foreign")
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = EditTeam()
    w.show()
    sys.exit(app.exec())
