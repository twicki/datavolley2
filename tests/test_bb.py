import datavolley2

import datavolley2.statistics as stats
import datavolley2.statistics.Actions as actions

# gs = stats.GameState()

team = stats.Team.from_string("*")
gs = stats.GameState()

# action = stats.Actions.Substitute(actions.Team("*"), 1, 1)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("*"), 2, 2)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("*"), 3, 3)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("*"), 4, 4)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("*"), 5, 5)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("*"), 6, 6)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("/"), 10, 1)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("/"), 11, 2)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("/"), 12, 3)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("/"), 13, 4)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("/"), 14, 5)
# gs.add_logical(action)
# action = stats.Actions.Substitute(actions.Team("/"), 15, 6)
# gs.add_logical(action)


# # str1, str2 = actions.GameAction.splitstring("1.2")
# # action = actions.GameAction()
# # action.set_values_from_string(str1)
# # allactions.append(action)
# # if str2:
# #     action = actions.GameAction()
# #     action.set_values_from_string(str2)
# #     allactions.append(action)
# # for action in allactions:
# #     gs.add_logical(action)
# # print(gs)

# action3 = stats.Actions.Rotation(actions.Team("*"))
# action3.team_ = actions.Team("*")
# gs.add_logical(action3)
# print(gs)

# allactions = []
# str1, str2 = actions.GameAction.splitstring("1#")
# action = actions.GameAction()
# action.set_values_from_string(str1)
# allactions.append(action)
# if str2:
#     action = actions.GameAction()
#     action.set_values_from_string(str2)
#     allactions.append(action)
# for action in allactions:
#     gs.add_logical(action)
# print(gs)
gs.add_string("*serve")
gs.add_string("*sub 10 1")
gs.add_string("*sub 11 2")
gs.add_string("*sub 12 3")
gs.add_string("*sub 13 4")
gs.add_string("*sub 14 5")
gs.add_string("*sub 15 6")

gs.add_string("/sub 1 1")
gs.add_string("/sub 2 2")
gs.add_string("/sub 3 3")
gs.add_string("/sub 4 4")
gs.add_string("/sub 5 5")
gs.add_string("/sub 6 6")
gs.add_string("10s#")
gs.add_string("10s.1")
gs.add_string("/1#")
gs.add_string("/sub 22 5")
gs.add_string("*team schoenenwerd")
gs.add_string("/team jona")
print(gs)
