from tvrscouting.utils.errors import TVRSyntaxError


def set_team(user_string, returnvalue):
    if user_string[0] == "/":
        returnvalue = user_string[0] + returnvalue[1:]
        user_string = user_string[1:]
        return returnvalue, user_string, True
    elif user_string[0] == "*":
        returnvalue = user_string[0] + returnvalue[1:]
        user_string = user_string[1:]
        return returnvalue, user_string, True
    else:
        return returnvalue, user_string, False


def set_number(user_string, returnvalue):
    if len(user_string) > 1 and user_string[1].isnumeric():
        number = int(user_string[0:2])
        returnvalue = returnvalue[0] + str(user_string[0:2]) + returnvalue[3:]
        user_string = user_string[2:]
    else:
        returnvalue = returnvalue[0] + "0" + str(user_string[0]) + returnvalue[3:]
        user_string = user_string[1:]
    return returnvalue, user_string


def set_action(user_string, returnvalue):
    if len(user_string):
        if user_string[0] in ["e", "h", "b", "s", "r", "d"]:
            returnvalue = returnvalue[:3] + user_string[0] + returnvalue[4:]
            user_string = user_string[1:]
            return returnvalue, user_string, True

    return returnvalue, user_string, False


def set_quality(user_string, returnvalue):
    if len(user_string):
        if user_string[0] in ["#", "+", "-", "=", "p", "o"]:
            returnvalue = returnvalue[:4] + user_string[0] + returnvalue[5:]
            user_string = user_string[1:]
            return returnvalue, user_string, True
    return returnvalue, user_string, False


def set_combination(user_string, returnvalue):
    if len(user_string) > 1:
        if user_string[0] in ["D", "X", "C", "V"]:
            returnvalue = returnvalue[:5] + user_string[0:2] + returnvalue[7:]
            user_string = user_string[2:]
        return returnvalue, user_string
    return returnvalue, user_string


def set_from_direction(user_string, returnvalue):
    if len(user_string) and user_string[0].isnumeric():
        returnvalue = returnvalue[:7] + user_string[0] + returnvalue[8:]
        user_string = user_string[1:]
        return returnvalue, user_string, True
    return returnvalue, user_string, False


def set_to_direction(user_string, returnvalue):
    if len(user_string) and user_string[0].isnumeric():
        returnvalue = returnvalue[:8] + user_string[0] + returnvalue[9:]
        return returnvalue, True, user_string[1:]
    return returnvalue, False, user_string


def set_type(user_string, returnvalue):
    if len(user_string) and user_string[0] in ["T", "H", "Q", "L", "R", "A", "D"]:
        returnvalue = returnvalue[:10] + user_string[0] + returnvalue[11:]
        user_string = user_string[1:]
    return returnvalue, user_string


def set_players(user_string, returnvalue):
    players_set = False
    if len(user_string) and user_string[0].isnumeric():
        returnvalue = returnvalue[:11] + user_string[0] + returnvalue[12:]
        user_string = user_string[1:]
        players_set = True
    return returnvalue, user_string, players_set


def set_error_type(user_string, returnvalue):
    if len(user_string) and user_string[0] in ["S", "O", "N", "X", "B", "D"]:
        returnvalue = returnvalue[:12] + user_string[0] + returnvalue[13:]
        user_string = user_string[1:]
    return returnvalue, user_string


def set_extended_scout(user_string, returnvalue):
    players_set = False
    if len(user_string) and user_string[0] == ";":
        user_string = user_string[1:]
        returnvalue, user_string = set_type(user_string, returnvalue)
        returnvalue, user_string, players_set = set_players(user_string, returnvalue)
        returnvalue, user_string = set_error_type(user_string, returnvalue)
    return returnvalue, user_string, players_set


def expandString(user_string, was_compound=False):
    returnvalue = "*00h+D000;D9D"
    returnvalue, user_string, team_set = set_team(user_string, returnvalue)
    returnvalue, user_string = set_number(user_string, returnvalue)
    returnvalue, user_string, action_set = set_action(user_string, returnvalue)
    returnvalue, user_string, quality_set = set_quality(user_string, returnvalue)

    returnvalue, user_string = set_combination(user_string, returnvalue)
    returnvalue, user_string, from_direction_set = set_from_direction(user_string, returnvalue)
    returnvalue, to_directon_set, user_string = set_to_direction(user_string, returnvalue)
    if not quality_set:
        returnvalue, user_string, quality_set = set_quality(user_string, returnvalue)
    returnvalue, user_string, players_set = set_extended_scout(user_string, returnvalue)
    if len(user_string):
        raise TVRSyntaxError()
    return (
        returnvalue,
        team_set,
        action_set,
        quality_set,
        from_direction_set,
        to_directon_set,
        players_set,
    )
