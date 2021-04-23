from typing import List

from tvrscouting.statistics.Players.players import Player


class TeamInfo:
    def __init__(
        self,
    ):
        super().__init__()
        self.name: str = ""
        self.head_coach: str = ""
        self.assistant_coach: str = ""
        self.players: List[Player] = []

    def to_string(self, starting_char: str) -> str:
        retval = starting_char + "team" + "!" + self.name + "\n"
        for player in self.players:
            retval += (
                starting_char
                + "player"
                + "!"
                + str(player.Number)
                + "!"
                + player.Name.split()[-1]
                + "!"
                + str(player.Position)
            )
            if player.is_capitain:
                retval += "!C"
            retval += "\n"
        return retval
