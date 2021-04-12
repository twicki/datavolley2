import sys
import os
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog

import tvrscouting
from tvrscouting.serializer.serializer import Serializer
from tvrscouting.uis.setterAnalysis import Ui_Form
from tvrscouting.analysis.basic_filter_widget import Basic_Filter
import copy

from tvrscouting.statistics import Gameaction

# from tvrscouting.statistics.Actions.SpecialAction import InitializePlayer
from tvrscouting.statistics.Players.players import Team, Player
from tvrscouting.analysis.filters import *

# from tvrscouting.analysis.basic_filter_widget import Basic_Filter


class SetterCallAnalysis:
    def __init__(
        self,
        name_l,
        percentage,
        dia_l,
        dia_per,
        dia_tot,
        middle_1_l,
        middle_1_per,
        middle_1_tot,
        setter_l,
        setter_per,
        setter_tot,
        middle_2_l,
        middle_2_per,
        middle_2_tot,
        middle_3_l,
        middle_3_per,
        middle_3_tot,
        outside_l,
        outside_per,
        outside_tot,
        backrow_l,
        backrow_per,
        backrow_tot,
        containing_widget,
        middle_to_show=1,
        call="K1",
    ):
        super().__init__()
        self.percentage = percentage
        self.name_l = name_l
        self.dia_l = dia_l
        self.dia_per = dia_per
        self.dia_tot = dia_tot
        self.setter_l = setter_l
        self.setter_per = setter_per
        self.setter_tot = setter_tot
        self.outside_l = outside_l
        self.outside_per = outside_per
        self.outside_tot = outside_tot
        self.backrow_l = backrow_l
        self.backrow_per = backrow_per
        self.backrow_tot = backrow_tot
        self.containing_widget = containing_widget
        self.middle_slots = [
            (
                middle_1_l,
                middle_1_per,
                middle_1_tot,
            ),
            (
                middle_2_l,
                middle_2_per,
                middle_2_tot,
            ),
            (
                middle_3_l,
                middle_3_per,
                middle_3_tot,
            ),
        ]
        self.players = [
            (
                dia_l,
                dia_per,
                dia_tot,
            ),
            (
                setter_l,
                setter_per,
                setter_tot,
            ),
            (
                outside_l,
                outside_per,
                outside_tot,
            ),
            (
                backrow_l,
                backrow_per,
                backrow_tot,
            ),
        ]
        self.middle_to_show = middle_to_show
        self.call = call
        self.name_l.setText(call[0])
        self.show_specific_middle_position(middle_to_show)

    def show_specific_middle_position(self, middle):
        for middle_widget in self.middle_slots:
            for slot in middle_widget:
                slot.hide()
        if middle > -1:
            for slot in self.middle_slots[middle]:
                slot.show()

    def show(self):
        for player in self.players:
            for element in player:
                element.show()
        self.show_specific_middle_position(self.middle_to_show)
        self.percentage.show()
        self.name_l.show()
        self.containing_widget.show()

    def hide(self):
        for player in self.players:
            for element in player:
                element.hide()
        self.show_specific_middle_position(-1)
        self.percentage.hide()
        self.name_l.hide()
        self.containing_widget.hide()


