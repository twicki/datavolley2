import datavolley2

import datavolley2.statistics as stats
import datavolley2.statistics.Actions as actions

from datavolley2.statistics.Gamestate.game_state import (
    expandString,
    split_string,
    Player,
)


from datavolley2.analysis.static import StaticWriter

gs = stats.GameState()


gs.add_string("/1s#1.1-2")

print(sw.gamestate.score)