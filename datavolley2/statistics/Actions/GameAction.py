from enum import Enum


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


class Fingers(Enum):
    THUMB = (1, "thumb")
    INDEX = (2, "index")
    MIDDLE = (3, "middle")
    RING = (4, "ring")
    PINKY = (5, "pinky")

    def __str__(self):
        return self.value[1]


# class Team:
#     def __init__(self):
#         pass


class GameAction:
    def __init__(self):
        pass