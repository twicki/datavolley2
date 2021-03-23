import copy
import enum
import ast
from copy import deepcopy
from collections import OrderedDict


import tvrscouting.statistics.Actions as actions
from tvrscouting.utils.errors import TVRSyntaxError

from tvrscouting.statistics.Actions.GameAction import (
    Gameaction,
    is_scoring,
    Action,
    Quality,
)
import tvrscouting.statistics.Actions.SpecialAction as SpecialActions
from tvrscouting.statistics.Players.players import Player
from tvrscouting.analysis.filters import *


def truncate_list(in_list, size=11):
    if len(in_list) < size:
        return in_list
    else:
        return in_list[-size:]


class Field:
    def __init__(self) -> None:
        self.players = []
        for i in range(6):
            self.players.append(Player(0))


class Court:
    def __init__(self) -> None:
        self.fields = []
        f1 = Field()
        self.fields.append(f1)
        f2 = Field()
        self.fields.append(f2)

    def rotate(self, who: int) -> None:
        self.fields[who].players.append(self.fields[who].players.pop(0))


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
        if user_string[0] in ["#", "+", "-", "=", "p", "o"]:
            returnvalue = returnvalue[:4] + user_string[0] + returnvalue[5:]
            user_string = user_string[1:]
            return returnvalue, user_string, True
    return returnvalue, user_string, False


def set_combination(user_string, returnvalue):
    if len(user_string) > 1:
        if user_string[0] in ["D", "X", "C"]:
            returnvalue = returnvalue[:5] + user_string[0:2] + returnvalue[7:]
            user_string = user_string[2:]
        return returnvalue, user_string
    return returnvalue, user_string


def set_from_direction(user_string, returnvalue):
    if len(user_string) and user_string[0].isnumeric():
        returnvalue = returnvalue[:7] + user_string[0] + returnvalue[8:]
        user_string = user_string[1:]
        return returnvalue, user_string, True
    return returnvalue, user_string, False


def set_to_direction(user_string, returnvalue):
    if len(user_string) and user_string[0].isnumeric():
        returnvalue = returnvalue[:8] + user_string[0]
        return returnvalue, True
    elif len(user_string):
        raise TVRSyntaxError()
    return returnvalue, False


def expandString(user_string):
    returnvalue = "*00h+D000"
    returnvalue, user_string, team_set = set_team(user_string, returnvalue)
    returnvalue, user_string = set_number(user_string, returnvalue)
    returnvalue, user_string, action_set = set_action(user_string, returnvalue)
    returnvalue, user_string, quality_set = set_quality(user_string, returnvalue)

    returnvalue, user_string = set_combination(user_string, returnvalue)
    returnvalue, user_string, from_direction_set = set_from_direction(
        user_string, returnvalue
    )
    returnvalue, to_directon_set = set_to_direction(user_string, returnvalue)

    return (
        returnvalue,
        team_set,
        action_set,
        quality_set,
        from_direction_set,
        to_directon_set,
    )


def correct_strings(
    s1,
    team,
    action,
    quality,
    from_set,
    to_set,
    s2,
    team2,
    action2,
    quality2,
    from_set2,
    to_set2,
):
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
        s2 = (
            s2[:4]
            + str(actions.Quality.inverse(actions.Quality.from_string(s1[4])))
            + s2[5:]
        )
    if not quality and quality2:
        s1 = (
            s1[:4]
            + str(actions.Quality.inverse(actions.Quality.from_string(s2[4])))
            + s1[5:]
        )

    ## correct the from and to position:
    if not from_set2:
        s2 = s2[:7] + s1[8] + s2[8:]
    if not to_set2:
        s2 = s2[:8] + s1[7]
    if not from_set:
        s1 = s1[:7] + s2[8] + s1[8:]
    if not to_set:
        s1 = s1[:8] + s2[7]

    return s1, s2


def split_string(input):
    strings = input.split(".")
    if len(strings) > 1:
        (
            s1,
            team_set,
            action_set,
            quality_set,
            from_direction_set,
            to_directon_set,
        ) = expandString(strings[0])
        (
            s2,
            team_set_2,
            action_set_2,
            quality_set_2,
            from_direction_set_2,
            to_directon_set_2,
        ) = expandString(strings[1])
        s1, s2 = correct_strings(
            s1,
            team_set,
            action_set,
            quality_set,
            from_direction_set,
            to_directon_set,
            s2,
            team_set_2,
            action_set_2,
            quality_set_2,
            from_direction_set_2,
            to_directon_set_2,
        )
    else:
        s1, _, _, _, _, _ = expandString(strings[0])
        s2 = None
    return s1, s2


