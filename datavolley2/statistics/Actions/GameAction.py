from enum import Enum
from .AbstractAction import AbstractAction
import datavolley2.statistics.Gamestate.game_state as gs


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
            return Quality.Good
        elif quality == Quality.Error:
            return Quality.Good


class Action(Enum):
    Setting = (1, "e")
    Hit = (2, "h")
    Block = (3, "b")
    Serve = (4, "s")
    Reception = (5, "r")
    Defense = (6, "d")

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


class Gameaction(AbstractAction):
    team = None
    player = None
    action = None
    quality = None

    def __init__(self, time_stamp=None):
        super().__init__(time_stamp)
        self.team = Team.Home
        self.player = 0
        self.action = Action.Hit
        self.quality = Quality.Good

    def __str__(self):
        return gs.expandString(
            str(self.team) + str(self.player) + str(self.action) + str(self.quality)
        )[0]

    @classmethod
    def from_string(cls, s, time_stamp=None):
        new = cls(time_stamp)
        new.team = Team.from_string(s[0])
        new.player = int(s[1:3])
        new.action = Action.from_string(s[3])
        new.quality = Quality.from_string(s[4])
        return new


def is_scoring(action):
    if action.quality == Quality.Kill:
        return action.team, True
    elif action.quality == Quality.Error:
        return Team.inverse(action.team), True
    else:
        return None, False