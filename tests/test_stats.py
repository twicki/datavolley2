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

gs.add_string("*player!3!Eiholzer!d")

gs.add_string("*sub!3!1")
gs.add_string("*serve")
gs.add_string("3s#")
gs.add_string("3s=")
gs.add_string("3#")
gs.add_string("3#")
gs.add_string("3#")
gs.add_string("3#")
gs.add_string("3#")
gs.add_string("3ho")
gs.add_string("3.5#")
gs.add_string("3=")
gs.add_string("/3.3#")

gs.add_string("/1s.3+")
gs.add_string("/1s#.3")
gs.add_string("/1s.3p")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")
gs.add_string("/1s#")


sw = StaticWriter(gs)

out = gs.collect_stats("/")

out = sw.court_filter("/@@@@@@@@@@@@")


out2 = sw.ralley_filter("03@@@@@@")
sw.analyze()

print(sw.gamestate.score)