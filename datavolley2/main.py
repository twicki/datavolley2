# from statistics import Gamestate
# import statistics.Gamestate as GS
import sys

from PyQt5 import QtWidgets

import datavolley2
from datavolley2.statistics import GameState

import matplotlib as mp
import numpy as np

# from datavolley2.statistics.Gamestate import GameState
from uis import Ui_Form, Ui_MainWindow
from uis.third import Ui_Form as thridUI


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_stats)
        self.pushButton_2.clicked.connect(self.save_and_reset)
        self.lineEdit.returnPressed.connect(self.update)
        self.game_state = GameState()
        self.fullstring = ""
        self.secondWindow = None
        self.ThirdWindow = None
        self.illegal = []

    def save_and_reset(self):
        userdata = self.textEdit.toPlainText()
        s = userdata.split()
        self.game_state = GameState()
        self.fullstring = userdata
        self.illegal.clear()

        for command in s:
            try:
                self.game_state.add_string(command)
            except:
                self.illegal.append(command)
        self.textEdit.setText(self.fullstring)
        self.lineEdit.clear()
        self.update()

    def update(self):
        text = self.lineEdit.text()
        self.fullstring = self.fullstring + text + "\n"
        s = text.split(" ")
        for command in s:
            try:
                self.game_state.add_string(command)
            except:
                self.illegal.append(command)

        self.textEdit.setText(self.fullstring)
        # self.textEdit.verticalScrollBar.setValue(
        #     self.textEdit.verticalScrollBar.maximum()
        # )

        ## update my view:
        self.lineEdit.clear()
        self.label_14.setText(self.game_state.teamnames[0])
        self.label_13.setText(self.game_state.teamnames[1])

        # home team
        number = self.game_state.court.fields[0].players[0].Number
        fulltext = str(number)
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[0][number]
        self.label.setText(fulltext)

        number = self.game_state.court.fields[0].players[1].Number
        fulltext = str(number)
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[0][number]
        self.label_5.setText(fulltext)

        number = self.game_state.court.fields[0].players[2].Number
        fulltext = str(number)
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[0][number]
        self.label_4.setText(fulltext)

        number = self.game_state.court.fields[0].players[3].Number
        fulltext = str(number)
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[0][number]
        self.label_6.setText(fulltext)

        number = self.game_state.court.fields[0].players[4].Number
        fulltext = str(number)
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[0][number]
        self.label_3.setText(fulltext)

        number = self.game_state.court.fields[0].players[5].Number
        fulltext = str(number)
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[0][number]
        self.label_2.setText(fulltext)

        # away team team
        number = self.game_state.court.fields[1].players[0].Number
        fulltext = str(number)
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_12.setText(fulltext)

        number = self.game_state.court.fields[1].players[1].Number
        fulltext = str(number)
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_8.setText(fulltext)

        number = self.game_state.court.fields[1].players[2].Number
        fulltext = str(number)
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_7.setText(fulltext)

        number = self.game_state.court.fields[1].players[3].Number
        fulltext = str(number)
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_9.setText(fulltext)

        number = self.game_state.court.fields[1].players[4].Number
        fulltext = str(number)
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_11.setText(fulltext)

        number = self.game_state.court.fields[1].players[5].Number
        fulltext = str(number)
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_10.setText(fulltext)

        ## set up score
        self.lcdNumber.display(self.game_state.score[0])
        self.lcdNumber_2.display(self.game_state.score[1])

        ## update the other view:
        if self.secondWindow is not None:
            ## team 1
            self.secondWindow.label_62.setText(self.game_state.teamnames[0])
            results = self.game_state.collect_stats("*")
            self.secondWindow.lcdNumber_61.display(results["team"]["hit"]["kill"])
            self.secondWindow.lcdNumber_62.display(results["team"]["serve"]["kill"])
            self.secondWindow.lcdNumber_63.display(results["team"]["block"])
            self.secondWindow.lcdNumber_64.display(results["team"]["error"])
            # p1 home
            number = self.game_state.court.fields[0].players[0].Number
            fulltext = str(number)
            if number in self.game_state.player_names[0]:
                fulltext = fulltext + " " + self.game_state.player_names[0][number]
            self.secondWindow.label.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_2.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_3.display(results[number]["block"])
                self.secondWindow.lcdNumber_6.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_5.display(ratio)

            # p2 home
            number = self.game_state.court.fields[0].players[1].Number
            fulltext = str(number)
            if number in self.game_state.player_names[0]:
                fulltext = fulltext + " " + self.game_state.player_names[0][number]
            self.secondWindow.label_22.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_23.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_25.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_22.display(results[number]["block"])
                self.secondWindow.lcdNumber_21.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_24.display(ratio)

            # p3 home
            number = self.game_state.court.fields[0].players[2].Number
            fulltext = str(number)
            if number in self.game_state.player_names[0]:
                fulltext = fulltext + " " + self.game_state.player_names[0][number]
            self.secondWindow.label_20.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_17.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_16.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_20.display(results[number]["block"])
                self.secondWindow.lcdNumber_19.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_18.display(ratio)

            # p4 home
            number = self.game_state.court.fields[0].players[3].Number
            fulltext = str(number)
            if number in self.game_state.player_names[0]:
                fulltext = fulltext + " " + self.game_state.player_names[0][number]
            self.secondWindow.label_28.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_28.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_30.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_27.display(results[number]["block"])
                self.secondWindow.lcdNumber_26.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_29.display(ratio)

            # p5 home
            number = self.game_state.court.fields[0].players[4].Number
            fulltext = str(number)
            if number in self.game_state.player_names[0]:
                fulltext = fulltext + " " + self.game_state.player_names[0][number]
            self.secondWindow.label_15.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_12.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_11.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_15.display(results[number]["block"])
                self.secondWindow.lcdNumber_14.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_13.display(ratio)

            # p6 home
            number = self.game_state.court.fields[0].players[5].Number
            fulltext = str(number)
            if number in self.game_state.player_names[0]:
                fulltext = fulltext + " " + self.game_state.player_names[0][number]
            self.secondWindow.label_8.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_8.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_10.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_4.display(results[number]["block"])
                self.secondWindow.lcdNumber_9.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_7.display(ratio)

            # lib home
            # number = self.game_state.libs[0]
            # fulltext = str(number)
            # if number in self.game_state.player_names[0]:
            #     fulltext = fulltext + " " + self.game_state.player_names[0][number]
            # self.secondWindow.label_71.setText(fulltext)
            # if number in results:
            #     self.secondWindow.lcdNumber_8.display(results[number]["hit"]["kill"])
            #     self.secondWindow.lcdNumber_10.display(results[number]["serve"]["kill"])
            #     self.secondWindow.lcdNumber_4.display(results[number]["block"])
            #     self.secondWindow.lcdNumber_9.display(results[number]["error"])
            #     if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
            #         ratio = int(
            #             results[number]["hit"]["kill"]
            #             / (
            #                 results[number]["hit"]["kill"]
            #                 + results[number]["hit"]["ball"]
            #             )
            #             * 100
            #         )
            #     else:
            #         ratio = 0
            #     self.secondWindow.lcdNumber_7.display(ratio)
            ## team 2
            results = self.game_state.collect_stats("/")
            self.secondWindow.label_61.setText(self.game_state.teamnames[1])
            self.secondWindow.lcdNumber_67.display(results["team"]["hit"]["kill"])
            self.secondWindow.lcdNumber_68.display(results["team"]["serve"]["kill"])
            self.secondWindow.lcdNumber_65.display(results["team"]["block"])
            self.secondWindow.lcdNumber_66.display(results["team"]["error"])
            # p1 away
            number = self.game_state.court.fields[1].players[0].Number
            fulltext = str(number)
            if number in self.game_state.player_names[1]:
                fulltext = fulltext + " " + self.game_state.player_names[1][number]
            self.secondWindow.label_46.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_37.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_45.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_49.display(results[number]["block"])
                self.secondWindow.lcdNumber_47.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_50.display(ratio)

            # p2 away
            number = self.game_state.court.fields[1].players[1].Number
            fulltext = str(number)
            if number in self.game_state.player_names[1]:
                fulltext = fulltext + " " + self.game_state.player_names[1][number]
            self.secondWindow.label_45.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_44.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_48.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_32.display(results[number]["block"])
                self.secondWindow.lcdNumber_31.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_57.display(ratio)

            # p3 away
            number = self.game_state.court.fields[1].players[2].Number
            fulltext = str(number)
            if number in self.game_state.player_names[1]:
                fulltext = fulltext + " " + self.game_state.player_names[1][number]
            self.secondWindow.label_50.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_34.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_41.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_38.display(results[number]["block"])
                self.secondWindow.lcdNumber_56.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_46.display(ratio)

            # p4 away
            number = self.game_state.court.fields[1].players[3].Number
            fulltext = str(number)
            if number in self.game_state.player_names[1]:
                fulltext = fulltext + " " + self.game_state.player_names[1][number]
            self.secondWindow.label_60.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_51.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_33.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_58.display(results[number]["block"])
                self.secondWindow.lcdNumber_59.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_55.display(ratio)

            # p5 away
            number = self.game_state.court.fields[1].players[4].Number
            fulltext = str(number)
            if number in self.game_state.player_names[1]:
                fulltext = fulltext + " " + self.game_state.player_names[1][number]
            self.secondWindow.label_59.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_60.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_53.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_43.display(results[number]["block"])
                self.secondWindow.lcdNumber_52.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_36.display(ratio)

            # p6 away
            number = self.game_state.court.fields[1].players[5].Number
            fulltext = str(number)
            if number in self.game_state.player_names[1]:
                fulltext = fulltext + " " + self.game_state.player_names[1][number]
            self.secondWindow.label_57.setText(fulltext)
            if number in results:
                self.secondWindow.lcdNumber_39.display(results[number]["hit"]["kill"])
                self.secondWindow.lcdNumber_40.display(results[number]["serve"]["kill"])
                self.secondWindow.lcdNumber_35.display(results[number]["block"])
                self.secondWindow.lcdNumber_42.display(results[number]["error"])
                if results[number]["hit"]["kill"] + results[number]["hit"]["ball"] > 0:
                    ratio = int(
                        results[number]["hit"]["kill"]
                        / (
                            results[number]["hit"]["kill"]
                            + results[number]["hit"]["ball"]
                        )
                        * 100
                    )
                else:
                    ratio = 0
                self.secondWindow.lcdNumber_54.display(ratio)

        if self.ThirdWindow:
            totals, delta = self.game_state.return_timeline()
            self.ThirdWindow.graphicsView.clear()
            self.ThirdWindow.graphicsView.plot(totals, delta)
        # hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        # self.ThirdWindow.graphicsView.plot(hour, temperature)

    def print_stats(self):
        if self.secondWindow is None:
            self.secondWindow = SecondWindow()
            s = SecondWindow()
        self.secondWindow.show()
        if self.ThirdWindow is None:
            self.ThirdWindow = ThirdWindow()
        self.ThirdWindow.show()


class SecondWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ThirdWindow(QtWidgets.QWidget, thridUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
