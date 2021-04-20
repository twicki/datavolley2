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
        teams=[{}, {}],
    ):
        super().__init__()
        self.date = date
        self.time = time
        self.season = season
        self.league = league
        self.phase = phase
        self.refs = refs
        self.spectators = spectators
        self.city = city
        self.hall = hall
        self.teams = teams
        self.matchnumber = matchnumber
