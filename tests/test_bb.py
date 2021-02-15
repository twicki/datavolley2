import datavolley2

import datavolley2.statistics as stats
import datavolley2.statistics.Actions as actions

from datavolley2.statistics.Gamestate.game_state import (
    expandString,
    split_string,
    Player,
)

gs = stats.GameState()


gs.add_string("*team!schoenenwerd")
gs.add_string("/team!jona")
gs.add_string("/player!2!tobias2!u")
gs.add_string("/player!5!tobias5!o")
gs.add_string("/player!3!tobias3!s")
gs.add_string("/player!4!tobias4!d")
gs.add_string("/player!6!tobias7!o")
gs.add_string("/player!9!tobias!m")

gs.add_string("*serve")
gs.add_string("*sub!10!1")
gs.add_string("*sub!11!2")
gs.add_string("*sub!12!3")
gs.add_string("*sub!13!4")
gs.add_string("*sub!14!5")
gs.add_string("*sub!15!6")

gs.add_string("/sub!1!1")
gs.add_string("/sub!2!2")
gs.add_string("/sub!3!3")
gs.add_string("/sub!4!4")
gs.add_string("/sub!5!5")
gs.add_string("/sub!6!6")

gs.add_string("3.5#")

gs.add_string("3.3#")
gs.add_string("/4#")
out = gs.collect_stats("/")
print(gs)
