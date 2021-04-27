import ast
import copy
from collections import OrderedDict
from typing import List, Optional

import tvrscouting.statistics.Actions as actions
import tvrscouting.statistics.Actions.SpecialAction as SpecialActions
from tvrscouting.analysis.filters import compare_action_to_string, rally_filter_from_string
from tvrscouting.statistics.Actions.ActionExpansion import StatementSettings, expandString
from tvrscouting.statistics.Actions.GameAction import (
    Action,
    Gameaction,
    Quality,
    SetterCall,
    is_scoring,
)
from tvrscouting.statistics.Players.players import Player, Team
from tvrscouting.utils.errors import TVRSyntaxError


def truncate_list(in_list, size=11):
    if len(in_list) < size:
        return in_list
    else:
        return in_list[-size:]


class Field:
    def __init__(self) -> None:
        self.players: List[Player] = []
        self.setter = None
        for _ in range(6):
            self.players.append(Player(0))

    def get_setter_position(self):
        if self.setter:
            for index, player in enumerate(self.players):
                if player.Number == self.setter:
                    return index + 1
        return 0


class Court:
    def __init__(self) -> None:
        self.fields: List[Field] = []
        f1 = Field()
        self.fields.append(f1)
        f2 = Field()
        self.fields.append(f2)

    def rotate(self, who: int) -> None:
        self.fields[who].players.append(self.fields[who].players.pop(0))


def correct_strings(
    s1: str,
    team: bool,
    action: bool,
    quality: bool,
    from_set: bool,
    to_set: bool,
    players_set: bool,
    s2: str,
    team2: bool,
    action2: bool,
    quality2: bool,
    from_set2: bool,
    to_set2: bool,
    players_set2: bool,
    settings: StatementSettings,
):
    # correct the teams
    if not team2:
        s2 = str(settings.compound_team(s1)) + s2[1:]
    if not team and team2:
        s1 = str(settings.compound_team(21)) + s1[1:]

    # correct the action:
    if not action2:
        s2 = s2[:3] + str(settings.compound_action(s1)) + s2[4:]
    if not action and action2:
        s1 = s1[:3] + str(settings.compound_action(s2)) + s1[4:]

    # correct the quality
    if not quality2:
        s2 = s2[:4] + str(actions.Quality.inverse(actions.Quality.from_string(s1[4]))) + s2[5:]
    if not quality and quality2:
        s1 = s1[:4] + str(actions.Quality.inverse(actions.Quality.from_string(s2[4]))) + s1[5:]

    # correct the from and to position:
    if not from_set2:
        s2 = s2[:7] + s1[8] + s2[8:]
    if not to_set2:
        s2 = s2[:8] + s1[7] + s2[9:]
    if not from_set:
        s1 = s1[:7] + s2[8] + s1[8:]
    if not to_set:
        s1 = s1[:8] + s2[7] + s1[9:]

    if s1[3] == "h" or s2[3] == "h":
        if not players_set2:
            s2 = s2[:9] + s1[10] + s2[10:]
        if not players_set and players_set2:
            s1 = s1[:9] + s2[10] + s1[10:]

    return s1, s2


def split_compound_statements(input, settings: StatementSettings):
    strings = input.split(".")
    if len(strings) > 1:
        (
            s1,
            team_set,
            action_set,
            quality_set,
            from_direction_set,
            to_directon_set,
            players_set,
        ) = expandString(strings[0], settings)
        if len(strings[1]) == 0:
            raise TVRSyntaxError()
        (
            s2,
            team_set_2,
            action_set_2,
            quality_set_2,
            from_direction_set_2,
            to_directon_set_2,
            players_set_2,
        ) = expandString(strings[1], settings)
        s1, s2 = correct_strings(
            s1,
            team_set,
            action_set,
            quality_set,
            from_direction_set,
            to_directon_set,
            players_set,
            s2,
            team_set_2,
            action_set_2,
            quality_set_2,
            from_direction_set_2,
            to_directon_set_2,
            players_set_2,
            settings,
        )
    else:
        s1, _, _, _, _, _, _ = expandString(strings[0], settings)
        s2 = None
    return s1, s2


