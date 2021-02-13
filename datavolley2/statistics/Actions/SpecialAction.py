from .GameAction import Team


class Substitute:
    player_in: int
    position_in: int

    def __init__(self, team: Team, player_in: int, position_in: int):
        super().__init__()
        self.team_ = team
        self.player_in = player_in
        self.position_in = position_in


class Rotation:
    team_: Team
    positive: bool

    def __init__(self, team: Team, direction: bool = True):
        super().__init__()
        team_ = team
        positive = direction


class Point:
    team_: Team
    value: int

    def __init__(self, team: Team, value: int = 1):
        super().__init__()
        self.team_ = team
        self.value = value


class Endset:
    team_: Team

    def __init__(self, team: Team):
        super().__init__()
        self.team_ = team


class SetServingTeam:
    team_: Team

    def __init__(self, team: Team):
        super().__init__()
        self.team_ = team
