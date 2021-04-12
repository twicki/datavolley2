from tvrscouting.statistics.Players.players import Team, Player
from .AbstractAction import AbstractAction


class Substitute(AbstractAction):
    player_in: int
    position_in: int

    def __init__(
        self,
        team: Team,
        player_in: int,
        position_in: int,
        time_stamp=None,
        auto_generated=False,
    ):
        super().__init__(time_stamp)
        self.team_ = team
        self.player_in = player_in
        self.position_in = position_in

    def __str__(self):
        return str(self.team_) + "sub!" + str(self.player_in) + "!" + str(self.position_in)


class Rotation(AbstractAction):
    team_: Team
    positive: bool

    def __init__(self, team: Team, direction: bool = True, time_stamp=None, auto_generated=False):
        super().__init__(time_stamp, auto_generated)
        self.team_ = team
        self.positive = direction

    def __str__(self):
        return str(self.team_) + "rota!" + str(int(self.positive)) + "!" + str(self.auto_generated)


class Point(AbstractAction):
    team_: Team
    value: int

    def __init__(self, team: Team, value: int = 1, time_stamp=None, auto_generated=False):
        super().__init__(time_stamp, auto_generated)
        self.team_ = team
        self.value = value

    def __str__(self):
        return str(self.team_) + "point" + "!" + str(self.auto_generated)


class Endset(AbstractAction):
    team_: Team

    def __init__(self, team: Team, time_stamp=None, auto_generated=False):
        super().__init__(time_stamp, auto_generated)
        self.team_ = team

    def __str__(self):
        return str(self.team_) + "endset" + "!" + str(self.auto_generated)


class SetServingTeam(AbstractAction):
    team_: Team

    def __init__(self, team: Team, time_stamp=None, auto_generated=False):
        super().__init__(time_stamp, auto_generated)
        self.team_ = team

    def __str__(self):
        return str(self.team_) + "serve" + "!" + str(self.auto_generated)


class SetSetter(AbstractAction):
    team_: Team

    def __init__(self, team: Team, setter_number: int = 1, time_stamp=None, auto_generated=False):
        super().__init__(time_stamp, auto_generated)
        self.team_ = team
        self.setter_number = setter_number

    def __str__(self):
        return (
            str(self.team_)
            + "setter"
            + "!"
            + str(self.setter_number)
            + "!"
            + str(self.auto_generated)
        )


class InitializePlayer(AbstractAction):
    team: Team
    number: int
    name: str
    position: Player.PlayerPosition

    def __init__(self, initialization_string: str, time_stamp=None):
        super().__init__(time_stamp)
        l = initialization_string.split("!")
        self.team = Team.from_string(l[0][0])
        self.number = int(l[1])
        self.name = l[2]
        self.position = Player.PlayerPosition.from_string(l[3])

    def __str__(self):
        return (
            str(self.team)
            + "player"
            + "!"
            + str(self.number)
            + "!"
            + self.name
            + "!"
            + str(self.position)
        )


class InitializeTeamName(AbstractAction):
    team: Team
    name: str

    def __init__(self, initialization_string: str, time_stamp=None):
        super().__init__(time_stamp)
        l = initialization_string.split("!")
        self.team = Team.from_string(l[0][0])
        self.name = l[1]

    def __str__(self):
        return str(self.team) + "team" + "!" + self.name
