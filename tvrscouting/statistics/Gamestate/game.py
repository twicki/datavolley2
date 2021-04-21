class Game:
    def __init__(self, game_state=None, meta_info=None):
        self._game_state = game_state
        self._meta_info = meta_info

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

    @property
    def meta_info(self):
        return self._meta_info

    @meta_info.setter
    def meta_info(self, value):
        self._meta_info = value