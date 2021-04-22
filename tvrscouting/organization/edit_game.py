import os
import pickle
import sys
from typing import List, Optional

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from tvrscouting.organization.game_meta_info import GameMetaInfo
from tvrscouting.organization.team_info import TeamInfo
from tvrscouting.uis.game_info import Ui_Form as Widget


class EditGame(QtWidgets.QWidget, Widget):
    STORED_DATA_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        ".persistent/",
    )

    def __init__(self, parent=None, game_info=None):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.qt_setup()
        self.teams: List[Optional[TeamInfo]] = [None, None]
        self.set_up_game_info(game_info)

    def set_up_game_info(self, game_info: GameMetaInfo):
        if game_info:
            self.date_line.setText(game_info.date)
            self.time_line.setText(game_info.time)
            self.season_line.setText(game_info.season)
            self.league_line.setText(game_info.league)
            self.phase_line.setText(game_info.phase)
            self.spec_line.setText(str(game_info.spectators))
            self.city_line.setText(game_info.city)
            self.hall_line.setText(game_info.hall)
            self.matchnumber_line.setText(str(game_info.matchnumber))
            sep = ", "
            refs = sep.join(game_info.refs)
            self.ref_line.setText(refs)
            for index, team in enumerate(game_info.teams):
                if team:
                    self.teams[index] = team
                    self.show_coaches[index].setText(team.head_coach)
                    self.show_teams[index].setText(team.name)

    def save_metadata(self) -> GameMetaInfo:
        info = GameMetaInfo()
        info.date = self.date_line.text()
        info.time = self.time_line.text()
        info.season = self.season_line.text()
        info.league = self.league_line.text()
        info.phase = self.phase_line.text()
        info.spectators = int(self.spec_line.text()) if self.spec_line.text() else 0
        info.city = self.city_line.text()
        info.hall = self.hall_line.text()
        info.matchnumber = int(self.matchnumber_line.text()) if self.matchnumber_line.text() else ""
        info.refs.clear()
        for ref in self.ref_line.text().split(","):
            info.refs.append(ref)
        info.teams.clear()
        for team in self.teams:
            info.teams.append(team)
        return info

    def team_to_string(self, team: Optional[TeamInfo], index: int):
        if team:
            teams = ["*", "/"]
            team_char = teams[index]
            return team.to_string(team_char)
        else:
            return ""

    def return_info_to_parent(self):
        if self.parent:
            self.parent.game.meta_info = self.save_metadata()
            if len(self.parent.textEdit.toPlainText()) == 0:
                full_string = ""
                for index, team in enumerate(self.teams):
                    full_string += self.team_to_string(team, index) + "\n"
                self.parent.textEdit.setText(full_string)
        self.close()

    def set_up_team(self, team_index=0, filename: str = None):
        if filename is None:
            filename = QFileDialog.getOpenFileName(
                self, "Open File", self.STORED_DATA_PATH, "*.tvrt"
            )[0]
            if not filename:
                return
        with open(filename, "rb") as picklefile:
            self.teams[team_index] = pickle.load(picklefile)
        self.show_coaches[team_index].setText(self.teams[team_index].head_coach)
        self.show_teams[team_index].setText(self.teams[team_index].name)

    def set_up_home_team(self):
        self.set_up_team(team_index=0)

    def set_up_guest_team(self):
        self.set_up_team(team_index=1)

    def qt_setup(self):
        self.save.clicked.connect(self.return_info_to_parent)
        self.home_team.clicked.connect(self.set_up_home_team)
        self.guest_team.clicked.connect(self.set_up_guest_team)
        self.show_teams = [self.show_home_name, self.show_guest_name]
        self.show_coaches = [self.show_home_coach, self.show_guest_coach]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = EditGame()
    w.show()
    sys.exit(app.exec())
