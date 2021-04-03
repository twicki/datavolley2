import sys
import os
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
import tvrscouting
from tvrscouting.uis.remote_comm import Ui_MainWindow
import socket
from PyQt5.QtCore import QTimer

from tvrscouting.uis.second import Ui_Form as commentatorUI
from tvrscouting.uis.third import Ui_Form as thridUI
from tvrscouting.uis.fourth import Ui_Form as fourthUI
import pickle
from tvrscouting.statistics.Gamestate.game_state import GameState


class PlayerProfileInView:
    def __init__(
        self,
        name_label,
        other_labels,
        hits_box,
        hit_pct_box,
        serve_box,
        block_box,
        rece_box,
        rece_pct_box,
        error_box,
        max_group=7,
    ):
        self.name_label = name_label
        self.other_labels = other_labels
        self.hits_box = hits_box
        self.hit_pct_box = hit_pct_box
        self.serve_box = serve_box
        self.block_box = block_box
        self.rece_box = rece_box
        self.rece_pct_box = rece_pct_box
        self.error_box = error_box
        self.max_group = max_group

    def update_from_result(self, result):
        self.name_label.setText(result[1]["name"])
        self.hits_box.display(result[1]["hit"]["kill"])
        self.serve_box.display(result[1]["serve"]["kill"])
        self.block_box.display(result[1]["block"])
        self.rece_box.display(result[1]["rece"]["total"])
        self.error_box.display(result[1]["error"])
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
        self.hits_box.hide()
        self.hit_pct_box.hide()
        self.serve_box.hide()
        self.block_box.hide()
        self.rece_box.hide()
        self.rece_pct_box.hide()
        self.error_box.hide()

    def show_view(self):
        self.name_label.show()
        for label in self.other_labels:
            label.show()
        self.hits_box.show()
        self.hit_pct_box.show()
        self.serve_box.show()
        self.block_box.show()
        self.rece_box.show()
        self.rece_pct_box.show()
        self.error_box.show()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/")
        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
        self.pushButton.pressed.connect(self.setup_server)
        self.timer = QTimer(self)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.fetch_data)
        self.pushButton_2.pressed.connect(self.setup_uis)
        self.s = None

        self.secondWindow = None
        self.ThirdWindow = None
        self.FourthWindow = None

    def fetch_data(self):
        try:
            data, addr = self.s.recvfrom(536870912)
            print("data from: " + str(addr))
            self.data = pickle.loads(data)
            self.update_commentator_view()
        except socket.timeout:
            pass

    def update_notes(self):
        self.textBrowser.setText(self.data["comments"])

    def update_commentator_view(self):
        self.update_notes()
        if self.secondWindow is not None:
            self.update_player_stats()
        if self.ThirdWindow:
            self.update_timeline()
        if self.FourthWindow:
            self.update_recent_scores_view()

    def update_player_stats(self):
        self.secondWindow.update_view_from_results(self.data["results"])

    def update_timeline(self):
        self.ThirdWindow.update_timeline(self.data["timeline"][0], self.data["timeline"][1])

    def update_recent_scores_view(self):
        score = self.data["score"]
        self.FourthWindow.update_view_from_results(score)

    def setup_server(self):
        host = "0.0.0.0"  # Server ip
        port = 4000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((host, port))
        self.s.settimeout(0.01)
        print("Server Started")
        self.timer.start()

    def setup_uis(self):
        if self.secondWindow is None:
            self.secondWindow = SecondWindow()
            s = SecondWindow()
        self.secondWindow.show()
        if self.ThirdWindow is None:
            self.ThirdWindow = ThirdWindow()
        self.ThirdWindow.show()
        if self.FourthWindow is None:
            self.FourthWindow = FourthWindow()
        self.FourthWindow.show()


