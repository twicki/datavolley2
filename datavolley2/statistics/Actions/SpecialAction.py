from .GameAction import Team
from .AbstractAction import AbstractAction


class Substitute(AbstractAction):
    player_in: int
    position_in: int

    def __init__(self, team: Team, player_in: int, position_in: int, time_stamp=None):
        super().__init__(time_stamp)
        self.team_ = team
        self.player_in = player_in
        self.position_in = position_in

    def __str__(self):
        return (
            str(self.team_)
            + "Substitute "
            + str(self.player_in)
            + " "
            + str(self.position_in)
        )


class Rotation(AbstractAction):
    team_: Team
    positive: bool

    def __init__(self, team: Team, direction: bool = True, time_stamp=None):
        super().__init__(time_stamp)
        self.team_ = team
        self.positive = direction

    def __str__(self):
        return str(self.team_) + "Rotation " + str(int(self.positive))


class Point(AbstractAction):
    team_: Team
    value: int

    def __init__(self, team: Team, value: int = 1, time_stamp=None):
        super().__init__(time_stamp)
        self.team_ = team
        self.value = value

    def __str__(self):
        return str(self.team_) + "Point"


class Endset(AbstractAction):
    team_: Team

    def __init__(self, team: Team, time_stamp=None):
        super().__init__(time_stamp)
        self.team_ = team

    def __str__(self):
        return str(self.team_) + "EndSet"


class SetServingTeam(AbstractAction):
    team_: Team

    def __init__(self, team: Team, time_stamp=None):
        super().__init__(time_stamp)
        self.team_ = team

    def __str__(self):
        return str(self.team_) + "Serve"
