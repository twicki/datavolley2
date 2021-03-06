from enum import Enum
from typing import List

from tvrscouting.statistics.Players.players import Team
from tvrscouting.utils.errors import TVRSyntaxError

from .AbstractAction import AbstractAction


class Quality(Enum):

    Perfect = (0, "p")
    Kill = (1, "#")
    Good = (2, "+")
    Bad = (3, "-")
    Over = (4, "o")
    Error = (5, "=")

    @classmethod
    def from_string(cls, s):
        for quality in cls:
            if quality.value[1] == s:
                return quality

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]

    @staticmethod
    def inverse(quality):
        if quality == Quality.Kill:
            return Quality.Over
        elif quality == Quality.Perfect:
            return Quality.Bad
        elif quality == Quality.Good:
            return Quality.Bad
        elif quality == Quality.Bad:
            return Quality.Good
        elif quality == Quality.Over:
            return Quality.Kill
        elif quality == Quality.Error:
            return Quality.Good


class Action(Enum):
    Set = (1, "e")
    Hit = (2, "h")
    Block = (3, "b")
    Serve = (4, "s")
    Reception = (5, "r")
    Defense = (6, "d")
    Freeball = (7, "f")

    @classmethod
    def from_string(cls, s):
        for quality in cls:
            if quality.value[1] == s:
                return quality

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]

    @staticmethod
    def inverse(action):
        if action == Action.Serve:
            return Action.Reception
        elif action == Action.Reception:
            return Action.Serve

        elif action == Action.Hit:
            return Action.Block
        elif action == Action.Block:
            return Action.Hit
        elif action == Action.Defense:
            return Action.Hit


class Combination(Enum):
    Default = (0, "D0")
    Fast_1 = (1, "X1")
    Fast_2 = (1, "X2")
    Fast_3 = (1, "X3")
    Medium_1 = (1, "C1")
    Medium_2 = (1, "C2")
    Medium_3 = (1, "C3")
    Medium_4 = (1, "C4")
    Medium_5 = (1, "C5")
    Medium_6 = (1, "C6")
    High_1 = (1, "V1")
    High_2 = (1, "V2")
    High_3 = (1, "V3")
    High_4 = (1, "V4")
    High_5 = (1, "V5")
    High_6 = (1, "V6")

    @classmethod
    def from_string(cls, s):
        for combination in cls:
            if combination.value[1] == s:
                return combination

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]


class SetterCall(AbstractAction):
    def __init__(self, time_stamp=None):
        super().__init__(time_stamp)
        self.team = Team.Home
        self.combination = "K1"
        self.set_to = "A"  # oneof [F,C,B,P,S] // here [A,M,D,P,S]

    def __str__(self):
        return str(self.team) + str(self.combination) + str(self.set_to)

    @classmethod
    def from_string(cls, s, time_stamp=None):
        new = cls(time_stamp)
        if s[0] in ["*", "/"]:
            new.team = Team.from_string(s[0])
            new.combination = s[1:3]
            if len(s) > 3:
                new.set_to = s[3]
        else:
            new.team = None
            new.combination = s[0:2]
            if len(s) > 2:
                new.set_to = s[2]
        return new


class Gameaction(AbstractAction):
    def __init__(self, time_stamp=None):
        super().__init__(time_stamp)
        self.team: Team = Team.Home
        self.player: int = 0
        self.action: Action = Action.Hit
        self.quality: Quality = Quality.Good
        self.combination: Combination = Combination.Default
        self.direction: List[int] = [0, 0]
        self.action_type: str = "D"
        self.action_players_involved: int = 9
        self.action_error_type: str = "D"
        self.direction_type: str = "c"

    def __str__(self):
        return (
            str(self.team)
            + "%02d" % self.player
            + str(self.action)
            + str(self.quality)
            + str(self.combination)
            + str(self.direction[0])
            + str(self.direction[1])
            + ";"
            + str(self.action_type)
            + str(self.action_players_involved)
            + str(self.action_error_type)
            + str(self.direction_type)
        )

    @classmethod
    def from_string(cls, s, time_stamp=None):
        new = cls(time_stamp)
        new.team = Team.from_string(s[0])
        new.player = int(s[1:3])
        if Action.from_string(s[3]):
            new.action = Action.from_string(s[3])
        else:
            raise TVRSyntaxError()
        if Quality.from_string(s[4]):
            new.quality = Quality.from_string(s[4])
        else:
            raise TVRSyntaxError()
        if Combination.from_string(s[5:7]):
            new.combination = Combination.from_string(s[5:7])
        else:
            raise TVRSyntaxError()
        new.direction[0] = str(s[7])
        new.direction[1] = str(s[8])
        new.action_type = s[10]
        new.action_players_involved = int(s[11])
        new.action_error_type = s[12]
        new.direction_type = s[13]
        return new


def is_scoring(action: Gameaction):
    if action.quality == Quality.Kill:
        return action.team, True
    elif action.quality == Quality.Error:
        return Team.inverse(action.team), True
    else:
        return None, False
