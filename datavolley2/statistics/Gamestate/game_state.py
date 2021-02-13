import copy
import enum

import datavolley2.statistics.Actions as actions
import datavolley2.statistics.Actions.GameAction as GameAction
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
            str1, str2 = actions.GameAction.splitstring(action)
            action = actions.GameAction()
            action.set_values_from_string(str1)
            allactions = []
            allactions.append(action)
            if str2:
                action = actions.GameAction()
                action.set_values_from_string(str2)
                allactions.append(action)
            for action in allactions:
                self.add_logical(action)

    def add_logical(self, action):
        self._current_actions.append(action)
        if isinstance(action, GameAction):
            who, was_score = action.is_scoring()
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

        if isinstance(action, SpecialActions.Substitute):
            who = action.team_
            field = self.court.fields[int(who)].players
            pos = action.position_in - 1
            fpos = field[:pos]
            fpos.append(Player(action.player_in))
            self.court.fields[int(who)].players = fpos + field[pos + 1 :]

        if isinstance(action, SpecialActions.Endset):
            self.score[0] = 0
            self.score[1] = 0

        if isinstance(action, SpecialActions.Rotation):
            self.court.rotate(int(action.team_))

        if isinstance(action, SpecialActions.SetServingTeam):
            self._last_serve = action.team_
        if isinstance(action, SpecialActions.Point):
            self.score[int(action.team_)] += action.value
        self.flush_actions()

    def flush_actions(self):
        self.rallies.append(
            (
                copy.deepcopy(self._current_actions),
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
