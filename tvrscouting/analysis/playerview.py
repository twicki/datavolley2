from PyQt5 import QtWidgets
from tvrscouting.uis.team_view import Ui_Form as TeamUI


class PlayerProfileInView:
    def __init__(
        self,
        name_label,
        other_labels,
        hits_box,
        kills_box,
        hit_pct_box,
        serve_box,
        block_box,
        rece_box,
        rece_pct_box,
        error_box,
        total_points_box,
        max_group=7,
    ):
        self.name_label = name_label
        self.other_labels = other_labels
        self.hits_box = hits_box
        self.kills_box = kills_box
        self.hit_pct_box = hit_pct_box
        self.serve_box = serve_box
        self.block_box = block_box
        self.rece_box = rece_box
        self.rece_pct_box = rece_pct_box
        self.error_box = error_box
        self.total_points_box = total_points_box
        self.max_group = max_group

    def update_from_result(self, result):
        self.name_label.setText(result[1]["name"])
        self.kills_box.display(result[1]["hit"]["kill"])
        self.hits_box.display(result[1]["hit"]["total"])
        self.serve_box.display(result[1]["serve"]["kill"])
        self.block_box.display(result[1]["block"])
        self.rece_box.display(result[1]["rece"]["total"])
        self.error_box.display(result[1]["error"])
        self.total_points_box.display(
            result[1]["hit"]["kill"] + result[1]["serve"]["kill"] + result[1]["block"]
        )
        if result[1]["hit"]["total"] > 0:
            ratio = int(result[1]["hit"]["kill"] / (result[1]["hit"]["total"]) * 100)
        else:
            ratio = 0
        self.hit_pct_box.display(ratio)
        if result[1]["rece"]["total"] > 0:
            ratio = int(result[1]["rece"]["win"] / (result[1]["rece"]["total"]) * 100)
        else:
            ratio = 0
        self.rece_pct_box.display(ratio)
        self.show_view()

    def hide_view(self):
        self.name_label.hide()
        for label in self.other_labels:
            label.hide()
        self.kills_box.hide()
        self.hits_box.hide()
        self.hit_pct_box.hide()
        self.serve_box.hide()
        self.block_box.hide()
        self.rece_box.hide()
        self.rece_pct_box.hide()
        self.error_box.hide()
        self.total_points_box.hide()

    def show_view(self):
        self.name_label.show()
        for label in self.other_labels:
            label.show()
        self.kills_box.show()
        self.hits_box.show()
        self.hit_pct_box.show()
        self.serve_box.show()
        self.block_box.show()
        self.rece_box.show()
        self.rece_pct_box.show()
        self.error_box.show()
        self.total_points_box.show()


class TeamView(QtWidgets.QWidget, TeamUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.player_profiles = []
        self.team_profile = {}
        self.qt_setup()

    def qt_setup(self):
        self.team_profile = {}
        self.team_profile["name"] = self.l_team_home
        self.team_profile["hit"] = self.home_hits
        self.team_profile["serve"] = self.home_serve
        self.team_profile["block"] = self.home_block
        self.team_profile["error"] = self.home_error
        self.player_profiles = []
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
                4,
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
                5,
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
                5,
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
                7,
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
                7,
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
                7,
            )
        )

    def update_team_view(self, results):
        self.team_profile["name"].setText(results["team"]["name"])
        self.team_profile["hit"].display(results["team"]["hit"]["kill"])
        self.team_profile["serve"].display(results["team"]["serve"]["kill"])
        self.team_profile["block"].display(results["team"]["block"])
        self.team_profile["error"].display(results["team"]["error"])

    @staticmethod
    def no_actions_performed(player_details):
        if player_details["group"] < 7:
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

    def find_candidate_results_in_team(self, result):
        candidate_found = False
        while candidate_found == False:
            if len(result) == 0:
                value = None
                candidate_found = True
            else:
                value = result.popitem(False)
                if value == None:
                    candidate_found = True
                elif not TeamView.no_actions_performed(value[1]):
                    candidate_found = True
        return value

    def update_player_views(self, results):
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

    def update_view_from_results(self, results):
        self.update_team_view(results)
        self.update_player_views(results)


class TeamViews:
    def __init__(self):
        self.views = []
        self.home_view = None
        self.guest_view = None
        self.views.append(self.home_view)
        self.views.append(self.guest_view)

    def show(self):
        if self.home_view is None:
            self.home_view = TeamView()
        if self.guest_view is None:
            self.guest_view = TeamView()
        self.views.clear()
        self.views.append(self.home_view)
        self.views.append(self.guest_view)
        for view in self.views:
            view.show()

    def update_view_from_results(self, results):
        for index, view in enumerate(self.views):
            view.update_team_view(results[index])
            view.update_player_views(results[index])
