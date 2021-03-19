import pickle
from tvrscouting.statistics import GameState


class Serializer:
    def __init__(self, gamestate=None):
        super().__init__()
        self.game_state = GameState() if gamestate is None else gamestate

    def serialize(self, filename: str):
        with open(filename, "wb") as picklefile:
            pickle.dump(self.game_state, picklefile)

    def deserialize(self, filename: str):
        with open(filename, "rb") as picklefile:
            self.game_state = pickle.load(picklefile)
        return self.game_state
