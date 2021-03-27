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
print(gs.score)