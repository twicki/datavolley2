#!/usr/bin/env python3
import datavolley2
import datavolley2.statistics as stats
from datavolley2.statistics.Actions import Team
import datavolley2.statistics.Gamestate.game_state as gs
from datavolley2.statistics.Actions.GameAction import Gameaction
from typing import List, Any, Dict

from jinja2 import Environment, FileSystemLoader


def string_match(action_string: str, filter_string: str) -> bool:
    assert len(action_string) == len(filter_string)
    for i in range(len(filter_string)):
        if filter_string[i] != "@" and action_string[i] != filter_string[i]:
            return False
    return True


def field_compare(field, string):
    for i in range(1, 13, 2):
        if (
            string[i + 1] != "@"
            and int(string[i : i + 2]) != field.players[int((i - 1) / 2)].Number
        ):
            return False
    return True


def court_compare(court, string):
    if string[0] != "/":
        if not field_compare(court.fields[0], string):
            return False
    if string[0] != "*":
        if not field_compare(court.fields[1], string):
            return False
    return True


def ralley_compare(ralley, string):
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


class StaticWriter:
    """
    writes out the datavolley-like file
    """

    ## all the required information to fill out the template
    global_info = {}
    scores = {}
    playerstats = {}
    teamstats = {}
    detailed_infos = {}

    gamestate: stats.GameState

    def __init__(self, game_state: stats.GameState):
        super().__init__()
        self.gamestate = game_state

    def action_filter(self, filter_string: str, rallies=None) -> List[Any]:
        if rallies is None:
            rallies = self.gamestate.rallies
        retval = []
        for ralley in rallies:
            for action in ralley[0]:
                if isinstance(action, stats.Gameaction):
                    current_action = str(action)
                    if string_match(current_action, filter_string):
                        retval.append(action)

        return retval

    def ralley_filter(self, filter_string: str, rallies=None) -> List[Any]:
        if rallies is None:
            rallies = self.gamestate.rallies
        retval = []
        for ralley in rallies:
            if ralley_compare(ralley, filter_string):
                retval.append(ralley)
        return retval

    def court_filter(self, filter_string: str, rallies=None) -> List[Any]:
        if rallies is None:
            rallies = self.gamestate.rallies
        retval = []
        for ralley in rallies:
            if court_compare(ralley[1], filter_string):
                retval.append(ralley)
        return retval

    def fill_scores(self) -> None:
        partialscores = []
        intermediates = [8, 16, 21]
        intermediate = intermediates[0]
        for rally in self.gamestate.rallies:
            setnumber = rally[3][0] + rally[3][1] + 1
            if len(partialscores) < setnumber:
                partialscores.append({"finalscore": [], "mid_results": []})

            if rally[2][0] == intermediate or rally[2][1] == intermediate:
                partialscores[setnumber - 1]["mid_results"].append(rally[2])
                try:
                    intermediate = intermediates[intermediates.index(intermediate) + 1]
                except IndexError:
                    intermediate = intermediates[0]
            if rally[2][0] == 25 or rally[2][1] == 25:
                partialscores[setnumber - 1]["finalscore"] = rally[2]
        last = self.gamestate.score
        if last[0] != 25 and last[1] != 25 and (last[0] != 0 and last[1] != 0):
            setnumber = self.gamestate.set_score[0] + self.gamestate.set_score[1] + 1
            partialscores[setnumber - 1]["finalscore"] = last

        # get final score
        home_total = 0
        away_total = 0
        for scores in partialscores:
            home_total += scores["finalscore"][0]
            away_total += scores["finalscore"][1]

        self.scores["set_score"] = {
            "home": self.gamestate.set_score[0],
            "guest": self.gamestate.set_score[1],
        }
        self.scores["final_score"] = {}
        self.scores["final_score"]["duration"] = -1
        self.scores["final_score"]["score"] = {
            "home": home_total,
            "guest": away_total,
        }
        self.scores["setresults"] = []
        for i in range(len(partialscores)):
            self.scores["setresults"].append(
                {
                    "setnumber": i + 1,
                    "time": -1,
                    "finalresult": {
                        "home": partialscores[i]["finalscore"][0],
                        "guest": partialscores[i]["finalscore"][1],
                    },
                    "results": [],
                }
            )
            for j in range(3):
                if len(partialscores[i]["mid_results"]) > j:
                    self.scores["setresults"][i]["results"].append(
                        {
                            "home": partialscores[i]["mid_results"][j][0],
                            "guest": partialscores[i]["mid_results"][j][1],
                        }
                    )
                else:
                    self.scores["setresults"][i]["results"].append(
                        {
                            "home": ".",
                            "guest": ".",
                        }
                    )

    def fill_global_info(self):
        self.global_info["teamnames"] = {
            "home": self.gamestate.teamnames[0],
            "guest": self.gamestate.teamnames[1],
        }
        # TODO: this info is not stored
        self.global_info["coaches"] = {
            "home": {"HC": "Some Name", "AC": "Another Name"},
            "guest": {"HC": "Some Name", "AC": "Another Name"},
        }

    def fill_team_stats(self):
        self.teamstats = {
            "home": {
                "Total": {},
                "Per_set": [],
            },
            "guest": {
                "Total": {},
                "Per_set": [],
            },
        }

        self.teamstats["home"]["Total"] = self.collect_stats_from_number(
            Team.from_string("*"), "@@"
        )
        self.teamstats["guest"]["Total"] = self.collect_stats_from_number(
            Team.from_string("/"), "@@"
        )

        number_of_sets = self.gamestate.set_score[0] + self.gamestate.set_score[1]
        if self.gamestate.score[0] + self.gamestate.score[1] != 0:
            number_of_sets += 1
        for i in range(number_of_sets):

            ralley_filter_string = "@@@@@@" + str(i) + "@"
            current_rallies = self.ralley_filter(ralley_filter_string)
            setstat_home = self.collect_stats_from_number(
                Team.from_string("*"), "@@", current_rallies
            )
            setstat_home["setnumber"] = i + 1
            setstat_home["SABO"] = {
                "serve": setstat_home["Serve"]["Points"],
                "attack": setstat_home["Attack"]["Points"],
                "block": setstat_home["Blocks"],
                "errors": len(self.action_filter("/@@@=", current_rallies)),
            }
            self.teamstats["home"]["Per_set"].append(setstat_home)

            setstat_guest = self.collect_stats_from_number(
                Team.from_string("/"), "@@", current_rallies
            )
            setstat_guest["setnumber"] = i + 1
            setstat_guest["SABO"] = {
                "serve": setstat_guest["Serve"]["Points"],
                "attack": setstat_guest["Attack"]["Points"],
                "block": setstat_guest["Blocks"],
                "errors": len(self.action_filter("*@@@=", current_rallies)),
            }
            self.teamstats["guest"]["Per_set"].append(setstat_guest)

    def fill_player_stats(self) -> None:
        self.playerstats["home"] = []
        self.playerstats["guest"] = []
        for team, name in [
            (Team.from_string("*"), "home"),
            (Team.from_string("/"), "guest"),
        ]:
            for player in self.gamestate.players[int(team)]:

                self.playerstats[name].append(
                    self.collect_individual_statistics(team, player)
                )
            for playerstat in self.playerstats[name]:
                if playerstat["Blocks"] == 0:
                    playerstat["Blocks"] == "."
                for k, v in playerstat["Attack"].items():
                    if v == 0:
                        playerstat["Attack"][k] = "."
                for k, v in playerstat["Reception"].items():
                    if v == 0:
                        playerstat["Reception"][k] = "."
                for k, v in playerstat["Serve"].items():
                    if v == 0:
                        playerstat["Serve"][k] = "."
                for k, v in playerstat["Points"].items():
                    if v == 0:
                        playerstat["Points"][k] = "."

    def fill_detailed_info(self):
        self.detailed_infos["home"] = {}
        self.detailed_infos["guest"] = {}
        for team, name in [
            (Team.from_string("*"), "home"),
            (Team.from_string("/"), "guest"),
        ]:
            self.detailed_infos[name]["plus_minus_rotations"] = []
            for position in [1, 2, 3, 4, 5, 6]:
                plus_minus = {}
                for player in self.gamestate.players[int(team)]:
                    if player.Position == gs.Player.PlayerPosition.Setter:
                        offset = position - 1
                        filter_string = (
                            str(team)
                            + ("@" * 2 * offset)
                            + "%02d" % player.Number
                            + ("@" * 2 * (5 - offset))
                        )
                        rallies = self.court_filter(filter_string)
                        points = self.collect_stats_from_number(team, "@@", rallies)[
                            "Points"
                        ]["Total"]
                        opponent_points = self.collect_stats_from_number(
                            Team.inverse(team), "@@", rallies
                        )["Points"]["Total"]
                        # TODO check if already there
                        if position in plus_minus:
                            plus_minus[position] += points - opponent_points
                        else:
                            plus_minus[position] = points - opponent_points
                self.detailed_infos[name]["plus_minus_rotations"].append(
                    (plus_minus[position], position)
                )
            # Number of sideout points
            rece_rallies = self.ralley_filter("@@@@@@@" + str(Team.inverse(team)))
            side_out_points = self.collect_stats_from_number(team, "@@", rece_rallies)[
                "Points"
            ]["Total"]
            self.detailed_infos[name]["SideOut"] = side_out_points

            total_rece = self.teamstats[name]["Total"]["Reception"]["Total"]
            self.detailed_infos[name]["Rece_per_point"] = "{:.2f}".format(
                (total_rece / side_out_points) if side_out_points > 0 else 0
            )

            # Number of break points
            serve_rallies = self.ralley_filter("@@@@@@@" + str(team))
            break_points = self.collect_stats_from_number(team, "@@", serve_rallies)[
                "Points"
            ]["Total"]
            self.detailed_infos[name]["Break_Points"] = break_points

            total_serve = self.teamstats[name]["Total"]["Serve"]["Total"]
            self.detailed_infos[name]["Serve_per_break"] = "{:.2f}".format(
                (total_serve / break_points if break_points > 0 else 0)
            )

            # TODO: we do not distinguish between k1 and k2 yet, so all mushed together
            self.detailed_infos[name]["K1_stats"] = {
                "positive": {},
                "negative": {},
            }
            rece_rallies = self.ralley_filter("@@@@@@@" + str(Team.inverse(team)))
            positive_rallies = []
            negative_rallies = []
            for ralley in rece_rallies:
                has_positive = len(self.action_filter("@@@r+", [ralley])) + len(
                    self.action_filter("@@@rp", [ralley])
                )
                if has_positive > 0:
                    positive_rallies.append(ralley)
                else:
                    negative_rallies.append(ralley)
            self.detailed_infos[name]["K1_stats"]["positive"]["Total"] = len(
                self.action_filter("@@@h@", positive_rallies)
            )
            self.detailed_infos[name]["K1_stats"]["positive"]["Error"] = len(
                self.action_filter("@@@h=", positive_rallies)
            )
            self.detailed_infos[name]["K1_stats"]["positive"]["Blocked"] = len(
                self.action_filter("@@@ho", positive_rallies)
            )
            self.detailed_infos[name]["K1_stats"]["positive"]["Points"] = len(
                self.action_filter("@@@h#", positive_rallies)
            )

            self.detailed_infos[name]["K1_stats"]["negative"]["Total"] = len(
                self.action_filter("@@@h@", negative_rallies)
            )
            self.detailed_infos[name]["K1_stats"]["negative"]["Error"] = len(
                self.action_filter("@@@h=", negative_rallies)
            )
            self.detailed_infos[name]["K1_stats"]["negative"]["Blocked"] = len(
                self.action_filter("@@@ho", negative_rallies)
            )
            self.detailed_infos[name]["K1_stats"]["negative"]["Points"] = len(
                self.action_filter("@@@h#", negative_rallies)
            )

            self.detailed_infos[name]["K2_stats"] = {
                "Error": -1,
                "Blocked": -1,
                "Points": -1,
                "Total": -1,
            }

    def collect_stats_from_number(
        self, team: Team, player_number: str, rallies=None
    ) -> Dict:
        fulldata = {}
        fulldata["Attack"] = {}
        filterstring = str(team) + player_number + "h" + "@"
        fulldata["Attack"]["Total"] = len(self.action_filter(filterstring, rallies))
        filterstring = str(team) + player_number + "h" + "#"
        fulldata["Attack"]["Points"] = len(self.action_filter(filterstring, rallies))
        filterstring = str(team) + player_number + "h" + "="
        fulldata["Attack"]["Error"] = len(self.action_filter(filterstring, rallies))
        filterstring = str(team) + player_number + "h" + "o"
        fulldata["Attack"]["Blocked"] = len(self.action_filter(filterstring, rallies))
        fulldata["Attack"]["Percentage"] = int(
            100
            * (
                (fulldata["Attack"]["Points"] / fulldata["Attack"]["Total"])
                if fulldata["Attack"]["Total"] > 0
                else 0
            )
        )

        fulldata["Blocks"] = {}
        filterstring = str(team) + player_number + "b" + "#"
        fulldata["Blocks"] = len(self.action_filter(filterstring, rallies))

        fulldata["Reception"] = {}
        filterstring = str(team) + player_number + "r" + "@"
        total_receptions = len(self.action_filter(filterstring, rallies))
        fulldata["Reception"]["Total"] = total_receptions
        filterstring = str(team) + player_number + "r" + "+"
        positive = len(self.action_filter(filterstring, rallies))
        filterstring = str(team) + player_number + "r" + "p"
        positive += len(self.action_filter(filterstring, rallies))
        fulldata["Reception"]["Positive"] = int(
            100 * (positive / total_receptions if total_receptions > 0 else 0)
        )
        filterstring = str(team) + player_number + "r" + "o"
        fulldata["Reception"]["Error"] = len(self.action_filter(filterstring, rallies))
        filterstring = str(team) + player_number + "r" + "p"
        fulldata["Reception"]["Perfect"] = int(
            100
            * (
                len(self.action_filter(filterstring, rallies)) / total_receptions
                if total_receptions > 0
                else 0
            )
        )

        fulldata["Serve"] = {}
        filterstring = str(team) + player_number + "s" + "@"
        fulldata["Serve"]["Total"] = len(self.action_filter(filterstring, rallies))
        filterstring = str(team) + player_number + "s" + "="
        fulldata["Serve"]["Error"] = len(self.action_filter(filterstring, rallies))
        filterstring = str(team) + player_number + "s" + "#"
        fulldata["Serve"]["Points"] = len(self.action_filter(filterstring, rallies))

        fulldata["Points"] = {}
        filterstring = str(team) + player_number + "@" + "#"
        total_points = len(self.action_filter(filterstring, rallies))
        fulldata["Points"]["Total"] = total_points
        filterstring = str(team) + player_number + "@" + "="
        total_errors = len(self.action_filter(filterstring, rallies))
        filterstring = str(team) + player_number + "@" + "o"
        total_errors += len(self.action_filter(filterstring, rallies))
        fulldata["Points"]["Plus_minus"] = total_points - total_errors

        # TODO: add this later
        fulldata["Points"]["BP"] = 0

        return fulldata

    def collect_individual_statistics(self, team: Team, player: gs.Player) -> Dict:
        player_number = "%02d" % player.Number
        fulldata = self.collect_stats_from_number(team, player_number)
        fulldata["Name"] = player.Name
        fulldata["Number"] = player.Number
        fulldata["Role"] = ""
        if player.is_capitain:
            fulldata["Role"] = "C"
        elif player.Position == gs.Player.PlayerPosition.Libera:
            fulldata["Role"] = "L"
        # TODO: find out the starts
        fulldata["Starts"] = [0, 0, 0, 0, 0]
        for rally in self.gamestate.rallies:
            setnumber = rally[3][0] + rally[3][1]
            if player.Position == gs.Player.PlayerPosition.Libera:
                for action in rally[0]:
                    if isinstance(action, Gameaction):
                        if action.player == player.Number:
                            fulldata["Starts"][setnumber] = -1
                            continue
            else:
                for i in range(6):
                    if player.Number == rally[1].fields[int(team)].players[i].Number:
                        if rally[2][0] + rally[2][1] == 0:
                            fulldata["Starts"][setnumber] = i + 1
                        elif fulldata["Starts"][setnumber] == 0:
                            fulldata["Starts"][setnumber] = -1

        return fulldata

    def analyze(self) -> None:
        self.fill_scores()
        self.fill_global_info()
        self.fill_team_stats()
        self.fill_player_stats()
        self.fill_detailed_info()

        file_loader = FileSystemLoader(
            "/home/tobiasw/Documents/Volley/playoff/datavolley2/datavolley2/analysis/template"
        )
        env = Environment(loader=file_loader)

        template = env.get_template("template.jinja2")

        output = template.render(
            scores=self.scores,
            global_info=self.global_info,
            playerstats=self.playerstats,
            teamstats=self.teamstats,
            detailed_infos=self.detailed_infos,
        )

        with open("template.tex", "w") as f:
            f.write(output)
            f.close()
