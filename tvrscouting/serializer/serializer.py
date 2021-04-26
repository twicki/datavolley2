import os
import pickle

from PyQt5.QtWidgets import QFileDialog
from typing import Optional
from tvrscouting.statistics.Gamestate.game import Game


class Serializer:
    def __init__(self, parent, game=None):
        super().__init__()
        self.parent = parent
        self.game = Game() if game is None else game

    def serialize(self, filename: Optional[str] = None):
        if filename is None:
            filename = QFileDialog.getSaveFileName(
                self.parent, "Save File", os.path.expanduser("~")
            )[0]
            if not filename:
                return
        with open(filename, "wb") as picklefile:
            pickle.dump(self.game, picklefile)

    def deserialize(self, filename: Optional[str] = None) -> Game:
        if filename is None:
            filename = QFileDialog.getOpenFileName(
                self.parent, "Open File", os.path.expanduser("~")
            )[0]
            if not filename:
                return
        with open(filename, "rb") as picklefile:
            self.game = pickle.load(picklefile)
        return self.game
