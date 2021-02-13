# from statistics import Gamestate
# import statistics.Gamestate as GS
import sys

from PyQt5 import QtWidgets

import datavolley2
from datavolley2.statistics import GameState

# from datavolley2.statistics.Gamestate import GameState
from uis import Ui_Form, Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_stats)
        self.pushButton_2.clicked.connect(self.increment)
        self.lineEdit.returnPressed.connect(self.update)
        self.game_state = GameState()
        self.value = 0
        self.stats = [None, None]
        self.fullstring = ""
        self.secondWindow = None

    def increment(self):
        self.value += 1
        if self.secondWindow is not None:
            self.secondWindow.label.setText(str(self.value))
            self.secondWindow.show()

    def update(self):
        text = self.lineEdit.text()
        self.fullstring = self.fullstring + text + "\n"
        s = text.split(" ")
        for command in s:
            self.game_state.add_string(command)
        self.textEdit.setText(self.fullstring)

        ## update my view:
        self.lineEdit.clear()
        self.label_14.setText(self.game_state.teamnames[0])
        self.label_13.setText(self.game_state.teamnames[1])

        number = self.game_state.court.fields[0].players[0].Number
        fulltext = str(number) 
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[0][number]
        self.label.setText(fulltext)

        number = self.game_state.court.fields[0].players[1].Number
        fulltext = str(number) 
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_5.setText(fulltext)

        number = self.game_state.court.fields[0].players[2].Number
        fulltext = str(number) 
        if number in self.game_state.player_names[0]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_4.setText(fulltext)

        number = self.game_state.court.fields[0].players[3].Number
        fulltext = str(number) 
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_6.setText(fulltext)

        number = self.game_state.court.fields[0].players[4].Number
        fulltext = str(number) 
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_3.setText(fulltext)

        number = self.game_state.court.fields[0].players[5].Number
        fulltext = str(number) 
        if number in self.game_state.player_names[1]:
            fulltext = fulltext + " " + self.game_state.player_names[1][number]
        self.label_2.setText(fulltext)
        

    def print_stats(self):
        if self.secondWindow is None:
            self.secondWindow = SecondWindow()
            s = SecondWindow()
        self.secondWindow.show()


class SecondWindow(QtWidgets.QWidget, Ui_Form):
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
