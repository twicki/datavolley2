from PyQt5 import QtWidgets

from tvrscouting.uis.fourth import Ui_Form as fourthUI


class RecentScores(QtWidgets.QWidget, fourthUI):
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
