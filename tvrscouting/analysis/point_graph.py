from PyQt5 import QtWidgets
from tvrscouting.uis.third import Ui_Form as thridUI


class PointGraph(QtWidgets.QWidget, thridUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def update_timeline(self, totals, delta):
        self.graphicsView.clear()
        self.graphicsView.plot(totals, delta)
        self.graphicsView.showGrid(True, True, 0.8)