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


def set_team(user_string, returnvalue):
    if user_string[0] == "/":
        returnvalue = user_string[0] + returnvalue[1:]
        user_string = user_string[1:]
        return returnvalue, user_string, True
    elif user_string[0] == "*":
        returnvalue = user_string[0] + returnvalue[1:]
        user_string = user_string[1:]
        return returnvalue, user_string, True
    else:
        return returnvalue, user_string, False


def set_number(user_string, returnvalue):
    if len(user_string) > 1 and user_string[1].isnumeric():
        number = int(user_string[0:2])
        returnvalue = returnvalue[0] + str(user_string[0:2]) + returnvalue[3:]
        user_string = user_string[2:]
    else:
        returnvalue = returnvalue[0] + "0" + str(user_string[0]) + returnvalue[3:]
        user_string = user_string[1:]
    return returnvalue, user_string


def set_action(user_string, returnvalue):
    if len(user_string):
        if user_string[0] in ["e", "h", "b", "s", "r", "d"]:
            returnvalue = returnvalue[:3] + user_string[0] + returnvalue[4:]
            user_string = user_string[1:]
            return returnvalue, user_string, True

    return returnvalue, user_string, False


def set_quality(user_string, returnvalue):
    if len(user_string):
        returnvalue = returnvalue[:4] + user_string[0]
        return returnvalue, True
    return returnvalue, False


def expandString(user_string):
    returnvalue = "*00h+"
    returnvalue, user_string, team_set = set_team(user_string, returnvalue)
    returnvalue, user_string = set_number(user_string, returnvalue)
    returnvalue, user_string, action_set = set_action(user_string, returnvalue)
    returnvalue, quality_set = set_quality(user_string, returnvalue)

    return returnvalue, team_set, action_set, quality_set


def correct_strings(s1, team, action, quality, s2, team2, action2, quality2):
    ## correct the teams
    if not team2:
        s2 = str(actions.Team.inverse(actions.Team.from_string(s1[0]))) + s2[1:]
    if not team and team2:
        s1 = str(actions.Team.inverse(actions.Team.from_string(s2[0]))) + s1[1:]

    ## correct the action:
    if not action2:
        s2 = (
            s2[:3]
            + str(actions.Action.inverse(actions.Action.from_string(s1[3])))
            + s2[4:]
        )
    if not action and action2:
        s1 = (
            s1[:3]
            + str(actions.Action.inverse(actions.Action.from_string(s2[3])))
            + s1[4:]
        )

    ## correct the quality
    if not quality2:
        s2 = s2[:4] + str(actions.Quality.inverse(actions.Quality.from_string(s1[4])))
    if not quality and quality2:
        s1 = s1[:4] + str(actions.Quality.inverse(actions.Quality.from_string(s2[4])))
    return s1, s2


def split_string(input):
    strings = input.split(".")
    if len(strings) > 1:
        s1, team_set, action_set, quality_set = expandString(strings[0])
        s2, team_set_2, action_set_2, quality_set_2 = expandString(strings[1])
        s1, s2 = correct_strings(
            s1,
            team_set,
            action_set,
            quality_set,
            s2,
            team_set_2,
            action_set_2,
            quality_set_2,
        )
    else:
        s1, _, _, _ = expandString(strings[0])
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
    player_names = [{}, {}]
    libs = [None, None]

    def __init__(self) -> None:
        self.score = [0, 0]
        self.set_score = [0, 0]
        self.rallies = []
        self.court = Court()

        self._current_actions = []
        self._last_serve = None
        self.teamnames = [None, None]
        self.player_names = [{}, {}]

    def add_string(self, action: str):
        if "sub" in action:
            l = action.split("!")
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
            l = action.split("!")
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
            l = action.split("!")
            team = l[0][0]
            teamname = l[1]
            self.teamnames[int(actions.Team.from_string(team))] = teamname
        elif "pname" in action:
            l = action.split("!")
            team = l[0][0]
            playernumber = int(l[1])
            name = l[2]
            self.player_names[int(actions.Team.from_string(team))][playernumber] = name
        elif "lib" in action:
            l = action.split("!")
            team = l[0][0]
            playernumber = int(l[1])
            self.libs[int(actions.Team.from_string(team))] = playernumber
        else:
            str1, str2 = split_string(action)
            allactions = []
            allactions.append(copy.copy(Gameaction.from_string(str1)))
            if str2:
                allactions.append(copy.copy(Gameaction.from_string(str2)))
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

    def collect_stats(self, teamname):
        team = actions.Team.from_string(teamname)
        playerstats = {}
        allplayers = self.court.fields[int(team)].players
        if self.libs[int(team)]:
            allplayers.append(self.libs[int(team)])

        for player in allplayers:
            playerstats[player.Number] = {}
            if player.Number in self.player_names[int(team)]:
                playerstats[player.Number]["name"] = self.player_names[int(team)][
                    player.Number
                ]
            playerstats[player.Number]["serve"] = {}
            playerstats[player.Number]["serve"]["kill"] = 0
            playerstats[player.Number]["serve"]["ball"] = 0
            playerstats[player.Number]["reception"] = 0
            playerstats[player.Number]["hit"] = {}
            playerstats[player.Number]["hit"]["kill"] = 0
            playerstats[player.Number]["hit"]["ball"] = 0
            playerstats[player.Number]["error"] = 0
            playerstats[player.Number]["block"] = 0
        for player in allplayers:
            for rally in self.rallies:
                for action in rally[0]:
                    if isinstance(action, Gameaction):
                        # is is the right player on the right team
                        if action.Team == team:
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

        playerstats["team"] = {}
        playerstats["team"]["serve"] = {}
        playerstats["team"]["serve"]["kill"] = 0
        playerstats["team"]["reception"] = 0
        playerstats["team"]["hit"] = {}
        playerstats["team"]["hit"]["kill"] = 0
        playerstats["team"]["error"] = 0
        playerstats["team"]["block"] = 0
        for rally in self.rallies:
            for action in rally[0]:
                if isinstance(action, Gameaction):
                    # is is the right player on the right team
                    if action.Team == team:
                        # serve statistics
                        if action.action == Action.Serve:
                            if action.quality == Quality.Kill:
                                playerstats["team"]["serve"]["kill"] += 1
                            elif action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1

                        # hitting statistics
                        if action.action == Action.Hit:
                            if action.quality == Quality.Kill:
                                playerstats["team"]["hit"]["kill"] += 1
                            elif action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1

                        # blocking statistics
                        if action.action == Action.Block:
                            if action.quality == Quality.Kill:
                                playerstats["team"]["block"] += 1
                            elif action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1

                        # blocking statistics
                        if action.action == Action.Reception:
                            playerstats["team"]["reception"] += 1
                            if action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1
        return playerstats