class SecondWindow(QtWidgets.QWidget, commentatorUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.player_profiles = [[], []]
        self.team_profiles = [{}, {}]
        self.qt_setup()

    def qt_setup(self):
        self.team_profiles = [{}, {}]
        self.team_profiles[0]["name"] = self.l_team_home
        self.team_profiles[0]["hit"] = self.home_hits
        self.team_profiles[0]["serve"] = self.home_serve
        self.team_profiles[0]["block"] = self.home_block
        self.team_profiles[0]["error"] = self.home_error
        self.team_profiles[1]["name"] = self.l_team_guest
        self.team_profiles[1]["hit"] = self.guest_hits
        self.team_profiles[1]["serve"] = self.guest_serve
        self.team_profiles[1]["block"] = self.guest_block
        self.team_profiles[1]["error"] = self.guest_error
        self.player_profiles = [[], []]
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name,
                [
                    self.l_hits,
                    self.l_serve,
                    self.l_block,
                    self.l_rece,
                    self.l_error,
                ],
                self.hit,
                self.hit_pct,
                self.serve,
                self.block,
                self.rece,
                self.rece_pct,
                self.error,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_2,
                [
                    self.l_hits_2,
                    self.l_serve_2,
                    self.l_block_2,
                    self.l_rece_2,
                    self.l_error_2,
                ],
                self.hit_2,
                self.hit_pct_2,
                self.serve_2,
                self.block_2,
                self.rece_2,
                self.rece_pct_2,
                self.error_2,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_3,
                [
                    self.l_hits_3,
                    self.l_serve_3,
                    self.l_block_3,
                    self.l_rece_3,
                    self.l_error_3,
                ],
                self.hit_3,
                self.hit_pct_3,
                self.serve_3,
                self.block_3,
                self.rece_3,
                self.rece_pct_3,
                self.error_3,
                3,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_4,
                [
                    self.l_hits_4,
                    self.l_serve_4,
                    self.l_block_4,
                    self.l_rece_4,
                    self.l_error_4,
                ],
                self.hit_4,
                self.hit_pct_4,
                self.serve_4,
                self.block_4,
                self.rece_4,
                self.rece_pct_4,
                self.error_4,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_5,
                [
                    self.l_hits_5,
                    self.l_serve_5,
                    self.l_block_5,
                    self.l_rece_5,
                    self.l_error_5,
                ],
                self.hit_5,
                self.hit_pct_5,
                self.serve_5,
                self.block_5,
                self.rece_5,
                self.rece_pct_5,
                self.error_5,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_6,
                [
                    self.l_hits_6,
                    self.l_serve_6,
                    self.l_block_6,
                    self.l_rece_6,
                    self.l_error_6,
                ],
                self.hit_6,
                self.hit_pct_6,
                self.serve_6,
                self.block_6,
                self.rece_6,
                self.rece_pct_6,
                self.error_6,
                4,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_7,
                [
                    self.l_hits_7,
                    self.l_serve_7,
                    self.l_block_7,
                    self.l_rece_7,
                    self.l_error_7,
                ],
                self.hit_7,
                self.hit_pct_7,
                self.serve_7,
                self.block_7,
                self.rece_7,
                self.rece_pct_7,
                self.error_7,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_8,
                [
                    self.l_hits_8,
                    self.l_serve_8,
                    self.l_block_8,
                    self.l_rece_8,
                    self.l_error_8,
                ],
                self.hit_8,
                self.hit_pct_8,
                self.serve_8,
                self.block_8,
                self.rece_8,
                self.rece_pct_8,
                self.error_8,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_9,
                [
                    self.l_hits_9,
                    self.l_serve_9,
                    self.l_block_9,
                    self.l_rece_9,
                    self.l_error_9,
                ],
                self.hit_9,
                self.hit_pct_9,
                self.serve_9,
                self.block_9,
                self.rece_9,
                self.rece_pct_9,
                self.error_9,
                5,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_10,
                [
                    self.l_hits_10,
                    self.l_serve_10,
                    self.l_block_10,
                    self.l_rece_10,
                    self.l_error_10,
                ],
                self.hit_10,
                self.hit_pct_10,
                self.serve_10,
                self.block_10,
                self.rece_10,
                self.rece_pct_10,
                self.error_10,
                7,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_11,
                [
                    self.l_hits_11,
                    self.l_serve_11,
                    self.l_block_11,
                    self.l_rece_11,
                    self.l_error_11,
                ],
                self.hit_11,
                self.hit_pct_11,
                self.serve_11,
                self.block_11,
                self.rece_11,
                self.rece_pct_11,
                self.error_11,
                7,
            )
        )
        self.player_profiles[0].append(
            PlayerProfileInView(
                self.player_name_12,
                [
                    self.l_hits_12,
                    self.l_serve_12,
                    self.l_block_12,
                    self.l_rece_12,
                    self.l_error_12,
                ],
                self.hit_12,
                self.hit_pct_12,
                self.serve_12,
                self.block_12,
                self.rece_12,
                self.rece_pct_12,
                self.error_12,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_13,
                [
                    self.l_hits_13,
                    self.l_serve_13,
                    self.l_block_13,
                    self.l_rece_13,
                    self.l_error_13,
                ],
                self.hit_13,
                self.hit_pct_13,
                self.serve_13,
                self.block_13,
                self.rece_13,
                self.rece_pct_13,
                self.error_13,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_14,
                [
                    self.l_hits_14,
                    self.l_serve_14,
                    self.l_block_14,
                    self.l_rece_14,
                    self.l_error_14,
                ],
                self.hit_14,
                self.hit_pct_14,
                self.serve_14,
                self.block_14,
                self.rece_14,
                self.rece_pct_14,
                self.error_14,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_15,
                [
                    self.l_hits_15,
                    self.l_serve_15,
                    self.l_block_15,
                    self.l_rece_15,
                    self.l_error_15,
                ],
                self.hit_15,
                self.hit_pct_15,
                self.serve_15,
                self.block_15,
                self.rece_15,
                self.rece_pct_15,
                self.error_15,
                3,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_16,
                [
                    self.l_hits_16,
                    self.l_serve_16,
                    self.l_block_16,
                    self.l_rece_16,
                    self.l_error_16,
                ],
                self.hit_16,
                self.hit_pct_16,
                self.serve_16,
                self.block_16,
                self.rece_16,
                self.rece_pct_16,
                self.error_16,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_17,
                [
                    self.l_hits_17,
                    self.l_serve_17,
                    self.l_block_17,
                    self.l_rece_17,
                    self.l_error_17,
                ],
                self.hit_17,
                self.hit_pct_17,
                self.serve_17,
                self.block_17,
                self.rece_17,
                self.rece_pct_17,
                self.error_17,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_18,
                [
                    self.l_hits_18,
                    self.l_serve_18,
                    self.l_block_18,
                    self.l_rece_18,
                    self.l_error_18,
                ],
                self.hit_18,
                self.hit_pct_18,
                self.serve_18,
                self.block_18,
                self.rece_18,
                self.rece_pct_18,
                self.error_18,
                4,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_19,
                [
                    self.l_hits_19,
                    self.l_serve_19,
                    self.l_block_19,
                    self.l_rece_19,
                    self.l_error_19,
                ],
                self.hit_19,
                self.hit_pct_19,
                self.serve_19,
                self.block_19,
                self.rece_19,
                self.rece_pct_19,
                self.error_19,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_20,
                [
                    self.l_hits_20,
                    self.l_serve_20,
                    self.l_block_20,
                    self.l_rece_20,
                    self.l_error_20,
                ],
                self.hit_20,
                self.hit_pct_20,
                self.serve_20,
                self.block_20,
                self.rece_20,
                self.rece_pct_20,
                self.error_20,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_21,
                [
                    self.l_hits_21,
                    self.l_serve_21,
                    self.l_block_21,
                    self.l_rece_21,
                    self.l_error_21,
                ],
                self.hit_21,
                self.hit_pct_21,
                self.serve_21,
                self.block_21,
                self.rece_21,
                self.rece_pct_21,
                self.error_21,
                5,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_22,
                [
                    self.l_hits_22,
                    self.l_serve_22,
                    self.l_block_22,
                    self.l_rece_22,
                    self.l_error_22,
                ],
                self.hit_22,
                self.hit_pct_22,
                self.serve_22,
                self.block_22,
                self.rece_22,
                self.rece_pct_22,
                self.error_22,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_23,
                [
                    self.l_hits_23,
                    self.l_serve_23,
                    self.l_block_23,
                    self.l_rece_23,
                    self.l_error_23,
                ],
                self.hit_23,
                self.hit_pct_23,
                self.serve_23,
                self.block_23,
                self.rece_23,
                self.rece_pct_23,
                self.error_23,
                7,
            )
        )
        self.player_profiles[1].append(
            PlayerProfileInView(
                self.player_name_24,
                [
                    self.l_hits_24,
                    self.l_serve_24,
                    self.l_block_24,
                    self.l_rece_24,
                    self.l_error_24,
                ],
                self.hit_24,
                self.hit_pct_24,
                self.serve_24,
                self.block_24,
                self.rece_24,
                self.rece_pct_24,
                self.error_24,
                7,
            )
        )

    def update_team_view(self, results):
        for team in range(2):
            self.team_profiles[team]["name"].setText(results[team]["team"]["name"])
            self.team_profiles[team]["hit"].display(results[team]["team"]["hit"]["kill"])
            self.team_profiles[team]["serve"].display(results[team]["team"]["serve"]["kill"])
            self.team_profiles[team]["block"].display(results[team]["team"]["block"])
            self.team_profiles[team]["error"].display(results[team]["team"]["error"])

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
                elif not SecondWindow.no_actions_performed(value[1]):
                    candidate_found = True
        return value

    def update_player_views(self, results):
        for team in range(2):
            processed = True
            for player_view in self.player_profiles[team]:
                if processed:
                    candidate_results = self.find_candidate_results_in_team(results[team])
                    processed = False

                if candidate_results and candidate_results[1]["group"] < player_view.max_group:
                    processed = True
                    player_view.update_from_result(candidate_results)
                else:
                    player_view.hide_view()

    def update_view_from_results(self, results):
        self.update_team_view(results)
        self.update_player_views(results)


