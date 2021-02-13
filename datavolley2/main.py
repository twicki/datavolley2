# from statistics import Gamestate
# import statistics.Gamestate as GS
import sys

from PyQt5 import QtWidgets

import datavolley2
from datavolley2.statistics.Gamestate import GameState
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
        self.secondWindow = None

    def increment(self):
        self.value += 1
        if self.secondWindow is not None:
            self.secondWindow.label.setText(str(self.value))
            self.secondWindow.show()

    def update(self):
        pass
        # text = self.lineEdit.text()
        # print(text)

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
