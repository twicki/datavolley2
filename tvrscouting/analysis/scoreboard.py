from PyQt5 import QtWidgets
from tvrscouting.statistics.Players.players import Team
from tvrscouting.uis.scoreboard import Ui_Scoreboard as Scoreboard


class TeamView:
    def __init__(self, name_label, serve_box, set_score, point_score):
        self.name_label = name_label
        self.serve_box = serve_box
        self.set_score = set_score
        self.point_score = point_score


class Scoreboard(QtWidgets.QWidget, Scoreboard):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ninety_switch.pressed.connect(self.switch_90_degrees)
        self.oneeighty_switch.pressed.connect(self.switch_180_degrees)
        self.display_horizontal = True
        self.home_team_position = 0
        self.game_state = None
        self.vertical_court_elements = [
            self.v_p1_h,
            self.v_p2_h,
            self.v_p3_h,
            self.v_p4_h,
            self.v_p5_h,
            self.v_p6_h,
            self.v_p1_g,
            self.v_p2_g,
            self.v_p3_g,
            self.v_p4_g,
            self.v_p5_g,
            self.v_p6_g,
            self.v_net,
        ]
        self.horizontal_court_elements = [
            self.h_p1_h,
            self.h_p2_h,
            self.h_p3_h,
            self.h_p4_h,
            self.h_p5_h,
            self.h_p6_h,
            self.h_p1_g,
            self.h_p2_g,
            self.h_p3_g,
            self.h_p4_g,
            self.h_p5_g,
            self.h_p6_g,
            self.h_net,
        ]
        self.horiontal_score_elements = [
            self.h_g_score,
            self.h_g_setscore,
            self.h_g_label,
            self.h_g_serve,
        ]
        self.vertical_score_elements = [
            self.v_g_score,
            self.v_g_setscore,
            self.v_g_label,
            self.v_g_serve,
        ]
        self.home_score_elements = [
            self.h_score,
            self.h_setscore,
            self.h_label,
            self.h_serve,
        ]

        self.fieldView = {"field": [[], []], "teams": [], "net": None}
        self.fieldView["teams"] = [
            TeamView(self.h_label, self.h_serve, self.h_setscore, self.h_score),
            None,
        ]
        self.court = None
        self.show_horizontal()

    def switch_180_degrees(self):
        self.home_team_position = (1 + self.home_team_position) % 2
        self.update_from_gamestate()

    def switch_90_degrees(self):
        if self.display_horizontal:
            self.show_vertical()
            self.display_horizontal = False
        else:
            self.show_horizontal()
            self.display_horizontal = True
        self.update_from_gamestate()

    def show_horizontal(self):
        for element in self.vertical_court_elements:
            element.hide()
        for element in self.horizontal_court_elements:
            element.show()
        for element in self.horiontal_score_elements:
            element.show()
        for element in self.vertical_score_elements:
            element.hide()
        self.court = self.horizontal_court_elements
        self.fieldView["teams"][1] = TeamView(
            self.h_g_label, self.h_g_serve, self.h_g_setscore, self.h_g_score
        )
        self.fieldView["field"][0].clear()
        self.fieldView["field"][1].clear()
        for index, element in enumerate(self.court):
            if index < 12:
                self.fieldView["field"][index // 6].append(element)
            else:
                self.fieldView["net"] = element

    def show_vertical(self):
        for element in self.vertical_court_elements:
            element.show()
        for element in self.horizontal_court_elements:
            element.hide()
        for element in self.horiontal_score_elements:
            element.hide()
        for element in self.vertical_score_elements:
            element.show()
        self.court = self.vertical_court_elements
        self.fieldView["teams"][1] = TeamView(
            self.v_g_label, self.v_g_serve, self.v_g_setscore, self.v_g_score
        )
        self.fieldView["field"][0].clear()
        self.fieldView["field"][1].clear()
        for index, element in enumerate(self.court):
            if index < 12:
                self.fieldView["field"][index // 6].append(element)
            else:
                self.fieldView["net"] = element

    def display_team_info(self, game_state):
        for team in range(2):
            team_position_in_view = (team + self.home_team_position) % 2
            self.fieldView["teams"][team_position_in_view].name_label.setText(
                game_state.teamnames[team]
            )
            self.fieldView["teams"][team_position_in_view].point_score.display(
                game_state.score[team]
            )
            self.fieldView["teams"][team_position_in_view].set_score.display(
                game_state.set_score[team]
            )

    def display_serving_teams(self, game_state):
        home_team_position_in_view = self.home_team_position
        guest_team_position_in_view = (self.home_team_position + 1) % 2
        if game_state._last_serve == Team.from_string("*"):
            self.fieldView["teams"][home_team_position_in_view].serve_box.setChecked(True)
            self.fieldView["teams"][guest_team_position_in_view].serve_box.setChecked(False)

        elif game_state._last_serve == Team.from_string("/"):
            self.fieldView["teams"][home_team_position_in_view].serve_box.setChecked(False)
            self.fieldView["teams"][guest_team_position_in_view].serve_box.setChecked(True)

        else:
            self.fieldView["teams"][home_team_position_in_view].serve_box.setChecked(False)
            self.fieldView["teams"][guest_team_position_in_view].serve_box.setChecked(False)

    def display_players_on_court(self, game_state):
        for team in range(2):
            team_position_in_view = (team + self.home_team_position) % 2
            for player, positionview in zip(
                game_state.court.fields[team].players,
                self.fieldView["field"][team_position_in_view],
            ):
                number = player.Number
                full_label = str(number) if number > 0 else ""
                for player_in_list in game_state.players[team]:
                    if player_in_list.Number == number:
                        full_label = str(number) + " " + player_in_list.Name
                        break
                positionview.setText(full_label)

    def update_from_gamestate(self, game_state=None):
        if game_state:
            self.game_state = game_state
        if self.game_state:
            self.display_team_info(self.game_state)
            self.display_serving_teams(self.game_state)
            self.display_players_on_court(self.game_state)