class Rally:
    def __init__(self) -> None:
        self.actions: List[Action] = []
        self.court: Optional[Court] = None
        self.score: List[int] = []
        self.set_score: List[int] = []
        self.last_serve: Optional[Team] = None
        self.setter_call: Optional[SetterCall] = None

    def correct_setter_call(self):
        if self.setter_call:
            if self.setter_call.team is None:
                self.setter_call.team = self.find_receiveing_team_from_reception()
            if self.setter_call.team is None:
                self.setter_call.team = self.find_receiveing_team_from_serve()

    def find_receiveing_team_from_reception(self):
        for action in self.actions:
            if isinstance(action, Gameaction):
                action_string = str(action)
                if compare_action_to_string(action_string, "@@@r"):
                    return action.team
        return None

    def find_receiveing_team_from_serve(self):
        for action in self.actions:
            if isinstance(action, Gameaction):
                action_string = str(action)
                if compare_action_to_string(action_string, "@@@s"):
                    return Team.inverse(action.team)
        return None

    def find_receiveing_team_from_setter_call(self):
        if self.setter_call and self.setter_call.team:
            return self.setter_call.team
        return None

    def find_receiveing_team(self):
        team = self.find_receiveing_team_from_setter_call()
        if team is not None:
            return team
        team = self.find_receiveing_team_from_reception()
        if team is not None:
            return team
        team = self.find_receiveing_team_from_serve()
        if team is not None:
            return team
        return self.last_serve

    def wins_in_k1(self) -> bool:
        rece_team = self.find_receiveing_team()
        for action in self.actions:
            if isinstance(action, Gameaction):
                current_action = str(action)
                if compare_action_to_string(current_action, str(rece_team) + "@@h#"):
                    return True
                elif compare_action_to_string(current_action, "@@@h"):
                    return False
        return False

    def get_k1_hit(self) -> Optional[Gameaction]:
        rece_team = self.find_receiveing_team()
        for action in self.actions:
            if isinstance(action, Gameaction):
                current_action = str(action)
                if compare_action_to_string(current_action, str(rece_team) + "@@h"):
                    return current_action
                elif compare_action_to_string(current_action, str(Team.inverse(rece_team))):
                    return None
        return None


