from typing import Optional

from tvrscouting.organization.game_meta_info import GameMetaInfo
from tvrscouting.statistics.Gamestate.game_state import GameState


class Game:
    def __init__(self, game_state=None, meta_info=None):
        self._game_state: Optional[GameState] = game_state
        """The game state of the specific game"""

        self._meta_info: Optional[GameMetaInfo] = meta_info
        """The meta information of the game"""

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value: Optional[GameState]):
        self._game_state = value

    @property
    def meta_info(self):
        return self._meta_info

    @meta_info.setter
    def meta_info(self, value: Optional[GameMetaInfo]):
        self._meta_info = value
