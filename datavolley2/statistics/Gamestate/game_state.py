import copy
import enum
from copy import deepcopy

import datavolley2.statistics.Actions as actions

from datavolley2.statistics.Actions.GameAction import (
    Gameaction,
    is_scoring,
    Action,
    Quality,
)
import datavolley2.statistics.Actions.SpecialAction as SpecialActions


class Player:
    @enum.unique
    class PlayerPosition(enum.Enum):
        Setter = "Setter"
        Libera = "Libera"
        Outside = "Outside"
        Opposite = "Opposite"
        Middle = "Middle"
        Universal = "Universal"

    Position = PlayerPosition.Universal
    Number = 0

    def __init__(self, number: int, position=PlayerPosition.Universal) -> None:
        self.Number = number
        self.Position = position


class Field:
    def __init__(self) -> None:
        self.players = list()
        for i in range(6):
            self.players.append(Player(0))


class Court:
    fields = []

    def __init__(self) -> None:
        f1 = Field()
        self.fields.append(f1)
        f2 = Field()
        self.fields.append(f2)

    def rotate(self, who: int) -> None:
        self.fields[who].players.append(self.fields[who].players.pop(0))
        #  = np.roll(self.fields[who].players, -1)


def expandString(input):
    return input


def split_string(input):
    strings = input.split(".")
    if len(strings) > 1:
        s1 = expandString(strings[0])
        s2 = expandString(strings[1])
    else:
        s1 = expandString(strings[0])
        s2 = None
    return s1, s2


class GameState:
    score = [0, 0]
    set_score = [0, 0]
    # timeouts = [0, 0]
    rallies = []
    court = Court()

    _current_actions = []
    _last_serve = None
    teamnames = [None, None]

    def __init__(self) -> None:
        pass

    def add_string(self, action: str):
        if "sub" in action:
            l = action.split()
            number = int(l[1])
            position = int(l[2])
            team = l[0][0]
            action = SpecialActions.Substitute(
                actions.Team.from_string(team), number, position
            )
            self.add_logical(action)
        elif "serve" in action:
            team = action[0][0]
            action = SpecialActions.SetServingTeam(actions.Team.from_string(team))
            self.add_logical(action)
        elif "point" in action:
            l = action.split()
            number = int(l[1])
            team = l[0][0]
            action = SpecialActions.SetServingTeam(actions.Team.from_string(team))
            self.add_logical(action)
        elif "endset" in action:
            team = action[0][0]
            action = SpecialActions.Endset(actions.Team.from_string(team))
            self.add_logical(action)
        elif "rota" in action:
            team = action[0][0]
            action = SpecialActions.Endset(actions.Team.from_string(team))
            self.add_logical(action)
        elif "team" in action:
            l = action.split()
            team = l[0][0]
            teamname = l[1]
            self.teamnames[int(actions.Team.from_string(team))] = teamname
        else:
            str1, str2 = split_string(action)
            # str1, str2 = actions.GameAction.splitstring(action)
            allactions = []
            allactions.append(copy.copy(Gameaction.from_string(str1)))
            if str2:
                allactions.append(copy.copy(Gameaction.from_string(str1)))
            for thisaction in allactions:
                self.add_logical(thisaction)

    def add_logical(self, action):
        self._current_actions.append(action)
        if isinstance(action, SpecialActions.Substitute):
            who = action.team_
            field = self.court.fields[int(who)].players
            pos = action.position_in - 1
            fpos = field[:pos]
            fpos.append(Player(action.player_in))
            self.court.fields[int(who)].players = fpos + field[pos + 1 :]
            self.flush_actions()
        elif isinstance(action, SpecialActions.Endset):
            self.score[0] = 0
            self.score[1] = 0
            self.flush_actions()
        elif isinstance(action, SpecialActions.Rotation):
            self.court.rotate(int(action.team_))
            self.flush_actions()
        elif isinstance(action, SpecialActions.SetServingTeam):
            self._last_serve = action.team_
            self.flush_actions()
        elif isinstance(action, SpecialActions.Point):
            self.score[int(action.team_)] += action.value
            self.flush_actions()
        else:
            print(isinstance(action, Gameaction))
            who, was_score = is_scoring(action)
            if was_score:
                index = int(who)
                self._current_actions.append(actions.Point(who))

                # flush the current action before housekeeping
                self.flush_actions()

                # housekeeping: serve
                if who is not self._last_serve:
                    self._current_actions.append(actions.Rotation(who))
                    self.court.rotate(index)
                self._last_serve = who

                # housekeeping: scoring
                opponent = int(actions.Team.inverse(who))
                self.score[index] += 1
                if (
                    self.score[index] >= self.max_points_in_set()
                    and score[index] - 2 > self.score[opponent]
                ):
                    self._current_actions.append(actions.Endset(who))
                    self.flush_actions()
                    self.set_score[index] += 1
                    self.score[index] = 0
                    self.score[opponent] = 0

    def flush_actions(self):
        self.rallies.append(
            (
                list.copy(self._current_actions),
                copy.deepcopy(self.court),
                copy.deepcopy(self.score),
                copy.deepcopy(self.set_score),
            )
        )
        self._current_actions.clear()

    def add_plain(self, action):
        pass

    def max_points_in_set(self):
        if self.set_score[0] + self.set_score[1] < 4:
            return 25
        else:
            return 15

    def collect_stats(self, team):
        playerstats = {}
        for player in self.court.fields[int(team)].players:
            playerstats[player.Number] = {}
            playerstats[player.Number]["serve"] = {}
            playerstats[player.Number]["serve"]["kill"] = 0
            playerstats[player.Number]["serve"]["ball"] = 0
            playerstats[player.Number]["reception"] = 0
            playerstats[player.Number]["hit"] = {}
            playerstats[player.Number]["hit"]["kill"] = 0
            playerstats[player.Number]["hit"]["ball"] = 0
            playerstats[player.Number]["error"] = 0
            playerstats[player.Number]["block"] = 0

        for player in self.court.fields[int(team)].players:
            for rally in self.rallies:
                for action in rally[0]:
                    if isinstance(action, Gameaction):
                        # is is the right player on the right team
                        if action.team == actions.Team.Home:
                            if action.player == player.Number:
                                # serve statistics
                                if action.action == Action.Serve:
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["serve"]["kill"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1
                                    else:
                                        playerstats[player.Number]["serve"]["ball"] += 1

                                # hitting statistics
                                if action.action == Action.Hit:
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["hit"]["kill"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1
                                    else:
                                        playerstats[player.Number]["hit"]["ball"] += 1

                                # blocking statistics
                                if action.action == Action.Block:
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["block"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

                                # blocking statistics
                                if action.action == Action.Reception:
                                    playerstats[player.Number]["reception"] += 1
                                    if action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1
        return playerstats