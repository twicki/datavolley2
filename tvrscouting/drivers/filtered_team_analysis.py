import copy
import os
import sys
from typing import List, OrderedDict

from PyQt5 import QtGui, QtWidgets

from tvrscouting.analysis.basic_filter_widget import Basic_Filter
from tvrscouting.analysis.playerview import PlayerProfileInView, TeamView
from tvrscouting.statistics.Actions.GameAction import Action, Gameaction, Quality
from tvrscouting.statistics.Players.players import Player, Team
from tvrscouting.uis.filtered_team_view import Ui_Form


def collect_stats(
    players: List[List[Player]], actions: List[Gameaction], teamname: str
) -> OrderedDict:
    team = Team.from_string(teamname)
    playerstats = OrderedDict()

    players[int(team)] = sorted(players[int(team)], key=lambda player: player.Position)
    allplayers = players[int(team)]

    for player in allplayers:
        playerstats[player.Number] = {}
        playerstats[player.Number]["played"] = False
        for teams_player in players[int(team)]:
            if teams_player.Number == player.Number:
                playerstats[player.Number]["name"] = str(player.Number) + " " + teams_player.Name
        playerstats[player.Number]["serve"] = {}
        playerstats[player.Number]["serve"]["kill"] = 0
        playerstats[player.Number]["serve"]["total"] = 0
        playerstats[player.Number]["rece"] = {}
        playerstats[player.Number]["rece"]["win"] = 0
        playerstats[player.Number]["rece"]["total"] = 0
        playerstats[player.Number]["rece"]["perc"] = 0
        playerstats[player.Number]["hit"] = {}
        playerstats[player.Number]["hit"]["kill"] = 0
        playerstats[player.Number]["hit"]["total"] = 0
        playerstats[player.Number]["hit"]["perc"] = 0
        playerstats[player.Number]["error"] = 0
        playerstats[player.Number]["block"] = 0
        playerstats[player.Number]["points"] = 0
    for player in allplayers:
        for action in actions:
            # is is the right player on the right team
            if action.team == team:
                if action.player == player.Number:
                    playerstats[player.Number]["played"] = True
                    playerstats[player.Number]["group"] = int(player.Position)
                    # serve statistics
                    if action.action == Action.Serve:
                        playerstats[player.Number]["serve"]["total"] += 1
                        if action.quality == Quality.Kill:
                            playerstats[player.Number]["serve"]["kill"] += 1
                            playerstats[player.Number]["points"] += 1
                        elif action.quality == Quality.Error:
                            playerstats[player.Number]["error"] += 1

                    # hitting statistics
                    elif action.action == Action.Hit:
                        playerstats[player.Number]["hit"]["total"] += 1
                        if action.quality == Quality.Kill:
                            playerstats[player.Number]["hit"]["kill"] += 1
                            playerstats[player.Number]["points"] += 1
                        elif action.quality == Quality.Error:
                            playerstats[player.Number]["error"] += 1

                    # blocking statistics
                    elif action.action == Action.Block:
                        if action.quality == Quality.Kill:
                            playerstats[player.Number]["block"] += 1
                            playerstats[player.Number]["points"] += 1
                        elif action.quality == Quality.Error:
                            playerstats[player.Number]["error"] += 1

                    # rece statistics
                    elif action.action == Action.Reception:
                        playerstats[player.Number]["rece"]["total"] += 1
                        if action.quality == Quality.Perfect or action.quality == Quality.Good:
                            playerstats[player.Number]["rece"]["win"] += 1
                        elif action.quality == Quality.Error:
                            playerstats[player.Number]["error"] += 1
                    # other actions
                    else:
                        if action.quality == Quality.Kill:
                            playerstats[player.Number]["points"] += 1
                        elif action.quality == Quality.Error:
                            playerstats[player.Number]["error"] += 1

    for numbers in [number for number, stats in playerstats.items() if stats["played"] is False]:
        del playerstats[numbers]

    playerstats["team"] = {}
    playerstats["team"]["name"] = "Full Team"
    playerstats["team"]["group"] = 7
    playerstats["team"]["serve"] = {}
    playerstats["team"]["serve"]["kill"] = 0
    playerstats["team"]["serve"]["total"] = 0
    playerstats["team"]["rece"] = {}
    playerstats["team"]["rece"]["win"] = 0
    playerstats["team"]["rece"]["total"] = 0
    playerstats["team"]["rece"]["perc"] = 0
    playerstats["team"]["hit"] = {}
    playerstats["team"]["hit"]["kill"] = 0
    playerstats["team"]["hit"]["total"] = 0
    playerstats["team"]["hit"]["perc"] = 0
    playerstats["team"]["error"] = 0
    playerstats["team"]["block"] = 0
    playerstats["team"]["points"] = 0
    for action in actions:
        # is is the right player on the right team
        if action.team == team:
            # serve statistics
            if action.action == Action.Serve:
                playerstats["team"]["serve"]["total"] += 1
                if action.quality == Quality.Kill:
                    playerstats["team"]["serve"]["kill"] += 1
                    playerstats["team"]["points"] += 1
                elif action.quality == Quality.Error:
                    playerstats["team"]["error"] += 1

            # hitting statistics
            elif action.action == Action.Hit:
                playerstats["team"]["hit"]["total"] += 1
                if action.quality == Quality.Kill:
                    playerstats["team"]["hit"]["kill"] += 1
                    playerstats["team"]["points"] += 1
                elif action.quality == Quality.Error:
                    playerstats["team"]["error"] += 1

            # blocking statistics
            elif action.action == Action.Block:
                if action.quality == Quality.Kill:
                    playerstats["team"]["block"] += 1
                    playerstats["team"]["points"] += 1
                elif action.quality == Quality.Error:
                    playerstats["team"]["error"] += 1

            # blocking statistics
            elif action.action == Action.Reception:
                playerstats["team"]["rece"]["total"] += 1
                if action.quality == Quality.Perfect or action.quality == Quality.Good:
                    playerstats["team"]["rece"]["win"] += 1
                elif action.quality == Quality.Error:
                    playerstats["team"]["error"] += 1
            # other actions
            else:
                if action.quality == Quality.Kill:
                    playerstats["team"]["points"] += 1
                elif action.quality == Quality.Error:
                    playerstats["team"]["error"] += 1

    for stats in playerstats.values():
        stats["rece"]["perc"] = (
            int(100 * stats["rece"]["win"] / stats["rece"]["total"])
            if stats["rece"]["total"] > 0
            else 0
        )
        stats["hit"]["perc"] = (
            int(100 * stats["hit"]["kill"] / stats["hit"]["total"])
            if stats["hit"]["total"] > 0
            else 0
        )

    return playerstats


