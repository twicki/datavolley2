from datavolley2.statistics.Actions import Gameaction
from typing import List, Any, Dict


def compare_action_to_string(action_string: str, filter_string: str) -> bool:
    """compares the action to the given input string
    the string is formatted
    [Team][2-Digit Player Number][Action][Quality]
    """
    # assert len(action_string) == len(filter_string)
    # for i in range(len(filter_string)):
    #     if filter_string[i] != "@" and action_string[i] != filter_string[i]:
    #         return False
    for filter_char, action_char in zip(filter_string, action_string):
        if filter_char != "@" and action_char != filter_char:
            return False
    return True


def compare_field_to_string(field, string):
    """compares the field to the given input string
    the string is formatted
    [2-Digit-Number P1][2-Digit-Number P2][2-Digit-Number P3][2-Digit-Number P4][2-Digit-Number P5][2-Digit-Number P6]
    """
    for i in range(1, 13, 2):
        if (
            string[i + 1] != "@"
            and int(string[i : i + 2]) != field.players[int((i - 1) / 2)].Number
        ):
            return False
    return True


def compare_court_to_string(court, string):
    """compares the court of a rally to the given input string
    the string is formatted
    [Team][2-Digit-Number P1][2-Digit-Number P2][2-Digit-Number P3][2-Digit-Number P4][2-Digit-Number P5][2-Digit-Number P6]
    """
    if string[0] != "/":
        if not compare_field_to_string(court.fields[0], string):
            return False
    if string[0] != "*":
        if not compare_field_to_string(court.fields[1], string):
            return False
    return True


def compare_ralley_to_string(string, ralley):
    """compares the rally to the given input string
    the string is formatted [ScoreHMin][ScoreHMax][ScoreGMin][ScoreGMax][SetScoreH][SetScoreG][SetScoreTotal][HomeServe]
    """
    # scores
    if string[0] != "@" and int(string[0]) > ralley[2][0]:
        return False
    if string[1] != "@" and int(string[1]) < ralley[2][0]:
        return False
    if string[2] != "@" and int(string[2]) > ralley[2][1]:
        return False
    if string[3] != "@" and int(string[3]) < ralley[2][1]:
        return False
    # sets:
    if string[4] != "@" and int(string[4]) != ralley[3][0]:
        return False
    if string[5] != "@" and int(string[5]) != ralley[3][1]:
        return False
    if string[6] != "@" and int(string[6]) != ralley[3][1] + ralley[3][0]:
        return False
    # serving
    if string[7] != "@" and str(ralley[4]) != string[7]:
        return False
    return True


def action_filter_from_string(filter_string: str, rallies):
    """ filters actions form a set of rallies"""
    specific_actions = []
    for rally in rallies:
        for action in rally[0]:
            if isinstance(action, Gameaction):
                current_action = str(action)
                if compare_action_to_string(current_action, filter_string):
                    specific_actions.append(action)

    return specific_actions


def ralley_filter_from_string(filter_string: str, rallies) -> List:
    """ filters a subset of rallies form a set of rallies based on the score"""
    specific_rallies = []
    for ralley in rallies:
        if compare_ralley_to_string(filter_string, ralley):
            specific_rallies.append(ralley)
    return specific_rallies


def court_filter(filter_string: str, rallies) -> List[Any]:
    """ filters a subset of rallies form a set of rallies based on the court"""
    specific_rallies = []
    for rally in rallies:
        if compare_court_to_string(rally[1], filter_string):
            specific_rallies.append(rally)
    return specific_rallies


def rally_filter_from_action_string(filter_string: str, rallies) -> List:
    """ filters rallies based on an action that needs to be in that rally"""
    specific_rallies = []
    for rally in rallies:
        for action in rally[0]:
            if isinstance(action, Gameaction):
                current_action = str(action)
                if compare_action_to_string(current_action, filter_string):
                    specific_rallies.append(rally)
                    break
    return specific_rallies