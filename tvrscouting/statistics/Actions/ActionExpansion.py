import json
import os
from typing import Dict, List

from tvrscouting.statistics.Actions import GameAction
from tvrscouting.utils.errors import TVRSyntaxError


class StatementSettings:
    def __init__(self) -> None:
        self.compounds: Dict[str, List[str, int]] = {}
        self.quality: Dict[str, str] = {}
        self.zones: Dict[str, int] = {}
        self.zone_type: str = ""
        self.defaults: Dict[str, str] = {}
        self.load_settings()

    def load_settings(self) -> None:
        STORED_DATA_PATH = os.path.join(
            os.path.dirname(
                (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            ),
            ".persistent/",
        )
        with open(os.path.join(STORED_DATA_PATH, "settings.json"), "r") as f:
            data = json.load(f)
            self.compounds = data["compounds"]
            self.quality = data["quality"]
            self.zones = data["starting_zones"]
            self.zone_type = data["zone_type"]
            self.defaults = data["defaults"]

    def generate_default_string(self) -> str:
        return (
            self.defaults["team"]
            + "00"
            + self.defaults["action"]
            + self.quality[self.defaults["action"]]
            + self.defaults["combination"]
            + self.defaults["from"]
            + self.defaults["to"]
            + ";"
            + self.defaults["type"]
            + self.defaults["players"]
            + self.defaults["error_type"]
            + self.zone_type
        )

    def compound_team(self, action_string: str) -> GameAction.Team:
        if self.compounds[action_string[3]][1] == 1:
            return GameAction.Team.inverse(GameAction.Team.from_string(action_string[0]))
        else:
            return GameAction.Team.from_string(action_string[0])

    def compound_action(self, action_string: str) -> GameAction.Action:
        return GameAction.Action.from_string(self.compounds[action_string[3]][0])


def set_team(user_string: str, returnvalue: str):
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


def set_number(user_string: str, returnvalue: str):
    if len(user_string) > 1 and user_string[1].isnumeric():
        number = int(user_string[0:2])
        returnvalue = returnvalue[0] + str(user_string[0:2]) + returnvalue[3:]
        user_string = user_string[2:]
    else:
        returnvalue = returnvalue[0] + "0" + str(user_string[0]) + returnvalue[3:]
        user_string = user_string[1:]
    return returnvalue, user_string


def set_action(user_string: str, returnvalue: str):
    if len(user_string):
        if user_string[0] in ["e", "h", "b", "s", "r", "d", "f"]:
            returnvalue = returnvalue[:3] + user_string[0] + returnvalue[4:]
            user_string = user_string[1:]
            return returnvalue, user_string, True

    return returnvalue, user_string, False


def set_quality(user_string: str, returnvalue: str, settings: StatementSettings):
    default_quality = settings.quality[returnvalue[3]]
    returnvalue = returnvalue[:4] + default_quality + returnvalue[5:]
    if len(user_string):
        if user_string[0] in ["#", "+", "-", "=", "p", "o"]:
            returnvalue = returnvalue[:4] + user_string[0] + returnvalue[5:]
            user_string = user_string[1:]
            return returnvalue, user_string, True
    return returnvalue, user_string, False


def set_combination(user_string: str, returnvalue: str):
    if len(user_string) > 1:
        if user_string[0] in ["D", "X", "C", "V"]:
            returnvalue = returnvalue[:5] + user_string[0:2] + returnvalue[7:]
            user_string = user_string[2:]
        return returnvalue, user_string
    return returnvalue, user_string


def set_from_direction(user_string: str, returnvalue: str, settings: StatementSettings):
    if returnvalue[5:7] in settings.zones:
        returnvalue = returnvalue[:7] + str(settings.zones[returnvalue[5:7]]) + returnvalue[8:]
        return returnvalue, user_string, True
    elif len(user_string) and user_string[0].isnumeric():
        returnvalue = returnvalue[:7] + user_string[0] + returnvalue[8:]
        user_string = user_string[1:]
        return returnvalue, user_string, True
    return returnvalue, user_string, False


def set_to_direction(user_string: str, returnvalue: str):
    if len(user_string) and user_string[0].isnumeric():
        returnvalue = returnvalue[:8] + user_string[0] + returnvalue[9:]
        return returnvalue, True, user_string[1:]
    return returnvalue, False, user_string


def set_type(user_string: str, returnvalue: str):
    if len(user_string) and user_string[0] in ["T", "H", "Q", "L", "R", "A", "D"]:
        returnvalue = returnvalue[:10] + user_string[0] + returnvalue[11:]
        user_string = user_string[1:]
    return returnvalue, user_string


def set_players(user_string: str, returnvalue: str):
    players_set = False
    if len(user_string) and user_string[0].isnumeric():
        returnvalue = returnvalue[:11] + user_string[0] + returnvalue[12:]
        user_string = user_string[1:]
        players_set = True
    return returnvalue, user_string, players_set


def set_error_type(user_string: str, returnvalue: str):
    if len(user_string) and user_string[0] in ["S", "O", "N", "X", "B", "D"]:
        returnvalue = returnvalue[:12] + user_string[0] + returnvalue[13:]
        user_string = user_string[1:]
    return returnvalue, user_string


def set_direction_type(user_string: str, returnvalue: str):
    if len(user_string):
        if user_string[0] in ["c", "z"]:
            returnvalue = returnvalue[:13] + user_string[0] + returnvalue[14:]
        user_string = user_string[1:]
        return returnvalue, user_string
    return returnvalue, user_string


def set_extended_scout(user_string: str, returnvalue: str):
    players_set = False
    if len(user_string) and user_string[0] == ";":
        user_string = user_string[1:]
        returnvalue, user_string = set_type(user_string, returnvalue)
        returnvalue, user_string, players_set = set_players(user_string, returnvalue)
        returnvalue, user_string = set_error_type(user_string, returnvalue)
        returnvalue, user_string = set_direction_type(user_string, returnvalue)
    return returnvalue, user_string, players_set


def correct_zone_type(returnvalue: str):
    if returnvalue[3] != "h":
        returnvalue = returnvalue[:13] + "z" + returnvalue[14:]
    return returnvalue


def expandString(user_string: str, settings: StatementSettings):
    returnvalue = settings.generate_default_string()  # "*00h+D000;D9Dc"
    returnvalue, user_string, team_set = set_team(user_string, returnvalue)
    returnvalue, user_string = set_number(user_string, returnvalue)
    returnvalue, user_string, action_set = set_action(user_string, returnvalue)
    returnvalue, user_string, quality_set = set_quality(user_string, returnvalue, settings)

    returnvalue, user_string = set_combination(user_string, returnvalue)
    returnvalue, user_string, from_direction_set = set_from_direction(
        user_string, returnvalue, settings
    )
    returnvalue, to_directon_set, user_string = set_to_direction(user_string, returnvalue)
    if not quality_set:
        returnvalue, user_string, quality_set = set_quality(user_string, returnvalue, settings)
    returnvalue, user_string, players_set = set_extended_scout(user_string, returnvalue)

    returnvalue = correct_zone_type(returnvalue)
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
