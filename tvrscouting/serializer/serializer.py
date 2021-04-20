import os
import pickle

from PyQt5.QtWidgets import QFileDialog

from tvrscouting.statistics.Gamestate.game_state import GameState


class Serializer:
    def __init__(self, parent, gamestate=None):
        super().__init__()
        self.parent = parent
        self.game_state = GameState() if gamestate is None else gamestate

    def serialize(self, filename: str = None):
        if filename is None:
            filename = QFileDialog.getSaveFileName(
                self.parent, "Save File", os.path.expanduser("~")
            )[0]
            if not filename:
                return
        with open(filename, "wb") as picklefile:
            pickle.dump(self.game_state, picklefile)

    def deserialize(self, filename: str = None):
        if filename is None:
            filename = QFileDialog.getOpenFileName(
                self.parent, "Open File", os.path.expanduser("~")
            )[0]
            if not filename:
                return
        with open(filename, "rb") as picklefile:
            self.game_state = pickle.load(picklefile)
        return self.game_state