class GameState:
    def __init__(self) -> None:
        self.score: List[int] = [0, 0]
        self.set_score: List[int] = [0, 0]
        self.final_scores: List[List[int]] = []
        self.rallies: List[Rally] = []
        self.court: Court = Court()

        self._current_actions: List[Action] = []
        self.scoring_team: Optional[Team] = None
        self.set_ended = False
        self._setter_call = None

        self._last_serve = None
        self.teamnames = [None, None]
        self.setters = [None, None]
        self.players: List[List[Player]] = [[], []]

        self.settings: StatementSettings = StatementSettings()

        self.details = []

    def get_players_from_game_state(self) -> List[List[Player]]:
        retval = [[], []]
        for rally in self.rallies:
            for action in rally.actions:
                if isinstance(action, SpecialActions.InitializePlayer):
                    p = Player(action.number, action.position, action.name)
                    retval[int(action.team)].append(p)
        return retval

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

    def add_action_set_serving_team_from_string(self, action: str, time_stamp=None) -> None:
        """add a SetServingTeam action from a string formatted [Team]serve"""
        split_string = action.split("!")
        autogen = False
        if len(split_string) > 1:
            autogen = ast.literal_eval(split_string[1])
        team = split_string[0][0]
        action = SpecialActions.SetServingTeam(actions.Team.from_string(team), time_stamp, autogen)
        self.add_logical([action])

    def add_string(self, action: str, time_stamp=None):
        if len(action) == 0:
            return
        if "sub" in action:
            self.add_action_substitution_from_string(action, time_stamp)
        elif "serve" in action:
            self.add_action_set_serving_team_from_string(action, time_stamp)
        elif "point" in action:
            # TODO: continue the refactoring here
            split_action = action.split("!")
            number = int(split_action[1])
            team = split_action[0][0]
            action = SpecialActions.Point(actions.Team.from_string(team), time_stamp)
            self.add_logical([action])
        elif "endset" in action:
            team = action[0][0]
            action = SpecialActions.Endset(actions.Team.from_string(team), time_stamp)
            self.add_logical([action])
        elif "rota" in action:
            split_action = action.split("!")
            team = split_action[0][0]
            direction = True if int(split_action[1]) > 0 else False
            action = SpecialActions.Rotation(actions.Team.from_string(team), direction, time_stamp)
            self.add_logical([action])
        elif "team" in action:
            action = SpecialActions.InitializeTeamName(action, time_stamp)
            self.add_logical([action], time_stamp)
        elif "player" in action:
            action = SpecialActions.InitializePlayer(action, time_stamp)
            self.add_logical([action], time_stamp)
        elif "setter" in action:
            split_action = action.split("!")
            team = split_action[0][0]
            setter_number = int(split_action[1])
            action = SpecialActions.SetSetter(
                actions.Team.from_string(team), setter_number, time_stamp
            )
            self.add_logical([action], time_stamp)
        elif "timeout" in action:
            action = SpecialActions.Timeout(action, time_stamp)
            self.add_logical([action], time_stamp)
        elif "K" in action:
            action = SetterCall.from_string(action, time_stamp)
            self.add_logical([action], time_stamp)
        else:
            str1, str2 = split_compound_statements(action, self.settings)
            allactions = []
            allactions.append(copy.copy(Gameaction.from_string(str1, time_stamp)))
            if str2:
                allactions.append(copy.copy(Gameaction.from_string(str2, time_stamp)))
            self.add_logical(allactions, time_stamp)

    def create_action_list_from_string(self, action: str, time_stamp=None):
        if len(action) == 0:
            return
        if "sub" in action:
            split_string = action.split("!")
            number = int(split_string[1])
            position = int(split_string[2])
            team = split_string[0][0]
            return [
                SpecialActions.Substitute(
                    actions.Team.from_string(team), number, position, time_stamp
                )
            ]
        elif "serve" in action:
            split_string = action.split("!")
            autogen = False
            if len(split_string) > 1:
                autogen = ast.literal_eval(split_string[1])
            team = split_string[0][0]
            return [
                SpecialActions.SetServingTeam(actions.Team.from_string(team), time_stamp, autogen)
            ]
        elif "point" in action:
            # TODO: this is copied form above, refactor!
            split_string = action.split("!")
            number = int(split_string[1])
            team = split_string[0][0]
            return [SpecialActions.Point(actions.Team.from_string(team), time_stamp)]
        elif "endset" in action:
            team = action[0][0]
            return [SpecialActions.Endset(actions.Team.from_string(team), time_stamp)]
        elif "rota" in action:
            split_string = action.split("!")
            team = split_string[0][0]
            direction = True if int(split_string[1]) > 0 else False
            return [SpecialActions.Rotation(actions.Team.from_string(team), direction, time_stamp)]
        elif "team" in action:
            return [SpecialActions.InitializeTeamName(action, time_stamp)]
        elif "player" in action:
            return [SpecialActions.InitializePlayer(action, time_stamp)]
        elif "timeout" in action:
            return [SpecialActions.Timeout(action, time_stamp)]
        elif "setter" in action:
            split_string = action.split("!")
            team = split_string[0][0]
            setter_number = int(split_string[1])
            return [
                SpecialActions.SetSetter(actions.Team.from_string(team), setter_number, time_stamp)
            ]
        elif "K" in action:
            return [SetterCall.from_string(action, time_stamp)]
        else:
            str1, str2 = split_compound_statements(action, self.settings)
            allactions = []
            allactions.append(copy.copy(Gameaction.from_string(str1, time_stamp)))
            if str2:
                allactions.append(copy.copy(Gameaction.from_string(str2, time_stamp)))
            return allactions

    def add_plain(self, action_list, time_stamp=None):
        for action in action_list:
            self._current_actions.append(action)
        self.flush_actions_plain()
        for action in action_list:
            # TODO: this is copied form below, refactor!
            if isinstance(action, SpecialActions.Substitute):
                who = action.team_
                field = self.court.fields[int(who)].players
                pos = action.position_in - 1
                if field[pos].Number != 0:
                    action.player_out = field[pos].Number
                fpos = field[:pos]
                fpos.append(Player(action.player_in))
                self.court.fields[int(who)].players = fpos + field[pos + 1 :]
            elif isinstance(action, SpecialActions.Endset):
                self.final_scores.append([self.score[0], self.score[1]])
                self.set_score[int(action.team_)] += 1
                self.score[0] = 0
                self.score[1] = 0
                self.court.fields[0] = Field()
                self.court.fields[1] = Field()
            elif isinstance(action, SpecialActions.Rotation):
                self.court.rotate(int(action.team_))
            elif isinstance(action, SpecialActions.SetServingTeam):
                self._last_serve = action.team_
            elif isinstance(action, SpecialActions.Point):
                self.score[int(action.team_)] += action.value
            elif isinstance(action, SpecialActions.InitializePlayer):
                p = Player(action.number, action.position, action.name, action.is_capitan)
                self.players[int(action.team)].append(p)
            elif isinstance(action, SpecialActions.InitializeTeamName):
                self.teamnames[int(action.team)] = action.name
            elif isinstance(action, SpecialActions.SetSetter):
                self.court.fields[int(action.team_)].setter = action.setter_number
            elif isinstance(action, Gameaction):
                pass

    def add_logical(self, action_list, time_stamp=None):
        for action in action_list:
            self._current_actions.append(action)
        for action in action_list:
            if isinstance(action, SpecialActions.Substitute):
                who = action.team_
                field = self.court.fields[int(who)].players
                pos = action.position_in - 1
                if field[pos].Number != 0:
                    action.player_out = field[pos].Number
                fpos = field[:pos]
                fpos.append(Player(action.player_in))
                self.court.fields[int(who)].players = fpos + field[pos + 1 :]
                self.flush_actions()
            elif isinstance(action, SpecialActions.Endset):
                self.final_scores.append([self.score[0], self.score[1]])
                self.set_score[int(action.team_)] += 1
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
                p = Player(action.number, action.position, action.name, action.is_capitan)
                self.players[int(action.team)].append(p)
                self.flush_actions()
            elif isinstance(action, SpecialActions.InitializeTeamName):
                self.teamnames[int(action.team)] = action.name
                self.flush_actions()
            elif isinstance(action, SetterCall):
                self._setter_call = action
            elif isinstance(action, SpecialActions.SetSetter):
                self.court.fields[int(action.team_)].setter = action.setter_number
            elif isinstance(action, SpecialActions.Timeout):
                pass
            else:
                who, was_score = is_scoring(action)
                if was_score:
                    self.scoring_team = who
                    self.scoring_time_stamp = time_stamp

    def housekeeping_from_scoring_team(self, scoring_team):
        team = int(scoring_team)
        opponent = int(actions.Team.inverse(scoring_team))
        self._current_actions.append(
            actions.Point(scoring_team, time_stamp=self.scoring_time_stamp, auto_generated=True)
        )
        if scoring_team is not self._last_serve:
            self._current_actions.append(
                actions.Rotation(
                    scoring_team, time_stamp=self.scoring_time_stamp, auto_generated=True
                )
            )
            self._current_actions.append(
                actions.SetServingTeam(
                    scoring_team, time_stamp=self.scoring_time_stamp, auto_generated=True
                )
            )
            self.court.rotate(team)
        self._last_serve = scoring_team
        self.score[team] += 1
        if (
            self.score[team] >= self.max_points_in_set()
            and self.score[team] - 2 >= self.score[opponent]
        ):
            self.set_ended = True
        else:
            self.scoring_time_stamp = None
            self.scoring_team = None

    def end_set_from_scoring_team(self, scoring_team):
        team = int(scoring_team)
        self._current_actions.append(
            actions.Endset(scoring_team, time_stamp=self.scoring_time_stamp, auto_generated=True)
        )
        self.final_scores.append([self.score[0], self.score[1]])
        self.set_score[team] += 1
        self.score[0] = 0
        self.score[1] = 0
        self.court.fields[0] = Field()
        self.court.fields[1] = Field()
        self.set_ended = False
        self.scoring_time_stamp = None
        self.scoring_team = None

    def flush_actions_plain(self):
        current_rally = Rally()
        current_rally.court = copy.deepcopy(self.court)
        current_rally.score = copy.deepcopy(self.score)
        current_rally.set_score = copy.deepcopy(self.set_score)
        current_rally.last_serve = copy.deepcopy(self._last_serve)
        current_rally.actions = list.copy(self._current_actions)
        current_rally.setter_call = self._setter_call
        current_rally.correct_setter_call()
        self.rallies.append(current_rally)
        self._setter_call = None
        self._current_actions.clear()

    def flush_actions(self):
        if len(self._current_actions):
            current_rally = Rally()
            current_rally.court = copy.deepcopy(self.court)
            current_rally.score = copy.deepcopy(self.score)
            current_rally.set_score = copy.deepcopy(self.set_score)
            current_rally.last_serve = copy.deepcopy(self._last_serve)
            # we need to copy in the state first before we do housekeeping as we update the score
            if self.scoring_team:
                self.housekeeping_from_scoring_team(self.scoring_team)
            # we ned to copy in the actions after housekeeping in case point-actions happened
            current_rally.actions = list.copy(self._current_actions)
            current_rally.setter_call = self._setter_call
            current_rally.correct_setter_call()
            self.rallies.append(current_rally)
            self._setter_call = None
            self._current_actions.clear()
            if self.set_ended:
                endset_rally = Rally()
                endset_rally.court = copy.deepcopy(self.court)
                endset_rally.score = copy.deepcopy(self.score)
                endset_rally.set_score = copy.deepcopy(self.set_score)
                endset_rally.last_serve = copy.deepcopy(self._last_serve)
                # need to copy in the state first before we do housekeeping as we update the score
                self.end_set_from_scoring_team(self.scoring_team)
                # we ned to copy in the actions after housekeeping in case point-actions happened
                endset_rally.actions = list.copy(self._current_actions)
                self.rallies.append(endset_rally)
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
            if rally.set_score[0] + rally.set_score[1] == activeset:
                total = rally.score[0] + rally.score[1]
                delta = rally.score[0] - rally.score[1]
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
            if rally.set_score[0] + rally.set_score[1] == activeset:
                score = [rally.score[0], rally.score[1]]
                if len(scores) < 1 or scores[-1] != score:
                    scores.append(score)
        if self.score[0] + self.score[1] != 0:
            scores.append(self.score)
        scores = truncate_list(scores)
        return scores

    def collect_stats(self, teamname) -> OrderedDict:
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
            playerstats[player.Number]["rece"]["perc"] = 0
            playerstats[player.Number]["hit"] = {}
            playerstats[player.Number]["hit"]["kill"] = 0
            playerstats[player.Number]["hit"]["total"] = 0
            playerstats[player.Number]["hit"]["perc"] = 0
            playerstats[player.Number]["error"] = 0
            playerstats[player.Number]["block"] = 0
            playerstats[player.Number]["points"] = 0
        for player in allplayers:
            for rally in self.rallies:
                for action in rally.actions:
                    if isinstance(action, Gameaction):
                        # is is the right player on the right team
                        if action.team == team:
                            if action.player == player.Number:
                                playerstats[player.Number]["played"] = True
                                playerstats[player.Number]["group"] = int(player.Position)
                                # serve statistics
                                if action.action == Action.Serve:
                                    playerstats[player.Number]["serve"]["total"] += 1
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["serve"]["kill"] += 1
                                        playerstats[player.Number]["points"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

                                # hitting statistics
                                elif action.action == Action.Hit:
                                    playerstats[player.Number]["hit"]["total"] += 1
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["hit"]["kill"] += 1
                                        playerstats[player.Number]["points"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

                                # blocking statistics
                                elif action.action == Action.Block:
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["block"] += 1
                                        playerstats[player.Number]["points"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

                                # rece statistics
                                elif action.action == Action.Reception:
                                    playerstats[player.Number]["rece"]["total"] += 1
                                    if (
                                        action.quality == Quality.Perfect
                                        or action.quality == Quality.Good
                                    ):
                                        playerstats[player.Number]["rece"]["win"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1
                                # other actions
                                else:
                                    if action.quality == Quality.Kill:
                                        playerstats[player.Number]["points"] += 1
                                    elif action.quality == Quality.Error:
                                        playerstats[player.Number]["error"] += 1

        for numbers in [
            number for number, stats in playerstats.items() if stats["played"] is False
        ]:
            del playerstats[numbers]

        playerstats["team"] = {}
        playerstats["team"]["name"] = self.teamnames[int(team)] if self.teamnames[int(team)] else ""
        playerstats["team"]["group"] = 7
        playerstats["team"]["serve"] = {}
        playerstats["team"]["serve"]["kill"] = 0
        playerstats["team"]["serve"]["total"] = 0
        playerstats["team"]["rece"] = {}
        playerstats["team"]["rece"]["win"] = 0
        playerstats["team"]["rece"]["total"] = 0
        playerstats["team"]["rece"]["perc"] = 0
        playerstats["team"]["hit"] = {}
        playerstats["team"]["hit"]["kill"] = 0
        playerstats["team"]["hit"]["total"] = 0
        playerstats["team"]["hit"]["perc"] = 0
        playerstats["team"]["error"] = 0
        playerstats["team"]["block"] = 0
        playerstats["team"]["points"] = 0
        for rally in self.rallies:
            for action in rally.actions:
                if isinstance(action, Gameaction):
                    # is is the right player on the right team
                    if action.team == team:
                        # serve statistics
                        if action.action == Action.Serve:
                            playerstats["team"]["serve"]["total"] += 1
                            if action.quality == Quality.Kill:
                                playerstats["team"]["serve"]["kill"] += 1
                                playerstats["team"]["points"] += 1
                            elif action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1

                        # hitting statistics
                        elif action.action == Action.Hit:
                            playerstats["team"]["hit"]["total"] += 1
                            if action.quality == Quality.Kill:
                                playerstats["team"]["hit"]["kill"] += 1
                                playerstats["team"]["points"] += 1
                            elif action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1

                        # blocking statistics
                        elif action.action == Action.Block:
                            if action.quality == Quality.Kill:
                                playerstats["team"]["block"] += 1
                                playerstats["team"]["points"] += 1
                            elif action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1

                        # blocking statistics
                        elif action.action == Action.Reception:
                            playerstats["team"]["rece"]["total"] += 1
                            if action.quality == Quality.Perfect or action.quality == Quality.Good:
                                playerstats["team"]["rece"]["win"] += 1
                            elif action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1
                        # other actions
                        else:
                            if action.quality == Quality.Kill:
                                playerstats["team"]["points"] += 1
                            elif action.quality == Quality.Error:
                                playerstats["team"]["error"] += 1

        for stats in playerstats.values():
            stats["rece"]["perc"] = (
                int(100 * stats["rece"]["win"] / stats["rece"]["total"])
                if stats["rece"]["total"] > 0
                else 0
            )
            stats["hit"]["perc"] = (
                int(100 * stats["hit"]["kill"] / stats["hit"]["total"])
                if stats["hit"]["total"] > 0
                else 0
            )

        return playerstats

    def fix_time_stamps(self, old_game_state) -> None:
        for rally in self.rallies:
            filter_string = (
                "%02d" % (rally.score[0])
                + "%02d" % (rally.score[0] + 1)
                + "%02d" % (rally.score[1])
                + "%02d" % (rally.score[1] + 1)
                + str(rally.set_score[0])
                + str(rally.set_score[1])
                + "@"
                + "@"
            )
            old_rallies = rally_filter_from_string(filter_string, old_game_state.rallies)
            for new_action in rally.actions:
                if isinstance(new_action, Gameaction):
                    for rally in old_rallies:
                        if not new_action.time_stamp:
                            for old_action in rally.actions:
                                if isinstance(old_action, Gameaction):
                                    if str(old_action) == str(new_action):
                                        new_action.time_stamp = old_action.time_stamp
                                        break
        last_time_stamp = None
        for rally in self.rallies:
            for action in rally.actions:
                if action.time_stamp and last_time_stamp:
                    if action.time_stamp < last_time_stamp:
                        action.time_stamp = last_time_stamp
                elif last_time_stamp:
                    action.time_stamp = last_time_stamp
                last_time_stamp = action.time_stamp
