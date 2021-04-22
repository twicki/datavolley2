from typing import List

from tvrscouting.organization.team_info import TeamInfo


class GameMetaInfo:
    def __init__(
        self,
        date="",
        time="",
        season="",
        league="",
        phase="",
        refs=[],
        spectators=0,
        city="",
        hall="",
        matchnumber=0,
        teams=[TeamInfo(), TeamInfo()],
    ):
        super().__init__()
        self.date: str = date
        self.time: str = time
        self.season: str = season
        self.league: str = league
        self.phase: str = phase
        self.refs: str = refs
        self.spectators: int = spectators
        self.city: str = city
        self.hall: str = hall
        self.teams: List[TeamInfo] = teams
        self.matchnumber: int = matchnumber
