import os
import pickle
import socket
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTimer

from tvrscouting.analysis.playerview import TeamViews
from tvrscouting.uis.fourth import Ui_Form as fourthUI
from tvrscouting.uis.remote_comm import Ui_MainWindow
from tvrscouting.uis.third import Ui_Form as thridUI


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
        self.update_player_stats()
        self.update_timeline()
        self.update_recent_scores_view()

    def update_player_stats(self):
        if self.secondWindow is not None:
            self.secondWindow.update_view_from_results(self.data["results"])

    def update_timeline(self):
        if self.ThirdWindow:
            self.ThirdWindow.update_timeline(self.data["timeline"][0], self.data["timeline"][1])

    def update_recent_scores_view(self):
        if self.FourthWindow:
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
            self.secondWindow = TeamViews()
        self.secondWindow.show()
        if self.ThirdWindow is None:
            self.ThirdWindow = ThirdWindow()
        self.ThirdWindow.show()
        if self.FourthWindow is None:
            self.FourthWindow = FourthWindow()
        self.FourthWindow.show()


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