class ThirdWindow(QtWidgets.QWidget, thridUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def update_timeline(self, totals, delta):
        self.graphicsView.clear()
        self.graphicsView.plot(totals, delta)
        self.graphicsView.showGrid(True, True, 0.8)


class FourthWindow(QtWidgets.QWidget, fourthUI):
    home_scores = []
    guest_scores = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qt_setup()

    def qt_setup(self):
        self.home_scores = [
            self.lcdNumber,
            self.lcdNumber_2,
            self.lcdNumber_3,
            self.lcdNumber_4,
            self.lcdNumber_5,
            self.lcdNumber_6,
            self.lcdNumber_7,
            self.lcdNumber_8,
            self.lcdNumber_9,
            self.lcdNumber_10,
        ]
        self.guest_scores = [
            self.lcdNumber_11,
            self.lcdNumber_12,
            self.lcdNumber_13,
            self.lcdNumber_14,
            self.lcdNumber_15,
            self.lcdNumber_16,
            self.lcdNumber_17,
            self.lcdNumber_18,
            self.lcdNumber_19,
            self.lcdNumber_20,
        ]

    def update_view_from_results(self, results):
        self.label.setText(results["team_details"][0]["name"])
        self.label_2.setText(results["team_details"][1]["name"])
        self.lcdNumber_21.display(results["team_details"][0]["score"])
        self.lcdNumber_22.display(results["team_details"][1]["score"])
        for i in range(len(self.home_scores)):
            self.home_scores[i].hide()
            self.guest_scores[i].hide()
        for i in range(len(results["score"]) - 1):
            self.home_scores[i].show()
            self.guest_scores[i].show()
            if results["score"][i][0] != results["score"][i + 1][0]:
                self.home_scores[i].display(results["score"][i + 1][0])
                self.home_scores[i].setStyleSheet("""QLCDNumber {background-color: green}""")
                self.guest_scores[i].display(" ")
                self.guest_scores[i].setStyleSheet(
                    """QLCDNumber {background-color: rgb(114, 159, 207);}"""
                )
            else:
                self.guest_scores[i].display(results["score"][i + 1][1])
                self.guest_scores[i].setStyleSheet("""QLCDNumber {background-color: green}""")
                self.home_scores[i].display(" ")
                self.home_scores[i].setStyleSheet(
                    """QLCDNumber {background-color: rgb(114, 159, 207);}"""
                )


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()