class MainWindow(QtWidgets.QWidget, Ui_Form, Basic_Filter):
    def __init__(self):
        super().__init__()
        Basic_Filter.__init__(self)
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/")
        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
        self.team: int = 0 if self.HomeButton.isChecked() else 1
        self.qt_setup()

    def analyze(self):
        results = [
            collect_stats(self.players, self.actions, "*"),
            collect_stats(self.players, self.actions, "/"),
        ]
        self.update_player_views(results[self.team])
        self.update_team_view(results[self.team])

    def find_candidate_results_in_team(self, result):
        candidate_found = False
        while candidate_found is False:
            if len(result) == 0:
                value = None
                candidate_found = True
            else:
                value = result.popitem(False)
                if value is None:
                    candidate_found = True
                elif not TeamView.no_actions_performed(value[1]):
                    candidate_found = True
        return value

    def update_player_views(self, input_results):
        results = copy.deepcopy(input_results)
        processed = True
        for player_view in self.player_profiles:
            if processed:
                candidate_results = self.find_candidate_results_in_team(results)
                processed = False

            if candidate_results and candidate_results[1]["group"] < player_view.max_group:
                processed = True
                player_view.update_from_result(candidate_results)
            else:
                player_view.hide_view()

    def update_team_view(self, results):
        self.team_profile.update_from_result((None, results["team"]))

    def update_team(self):
        self.team = 0 if self.HomeButton.isChecked() else 1
        self.apply_all_filters()

    def qt_setup(self):
        self.HomeButton.clicked.connect(self.update_team)
        self.GuestButton.clicked.connect(self.update_team)

        self.team_profile: PlayerProfileInView = PlayerProfileInView(
            self.player_name_16,
            [
                self.l_hits_16,
                self.l_serve_16,
                self.l_block_16,
                self.l_rece_16,
            ],
            self.total_hits_16,
            self.hit_16,
            self.hit_pct_16,
            self.serve_16,
            self.block_16,
            self.rece_16,
            self.rece_pct_16,
            self.error_16,
            self.total_points_16,
            8,
        )
        self.player_profiles: List[PlayerProfileInView] = []
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name,
                [
                    self.l_hits,
                    self.l_serve,
                    self.l_block,
                    self.l_rece,
                ],
                self.total_hits,
                self.hit,
                self.hit_pct,
                self.serve,
                self.block,
                self.rece,
                self.rece_pct,
                self.error,
                self.total_points,
                3,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_2,
                [
                    self.l_hits_2,
                    self.l_serve_2,
                    self.l_block_2,
                    self.l_rece_2,
                ],
                self.total_hits_2,
                self.hit_2,
                self.hit_pct_2,
                self.serve_2,
                self.block_2,
                self.rece_2,
                self.rece_pct_2,
                self.error_2,
                self.total_points_2,
                3,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_3,
                [
                    self.l_hits_3,
                    self.l_serve_3,
                    self.l_block_3,
                    self.l_rece_3,
                ],
                self.total_hits_3,
                self.hit_3,
                self.hit_pct_3,
                self.serve_3,
                self.block_3,
                self.rece_3,
                self.rece_pct_3,
                self.error_3,
                self.total_points_3,
                3,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_4,
                [
                    self.l_hits_4,
                    self.l_serve_4,
                    self.l_block_4,
                    self.l_rece_4,
                ],
                self.total_hits_4,
                self.hit_4,
                self.hit_pct_4,
                self.serve_4,
                self.block_4,
                self.rece_4,
                self.rece_pct_4,
                self.error_4,
                self.total_points_4,
                3,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_5,
                [
                    self.l_hits_5,
                    self.l_serve_5,
                    self.l_block_5,
                    self.l_rece_5,
                ],
                self.total_hits_5,
                self.hit_5,
                self.hit_pct_5,
                self.serve_5,
                self.block_5,
                self.rece_5,
                self.rece_pct_5,
                self.error_5,
                self.total_points_5,
                4,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_6,
                [
                    self.l_hits_6,
                    self.l_serve_6,
                    self.l_block_6,
                    self.l_rece_6,
                ],
                self.total_hits_6,
                self.hit_6,
                self.hit_pct_6,
                self.serve_6,
                self.block_6,
                self.rece_6,
                self.rece_pct_6,
                self.error_6,
                self.total_points_6,
                4,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_7,
                [
                    self.l_hits_7,
                    self.l_serve_7,
                    self.l_block_7,
                    self.l_rece_7,
                ],
                self.total_hits_7,
                self.hit_7,
                self.hit_pct_7,
                self.serve_7,
                self.block_7,
                self.rece_7,
                self.rece_pct_7,
                self.error_7,
                self.total_points_7,
                4,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_8,
                [
                    self.l_hits_8,
                    self.l_serve_8,
                    self.l_block_8,
                    self.l_rece_8,
                ],
                self.total_hits_8,
                self.hit_8,
                self.hit_pct_8,
                self.serve_8,
                self.block_8,
                self.rece_8,
                self.rece_pct_8,
                self.error_8,
                self.total_points_8,
                4,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_9,
                [
                    self.l_hits_9,
                    self.l_serve_9,
                    self.l_block_9,
                    self.l_rece_9,
                ],
                self.total_hits_9,
                self.hit_9,
                self.hit_pct_9,
                self.serve_9,
                self.block_9,
                self.rece_9,
                self.rece_pct_9,
                self.error_9,
                self.total_points_9,
                5,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_10,
                [
                    self.l_hits_10,
                    self.l_serve_10,
                    self.l_block_10,
                    self.l_rece_10,
                ],
                self.total_hits_10,
                self.hit_10,
                self.hit_pct_10,
                self.serve_10,
                self.block_10,
                self.rece_10,
                self.rece_pct_10,
                self.error_10,
                self.total_points_10,
                5,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_11,
                [
                    self.l_hits_11,
                    self.l_serve_11,
                    self.l_block_11,
                    self.l_rece_11,
                ],
                self.total_hits_11,
                self.hit_11,
                self.hit_pct_11,
                self.serve_11,
                self.block_11,
                self.rece_11,
                self.rece_pct_11,
                self.error_11,
                self.total_points_11,
                5,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_12,
                [
                    self.l_hits_12,
                    self.l_serve_12,
                    self.l_block_12,
                    self.l_rece_12,
                ],
                self.total_hits_12,
                self.hit_12,
                self.hit_pct_12,
                self.serve_12,
                self.block_12,
                self.rece_12,
                self.rece_pct_12,
                self.error_12,
                self.total_points_12,
                5,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_13,
                [
                    self.l_hits_13,
                    self.l_serve_13,
                    self.l_block_13,
                    self.l_rece_13,
                ],
                self.total_hits_13,
                self.hit_13,
                self.hit_pct_13,
                self.serve_13,
                self.block_13,
                self.rece_13,
                self.rece_pct_13,
                self.error_13,
                self.total_points_13,
                7,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_14,
                [
                    self.l_hits_14,
                    self.l_serve_14,
                    self.l_block_14,
                    self.l_rece_14,
                ],
                self.total_hits_14,
                self.hit_14,
                self.hit_pct_14,
                self.serve_14,
                self.block_14,
                self.rece_14,
                self.rece_pct_14,
                self.error_14,
                self.total_points_14,
                7,
            )
        )
        self.player_profiles.append(
            PlayerProfileInView(
                self.player_name_15,
                [
                    self.l_hits_15,
                    self.l_serve_15,
                    self.l_block_15,
                    self.l_rece_15,
                ],
                self.total_hits_15,
                self.hit_15,
                self.hit_pct_15,
                self.serve_15,
                self.block_15,
                self.rece_15,
                self.rece_pct_15,
                self.error_15,
                self.total_points_15,
                7,
            )
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
