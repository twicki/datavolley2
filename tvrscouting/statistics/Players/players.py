from enum import Enum, unique


class Team(Enum):

    Home = (0, "*")
    Away = (1, "/")

    @classmethod
    def from_string(cls, s):
        for team in cls:
            if team.value[1] == s:
                return team

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]

    @staticmethod
    def inverse(team):
        if team == Team.Home:
            return Team.Away
        else:
            return Team.Home


class Player:
    @unique
    class PlayerPosition(Enum):
        Setter = ("Setter", "s", 1)
        Opposite = ("Opposite", "d", 2)
        Middle = ("Middle", "m", 3)
        Outside = ("Outside", "o", 4)
        Libera = ("Libera", "l", 5)
        Universal = ("Universal", "u", 6)

        def __lt__(self, other):
            if self.__class__ is other.__class__:
                return self.value[2] < other.value[2]
            else:
                return False
            # return NotImplemented

        def __int__(self):
            return self.value[2]

        def __str__(self):
            return self.value[1]

        @classmethod
        def from_string(cls, s):
            for position in cls:
                if position.value[1] == s:
                    return position

    Position = PlayerPosition.Universal
    Number = 0
    Name = ""
    is_capitain = False

    def __init__(
        self,
        number: int,
        position: PlayerPosition = PlayerPosition.Universal,
        name: str = "",
        is_capitain: bool = False,
    ) -> None:

        self.Number = number
        self.Position = position
        self.Name = name
        self.is_capitain = is_capitain