class Main(QtWidgets.QWidget, Ui_Form, Basic_Filter):
    sigKeyPress = QtCore.pyqtSignal(object)

    def __init__(self, game_state=None):
        super().__init__()
        Basic_Filter.__init__(self)
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/")
        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
        self.qt_setup()

    def apply_all_filters(self):
        self.shown_ralleis = []
        if self.game_state is None:
            self.load_file()
            if self.game_state is None:
                return
        for rally in self.game_state.rallies:
            if (
                self.check_all_rally_filters(rally)
                and self.check_all_court_filters(rally.court)
                and self.check_all_subaction_filters(rally)
            ):
                self.shown_ralleis.append(rally)

        self.analyze()

    @staticmethod
    def rally_wins_in_k1(rally):
        rece_team = rally.setter_call.team
        for action in rally.actions:
            if isinstance(action, Gameaction):
                current_action = str(action)
                if compare_action_to_string(current_action, str(rece_team) + "@@h#"):
                    return True
                elif compare_action_to_string(current_action, "@@@h"):
                    return False
        return False

    def analyze(self):
        total_calls = 0
        distributions = [
            {
                "F": [0, 0],
                "M": [0, 0],
                "B": [0, 0],
                "P": [0, 0],
                "S": [0, 0],
                "total": 0,
            },
            {
                "F": [0, 0],
                "M": [0, 0],
                "B": [0, 0],
                "P": [0, 0],
                "S": [0, 0],
                "total": 0,
            },
            {
                "F": [0, 0],
                "M": [0, 0],
                "B": [0, 0],
                "P": [0, 0],
                "S": [0, 0],
                "total": 0,
            },
            {
                "F": [0, 0],
                "M": [0, 0],
                "B": [0, 0],
                "P": [0, 0],
                "S": [0, 0],
                "total": 0,
            },
            {
                "F": [0, 0],
                "M": [0, 0],
                "B": [0, 0],
                "P": [0, 0],
                "S": [0, 0],
                "total": 0,
            },
            {
                "F": [0, 0],
                "M": [0, 0],
                "B": [0, 0],
                "P": [0, 0],
                "S": [0, 0],
                "total": 0,
            },
        ]
        for index, call in enumerate(self.calls):
            for rally in self.shown_ralleis:
                if rally.setter_call:
                    if rally.setter_call.combination == call.call[1]:
                        # TODO: check if K1 kill for each of those
                        if rally.setter_call.set_to in ["A", "F", "L"]:
                            distributions[index]["F"][0] += 1
                            distributions[index]["F"][1] += int(rally.wins_in_k1())
                            distributions[index]["total"] += 1
                            total_calls += 1
                        if rally.setter_call.set_to in ["M"]:
                            distributions[index]["M"][0] += 1
                            distributions[index]["M"][1] += int(rally.wins_in_k1())
                            distributions[index]["total"] += 1
                            total_calls += 1
                        if rally.setter_call.set_to in ["D", "B", "R"]:
                            distributions[index]["B"][0] += 1
                            distributions[index]["B"][1] += int(rally.wins_in_k1())
                            distributions[index]["total"] += 1
                            total_calls += 1
                        if rally.setter_call.set_to in ["P"]:
                            distributions[index]["P"][0] += 1
                            distributions[index]["P"][1] += int(rally.wins_in_k1())
                            distributions[index]["total"] += 1
                            total_calls += 1
                        if rally.setter_call.set_to in ["S"]:
                            distributions[index]["S"][0] += 1
                            distributions[index]["S"][1] += int(rally.wins_in_k1())
                            distributions[index]["total"] += 1
                            total_calls += 1

        for index, call in enumerate(self.calls):
            current_distribution = distributions[index]
            if current_distribution["total"] > 0:
                if current_distribution["B"][0] > 0:
                    call.dia_tot.display(current_distribution["B"][0])
                    call.dia_per.display(
                        int(current_distribution["B"][1] / current_distribution["B"][0] * 100)
                    )

                if current_distribution["F"][0] > 0:
                    call.outside_tot.display(current_distribution["F"][0])
                    call.outside_per.display(
                        int(current_distribution["F"][1] / current_distribution["F"][0] * 100)
                    )

                if current_distribution["S"][0] > 0:
                    call.setter_tot.display(current_distribution["S"][0])
                    call.setter_per.display(
                        int(current_distribution["S"][1] / current_distribution["S"][0] * 100)
                    )

                if current_distribution["P"][0] > 0:
                    call.backrow_tot.display(current_distribution["P"][0])
                    call.backrow_per.display(
                        int(current_distribution["P"][1] / current_distribution["P"][0] * 100)
                    )

                if current_distribution["M"][0] > 0:
                    call.middle_slots[call.middle_to_show][2].display(current_distribution["M"][0])
                    call.middle_slots[call.middle_to_show][1].display(
                        int(current_distribution["M"][1] / current_distribution["M"][0] * 100)
                    )

                call.percentage.display(int(current_distribution["total"] / total_calls * 100))
                call.show()
            else:
                call.hide()

    def qt_setup(self):
        self.action_filter_button.hide()
        self.calls = [
            SetterCallAnalysis(
                self.Call_label,
                self.Call_percentage,
                self.Dia_label,
                self.Dia_Kills,
                self.Dia_Total,
                self.Middle1_label,
                self.Middle1_Kills,
                self.Middle1_Total,
                self.Setter_label,
                self.Setter_Kills,
                self.Setter_Total,
                self.Middle2_label,
                self.Middle2_Kills,
                self.Middle2_Total,
                self.Middle3_label,
                self.Middle3_Kills,
                self.Middle3_Total,
                self.Outside_label,
                self.Outside_Kills,
                self.Outside_Total,
                self.Pipe_label,
                self.Pipe_Kills,
                self.Pipe_Total,
                self.widget_1,
                0,
                ("Overload 2", "K1"),
            ),
            SetterCallAnalysis(
                self.Call_label_2,
                self.Call_percentage_2,
                self.Dia_label_2,
                self.Dia_Kills_2,
                self.Dia_Total_2,
                self.Middle1_label_2,
                self.Middle1_Kills_2,
                self.Middle1_Total_2,
                self.Setter_label_2,
                self.Setter_Kills_2,
                self.Setter_Total_2,
                self.Middle2_label_2,
                self.Middle2_Kills_2,
                self.Middle2_Total_2,
                self.Middle3_label_2,
                self.Middle3_Kills_2,
                self.Middle3_Total_2,
                self.Outside_label_2,
                self.Outside_Kills_2,
                self.Outside_Total_2,
                self.Pipe_label_2,
                self.Pipe_Kills_2,
                self.Pipe_Total_2,
                self.widget_2,
                1,
                ("Standard", "K2"),
            ),
            SetterCallAnalysis(
                self.Call_label_3,
                self.Call_percentage_3,
                self.Dia_label_3,
                self.Dia_Kills_3,
                self.Dia_Total_3,
                self.Middle1_label_3,
                self.Middle1_Kills_3,
                self.Middle1_Total_3,
                self.Setter_label_3,
                self.Setter_Kills_3,
                self.Setter_Total_3,
                self.Middle2_label_3,
                self.Middle2_Kills_3,
                self.Middle2_Total_3,
                self.Middle3_label_3,
                self.Middle3_Kills_3,
                self.Middle3_Total_3,
                self.Outside_label_3,
                self.Outside_Kills_3,
                self.Outside_Total_3,
                self.Pipe_label_3,
                self.Pipe_Kills_3,
                self.Pipe_Total_3,
                self.widget_3,
                2,
                ("Overload 4", "K3"),
            ),
            SetterCallAnalysis(
                self.Call_label_4,
                self.Call_percentage_4,
                self.Dia_label_4,
                self.Dia_Kills_4,
                self.Dia_Total_4,
                self.Middle1_label_4,
                self.Middle1_Kills_4,
                self.Middle1_Total_4,
                self.Setter_label_4,
                self.Setter_Kills_4,
                self.Setter_Total_4,
                self.Middle2_label_4,
                self.Middle2_Kills_4,
                self.Middle2_Total_4,
                self.Middle3_label_4,
                self.Middle3_Kills_4,
                self.Middle3_Total_4,
                self.Outside_label_4,
                self.Outside_Kills_4,
                self.Outside_Total_4,
                self.Pipe_label_4,
                self.Pipe_Kills_4,
                self.Pipe_Total_4,
                self.widget_4,
                -1,
                ("No Middle", "K4"),
            ),
            SetterCallAnalysis(
                self.Call_label_5,
                self.Call_percentage_5,
                self.Dia_label_5,
                self.Dia_Kills_5,
                self.Dia_Total_5,
                self.Middle1_label_5,
                self.Middle1_Kills_5,
                self.Middle1_Total_5,
                self.Setter_label_5,
                self.Setter_Kills_5,
                self.Setter_Total_5,
                self.Middle2_label_5,
                self.Middle2_Kills_5,
                self.Middle2_Total_5,
                self.Middle3_label_5,
                self.Middle3_Kills_5,
                self.Middle3_Total_5,
                self.Outside_label_5,
                self.Outside_Kills_5,
                self.Outside_Total_5,
                self.Pipe_label_5,
                self.Pipe_Kills_5,
                self.Pipe_Total_5,
                self.widget_5,
                -1,
                ("?", "K5"),
            ),
            SetterCallAnalysis(
                self.Call_label_6,
                self.Call_percentage_6,
                self.Dia_label_6,
                self.Dia_Kills_6,
                self.Dia_Total_6,
                self.Middle1_label_6,
                self.Middle1_Kills_6,
                self.Middle1_Total_6,
                self.Setter_label_6,
                self.Setter_Kills_6,
                self.Setter_Total_6,
                self.Middle2_label_6,
                self.Middle2_Kills_6,
                self.Middle2_Total_6,
                self.Middle3_label_6,
                self.Middle3_Kills_6,
                self.Middle3_Total_6,
                self.Outside_label_6,
                self.Outside_Kills_6,
                self.Outside_Total_6,
                self.Pipe_label_6,
                self.Pipe_Kills_6,
                self.Pipe_Total_6,
                self.widget_6,
            ),
        ]
        self.calls[-1].hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())