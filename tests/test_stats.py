import tvrscouting

import tvrscouting.statistics as stats
import tvrscouting.statistics.Actions as actions

from tvrscouting.statistics.Gamestate.game_state import (
    expandString,
    split_string,
    Player,
)


from tvrscouting.analysis.static import StaticWriter

gs = stats.GameState()


gs.add_string("/1s#1.1-2")

print(sw.gamestate.score)