class GameState:
    score = [0, 0]
    set_score = [0, 0]
    rallies = []
    court = None

    _current_actions = []
    _last_serve = None
    teamnames = [None, None]
    players = [[], []]

    def __init__(self) -> None:
        self.score = [0, 0]
        self.set_score = [0, 0]
        self.rallies = []
        self.court = Court()

        self._current_actions = []
        self._last_serve = None
        self.teamnames = [None, None]
        self.players = [[], []]

        self.details = []

    def add_action_substitution_from_string(self, action: str, time_stamp=None) -> None:
        """add a substitiution action from a string formatted [Team]sub![Number]![Position]"""
        split_string = action.split("!")
        number = int(split_string[1])
        position = int(split_string[2])
        team = split_string[0][0]
        action = SpecialActions.Substitute(
            actions.Team.from_string(team), number, position, time_stamp
        )
        self.add_logical([action])

    def add_action_set_serving_team_from_string(
        self, action: str, time_stamp=None
    ) -> None:
        """add a SetServingTeam action from a string formatted [Team]serve"""
        split_string = action.split("!")
        autogen = False
        if len(split_string) > 1:
            autogen = ast.literal_eval(split_string[1])
        team = split_string[0][0]
        action = SpecialActions.SetServingTeam(
            actions.Team.from_string(team), time_stamp, autogen
        )
        self.add_logical([action])

    def add_string(self, action: str, time_stamp=None):
        if "sub" in action:
            self.add_action_substitution_from_string(action, time_stamp)
        elif "serve" in action:
            self.add_action_set_serving_team_from_string(action, time_stamp)
        elif "point" in action:
            # TODO: continue the refactoring here
            l = action.split("!")
            number = int(l[1])
            team = l[0][0]
            action = SpecialActions.Point(actions.Team.from_string(team), time_stamp)
            self.add_logical([action])
        elif "endset" in action:
            team = action[0][0]
            action = SpecialActions.Endset(actions.Team.from_string(team), time_stamp)
            self.add_logical([action])
        elif "rota" in action:
            l = action.split("!")
            team = l[0][0]
            direction = True if int(l[1]) > 0 else False
            action = SpecialActions.Rotation(
                actions.Team.from_string(team), direction, time_stamp
            )
            self.add_logical([action])
        elif "team" in action:
            action = SpecialActions.InitializeTeamName(action, time_stamp)
            self.add_logical([action], time_stamp)
        elif "player" in action:
            action = SpecialActions.InitializePlayer(action, time_stamp)
            self.add_logical([action], time_stamp)
        else:
            str1, str2 = split_string(action)
            allactions = []
            allactions.append(copy.copy(Gameaction.from_string(str1, time_stamp)))
            if str2:
                allactions.append(copy.copy(Gameaction.from_string(str2, time_stamp)))
            self.add_logical(allactions, time_stamp)

    def add_plain_from_string(self, action, time_stamp=None):
        # TODO: refactor things out here
        if "sub" in action:
            self.add_action_substitution_from_string(action, time_stamp)
        elif "serve" in action:
            l = action.split("!")
            self.add_action_set_serving_team_from_string(action, time_stamp)
        elif "point" in action:
            # TODO: continue the refactoring here
            l = action.split("!")
            autogen = ast.literal_eval(l[1])
            team = l[0][0]
            action = SpecialActions.Point(
                actions.Team.from_string(team),
                time_stamp=time_stamp,
                auto_generated=autogen,
            )
            self.add_logical([action])
        elif "endset" in action:
            l = action.split("!")
            autogen = ast.literal_eval(l[1])
            team = l[0][0]
            action = SpecialActions.Endset(
                actions.Team.from_string(team),
                time_stamp=time_stamp,
                auto_generated=autogen,
            )
            self.add_logical([action])
        elif "rota" in action:
            l = action.split("!")
            autogen = ast.literal_eval(l[2])
            team = l[0][0]
            direction = True if int(l[1]) > 0 else False
            action = SpecialActions.Rotation(
                actions.Team.from_string(team),
                direction,
                time_stamp=time_stamp,
                auto_generated=autogen,
            )
            self.add_logical([action])
        elif "team" in action:
            action = SpecialActions.InitializeTeamName(action, time_stamp)
            self.add_logical([action])
        elif "player" in action:
            action = SpecialActions.InitializePlayer(action, time_stamp)
            self.add_logical([action])
        else:
            self.add_plain([Gameaction.from_string(action, time_stamp)])

    def add_plain(self, action_list, time_stamp=None):
        for action in action_list:
            self._current_actions.append(action)
        for action in action_list:
            if isinstance(action, Gameaction):
                _, was_score = is_scoring(action)
                if was_score:
                    self.flush_actions()
            else:
                self.flush_actions()

    def add_logical(self, action_list, time_stamp=None):
        for action in action_list:
            self._current_actions.append(action)
        for action in action_list:
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
                self.court.fields[0] = Field()
                self.court.fields[1] = Field()
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
            elif isinstance(action, SpecialActions.InitializePlayer):
                p = Player(action.number, action.position, action.name)
                self.players[int(action.team)].append(p)
                self.flush_actions()
            elif isinstance(action, SpecialActions.InitializeTeamName):
                self.teamnames[int(action.team)] = action.name
                self.flush_actions()
            else:
                who, was_score = is_scoring(action)
                if was_score:
                    index = int(who)
                    self._current_actions.append(
                        actions.Point(who, time_stamp=time_stamp, auto_generated=True)
                    )

                    # flush the current action before housekeeping
                    self.flush_actions()

                    # housekeeping: serve
                    if who is not self._last_serve:
                        self._current_actions.append(
                            actions.Rotation(
                                who, time_stamp=time_stamp, auto_generated=True
                            )
                        )
                        self._current_actions.append(
                            actions.SetServingTeam(
                                who, time_stamp=time_stamp, auto_generated=True
                            )
                        )
                        self.court.rotate(index)
                    self._last_serve = who

                    # housekeeping: scoring
                    opponent = int(actions.Team.inverse(who))
                    self.score[index] += 1
                    if (
                        self.score[index] >= self.max_points_in_set()
                        and self.score[index] - 2 >= self.score[opponent]
                    ):
                        self._current_actions.append(
                            actions.Endset(
                                who, time_stamp=time_stamp, auto_generated=True
                            )
                        )
                        self.flush_actions()
                        self.set_score[index] += 1
                        self.score[0] = 0
                        self.score[1] = 0
                        self.court.fields[0] = Field()
                        self.court.fields[1] = Field()

    def flush_actions(self):
        c = Court()
        c.fields[0].players = list.copy(self.court.fields[0].players)
        c.fields[1].players = list.copy(self.court.fields[1].players)

        self.rallies.append(
            (
                list.copy(self._current_actions),
                copy.deepcopy(self.court),
                copy.deepcopy(self.score),
                copy.deepcopy(self.set_score),
                copy.deepcopy(str(self._last_serve)),
            )
        )
        self._current_actions.clear()

    def max_points_in_set(self):
        if self.set_score[0] + self.set_score[1] < 4:
            return 25
        else:
            return 15

    def return_timeline(self):
        totals = []
        deltas = []
        # if we are at the end of a set, we want to show the last one:
        if self.score[0] + self.score[1] == 0:
            activeset = self.set_score[0] + self.set_score[1] - 1
        else:
            activeset = self.set_score[0] + self.set_score[1]
        for rally in self.rallies:
            if rally[3][0] + rally[3][1] == activeset:
                total = rally[2][0] + rally[2][1]
                delta = rally[2][0] - rally[2][1]
                if len(totals) < 1 or totals[-1] is not total:
                    totals.append(total)
                    deltas.append(delta)
        if self.score[0] + self.score[1] != 0:
            totals.append(self.score[0] + self.score[1])
            deltas.append(self.score[0] - self.score[1])
        return totals, deltas

    def return_truncated_scores(self):
        scores = []
        # if we are at the end of a set, we want to show the last one:
        if self.score[0] + self.score[1] == 0:
            activeset = self.set_score[0] + self.set_score[1] - 1
        else:
            activeset = self.set_score[0] + self.set_score[1]
        for rally in self.rallies:
            if rally[3][0] + rally[3][1] == activeset:
                score = [rally[2][0], rally[2][1]]
                if len(scores) < 1 or scores[-1] != score:
                    scores.append(score)
        if self.score[0] + self.score[1] != 0:
            scores.append(self.score)
        scores = truncate_list(scores)
        return scores

    def collect_stats(self, teamname):
        team = actions.Team.from_string(teamname)
        playerstats = OrderedDict()

        self.players[int(team)] = sorted(
            self.players[int(team)], key=lambda player: player.Position
        )
        allplayers = self.players[int(team)]

        for player in allplayers:
            playerstats[player.Number] = {}
            playerstats[player.Number]["played"] = False
            for teams_player in self.players[int(team)]:
                if teams_player.Number == player.Number:
                    playerstats[player.Number]["name"] = (
                        str(player.Number) + " " + teams_player.Name
                    )
            playerstats[player.Number]["serve"] = {}
            playerstats[player.Number]["serve"]["kill"] = 0
            playerstats[player.Number]["serve"]["total"] = 0
            playerstats[player.Number]["rece"] = {}
            playerstats[player.Number]["rece"]["win"] = 0
            playerstats[player.Number]["rece"]["total"] = 0
            playerstats[player.Number]["hit"] = {}
            playerstats[player.Number]["hit"]["kill"] = 0
            playerstats[player.Number]["hit"]["total"] = 0
            playerstats[player.Number]["error"] = 0
            playerstats[player.Number]["block"] = 0
        for player in allplayers:
            for rally in self.rallies:
                for action in rally[0]:
                    if isinstance(action, Gameaction):
                        # is is the right player on the right team
                        if action.team == team:
                            if action.player == player.Number:
                                playerstats[player.Number]["played"] = True
                                playerstats[player.Number]["group"] = int(
                                    player.Position
                                )
                                # serve statistics
                                if action.action == Action.Serve:
                                    playerstats[player.Number]["serve"]["total"] += 1
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["serve"]["kill"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

                                # hitting statistics
                                if action.action == Action.Hit:
                                    playerstats[player.Number]["hit"]["total"] += 1
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["hit"]["kill"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

                                # blocking statistics
                                if action.action == Action.Block:
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["block"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

                                # blocking statistics
                                if action.action == Action.Reception:
                                    playerstats[player.Number]["rece"]["total"] += 1
                                    if (
                                        action.quality == Quality.Perfect
                                        or action.quality == Quality.Good
                                    ):
                                        playerstats[player.Number]["rece"]["win"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

        for numbers in [
            number for number, stats in playerstats.items() if stats["played"] == False
        ]:
            del playerstats[numbers]

        playerstats["team"] = {}
        playerstats["team"]["name"] = (
            self.teamnames[int(team)] if self.teamnames[int(team)] else ""
        )
        playerstats["team"]["group"] = 7
        playerstats["team"]["serve"] = {}
        playerstats["team"]["serve"]["kill"] = 0
        playerstats["team"]["rece"] = 0
        playerstats["team"]["hit"] = {}
        playerstats["team"]["hit"]["kill"] = 0
        playerstats["team"]["error"] = 0
        playerstats["team"]["block"] = 0
        for rally in self.rallies:
            for action in rally[0]:
                if isinstance(action, Gameaction):
                    # is is the right player on the right team
                    if action.team == team:
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
                            playerstats["team"]["rece"] += 1
                            if action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1
        return playerstats

    def fix_time_stamps(self, old_game_state) -> None:
        for rally in self.rallies:
            filter_string = (
                "%02d" % (rally[2][0])
                + "%02d" % (rally[2][0] + 1)
                + "%02d" % (rally[2][1])
                + "%02d" % (rally[2][1] + 1)
                + str(rally[3][0])
                + str(rally[3][1])
                + "@"
                + "@"
            )
            old_rallies = ralley_filter_from_string(
                filter_string, old_game_state.rallies
            )
            for new_action in rally[0]:
                if isinstance(new_action, Gameaction):
                    for rally in old_rallies:
                        if not new_action.time_stamp:
                            for old_action in rally[0]:
                                if isinstance(old_action, Gameaction):
                                    if str(old_action) == str(new_action):
                                        new_action.time_stamp = old_action.time_stamp
                                        break
        last_time_stamp = None
        for rally in self.rallies:
            for action in rally[0]:
                if action.time_stamp and last_time_stamp:
                    if action.time_stamp < last_time_stamp:
                        action.time_stamp = last_time_stamp
                elif last_time_stamp:
                    action.time_stamp = last_time_stamp
                last_time_stamp = action.time_stamp
