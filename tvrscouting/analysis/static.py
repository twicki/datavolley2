import sys
import os

import tvrscouting
import tvrscouting.statistics as stats
from tvrscouting.statistics.Players.players import Team, Player
import tvrscouting.statistics.Gamestate.game_state as gs
from tvrscouting.statistics.Actions.GameAction import Gameaction
from tvrscouting.analysis.filters import *

from tvrscouting.statistics.Actions.SpecialAction import Endset
from typing import List, Any, Dict

from jinja2 import Environment, FileSystemLoader


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

    def add_global_info(self, key: str, value: str):
        global_info[key] = value

    def add_coaches(self, team: str, position: str, name: str):
        global_info["coaches"][team] = name

    def fill_scores(self) -> None:
        partialscores = []
        start_times = []
        end_times = []
        intermediates = [8, 16, 21]
        intermediate = intermediates[0]
        for rally in self.gamestate.rallies:
            setnumber = rally[3][0] + rally[3][1] + 1
            if len(partialscores) < setnumber:
                partialscores.append({"finalscore": [], "mid_results": []})
                if setnumber == 5:
                    intermediates = [5, 10, 12]
                    intermediate = intermediates[0]
            if len(start_times) < setnumber:
                for action in rally[0]:
                    if action.time_stamp:
                        if isinstance(action, Gameaction):
                            start_times.append(action.time_stamp)
                            break
            if len(end_times) < setnumber:
                for action in rally[0]:
                    if isinstance(action, Endset):
                        end_times.append(action.time_stamp)
                        break

            if rally[2][0] == intermediate or rally[2][1] == intermediate:
                partialscores[setnumber - 1]["mid_results"].append(rally[2])
                try:
                    intermediate = intermediates[intermediates.index(intermediate) + 1]
                except IndexError:
                    intermediate = intermediates[0]
            # TODO: rename
            totalscore = 25 if rally[3][0] + rally[3][1] < 4 else 15
            if rally[2][0] == totalscore or rally[2][1] == totalscore:
                partialscores[setnumber - 1]["finalscore"] = rally[2]
        if len(start_times) != len(end_times):
            end_times.append(self.gamestate.rallies[-1][0][-1].time_stamp)
        last = self.gamestate.score
        if (
            last[0] != totalscore
            and last[1] != totalscore
            and (last[0] != 0 and last[1] != 0)
        ):
            setnumber = self.gamestate.set_score[0] + self.gamestate.set_score[1] + 1
            partialscores[setnumber - 1]["finalscore"] = last

        # get final score
        home_total = 0
        away_total = 0
        total_time = 0
        for score in partialscores:
            if len(score["finalscore"]) == 0:
                partialscores.remove(score)
        for scores in partialscores:
            home_total += scores["finalscore"][0]
            away_total += scores["finalscore"][1]

        self.scores["set_score"] = {
            "home": self.gamestate.set_score[0],
            "guest": self.gamestate.set_score[1],
        }
        self.scores["final_score"] = {}
        self.scores["final_score"]["score"] = {
            "home": home_total,
            "guest": away_total,
        }
        self.scores["setresults"] = []
        for i in range(len(partialscores)):
            if (
                len(start_times) > i
                and len(end_times) > i
                and start_times[i]
                and end_times[i]
            ):
                time = int((end_times[i] - start_times[i]) / 60.0)
                total_time += time
            else:
                time = ""
            self.scores["setresults"].append(
                {
                    "setnumber": i + 1,
                    "time": time,
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
        self.scores["final_score"]["duration"] = total_time if total_time > 0 else ""

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

            ralley_filter_string = "@@@@@@@@@@" + str(i) + "@"
            current_rallies = ralley_filter_from_string(
                ralley_filter_string, self.gamestate.rallies
            )
            setstat_home = self.collect_stats_from_number(
                Team.from_string("*"), "@@", current_rallies
            )
            setstat_home["setnumber"] = i + 1
            setstat_home["SABO"] = {
                "serve": setstat_home["Serve"]["Points"],
                "attack": setstat_home["Attack"]["Points"],
                "block": setstat_home["Blocks"],
                "errors": len(action_filter_from_string("/@@@=@@@@", current_rallies)),
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
                "errors": len(action_filter_from_string("*@@@=@@@@", current_rallies)),
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
                    playerstat["Blocks"] = "."
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
                    if player.Position == Player.PlayerPosition.Setter:
                        offset = position - 1
                        filter_string = (
                            str(team)
                            + ("@" * 2 * offset)
                            + "%02d" % player.Number
                            + ("@" * 2 * (5 - offset))
                        )
                        rallies = court_filter(filter_string, self.gamestate.rallies)
                        points = self.collect_stats_from_number(team, "@@", rallies)[
                            "Points"
                        ]["Total"]
                        opponent_points = self.collect_stats_from_number(
                            Team.inverse(team), "@@", rallies
                        )["Points"]["Total"]
                        if position in plus_minus:
                            plus_minus[position] += points - opponent_points
                        else:
                            plus_minus[position] = points - opponent_points
                self.detailed_infos[name]["plus_minus_rotations"].append(
                    (plus_minus[position], position)
                )
            # Number of sideout points
            rece_rallies = ralley_filter_from_string(
                "@@@@@@@@@@@" + str(Team.inverse(team)), self.gamestate.rallies
            )
            filterstring = str(team) + "@@@" + "#"
            side_out_points = len(action_filter_from_string(filterstring, rece_rallies))
            self.detailed_infos[name]["SideOut"] = side_out_points

            total_rece = self.teamstats[name]["Total"]["Reception"]["Total"]
            self.detailed_infos[name]["Rece_per_point"] = "{:.2f}".format(
                (total_rece / side_out_points) if side_out_points > 0 else 0
            )

            # Number of break points
            serve_rallies = ralley_filter_from_string(
                "@@@@@@@@@@@" + str(team), self.gamestate.rallies
            )
            filterstring = str(team) + "@@@" + "#"
            break_points = len(action_filter_from_string(filterstring, serve_rallies))
            self.detailed_infos[name]["Break_Points"] = break_points

            total_serve = self.teamstats[name]["Total"]["Serve"]["Total"]
            self.detailed_infos[name]["Serve_per_break"] = "{:.2f}".format(
                (total_serve / break_points if break_points > 0 else 0)
            )

            self.detailed_infos[name]["K1_stats"] = {
                "positive": {},
                "negative": {},
            }
            rece_rallies = ralley_filter_from_string(
                "@@@@@@@@@@@" + str(Team.inverse(team)), self.gamestate.rallies
            )
            positive_rallies = []
            negative_rallies = []
            for ralley in rece_rallies:
                has_positive = len(
                    action_filter_from_string("@@@r+@@@@", [ralley])
                ) + len(action_filter_from_string("@@@rp@@@@", [ralley]))
                if has_positive > 0:
                    positive_rallies.append(ralley)
                else:
                    negative_rallies.append(ralley)
            total_k1 = 0
            error_k1 = 0
            blocked_k1 = 0
            points_k1 = 0
            total_k2 = 0
            error_k2 = 0
            blocked_k2 = 0
            points_k2 = 0
            for ralley in positive_rallies:
                k1_found = False
                for action in ralley[0]:
                    if isinstance(action, Gameaction):
                        current_action = str(action)
                        if not k1_found:
                            if compare_action_to_string(
                                current_action, str(team) + "@@h@"
                            ):
                                total_k1 += 1
                                k1_found = True
                            if compare_action_to_string(
                                current_action, str(team) + "@@h="
                            ):
                                error_k1 += 1
                                k1_found = True
                            if compare_action_to_string(
                                current_action, str(team) + "@@ho"
                            ):
                                blocked_k1 += 1
                                k1_found = True
                            if compare_action_to_string(
                                current_action, str(team) + "@@h#"
                            ):
                                points_k1 += 1
                                k1_found = True
                        else:
                            if compare_action_to_string(
                                current_action, str(team) + "@@h@"
                            ):
                                total_k2 += 1
                            if compare_action_to_string(
                                current_action, str(team) + "@@h="
                            ):
                                error_k2 += 1
                            if compare_action_to_string(
                                current_action, str(team) + "@@ho"
                            ):
                                blocked_k2 += 1
                            if compare_action_to_string(
                                current_action, str(team) + "@@h#"
                            ):
                                points_k2 += 1

            self.detailed_infos[name]["K1_stats"]["positive"]["Total"] = total_k1
            self.detailed_infos[name]["K1_stats"]["positive"]["Error"] = error_k1
            self.detailed_infos[name]["K1_stats"]["positive"]["Blocked"] = blocked_k1
            self.detailed_infos[name]["K1_stats"]["positive"]["Points"] = int(
                100 * points_k1 / total_k1 if total_k1 > 0 else 0
            )

            total_k1 = 0
            error_k1 = 0
            blocked_k1 = 0
            points_k1 = 0
            for ralley in negative_rallies:
                k1_found = False
                for action in ralley[0]:
                    if isinstance(action, Gameaction):
                        current_action = str(action)
                        if not k1_found:
                            if compare_action_to_string(
                                current_action, str(team) + "@@h@"
                            ):
                                total_k1 += 1
                                k1_found = True
                            if compare_action_to_string(
                                current_action, str(team) + "@@h="
                            ):
                                error_k1 += 1
                                k1_found = True
                            if compare_action_to_string(
                                current_action, str(team) + "@@ho"
                            ):
                                blocked_k1 += 1
                                k1_found = True
                            if compare_action_to_string(
                                current_action, str(team) + "@@h#"
                            ):
                                points_k1 += 1
                                k1_found = True
                        else:
                            if compare_action_to_string(
                                current_action, str(team) + "@@h@"
                            ):
                                total_k2 += 1
                            if compare_action_to_string(
                                current_action, str(team) + "@@h="
                            ):
                                error_k2 += 1
                            if compare_action_to_string(
                                current_action, str(team) + "@@ho"
                            ):
                                blocked_k2 += 1
                            if compare_action_to_string(
                                current_action, str(team) + "@@h#"
                            ):
                                points_k2 += 1
            serve_rallies = ralley_filter_from_string(
                "@@@@@@@@@@@" + str(team), self.gamestate.rallies
            )
            for ralley in serve_rallies:
                for action in ralley[0]:
                    current_action = str(action)
                    if isinstance(action, Gameaction):
                        if compare_action_to_string(current_action, str(team) + "@@h@"):
                            total_k2 += 1
                        if compare_action_to_string(current_action, str(team) + "@@h="):
                            error_k2 += 1
                        if compare_action_to_string(current_action, str(team) + "@@ho"):
                            blocked_k2 += 1
                        if compare_action_to_string(current_action, str(team) + "@@h#"):
                            points_k2 += 1

            self.detailed_infos[name]["K1_stats"]["negative"]["Total"] = total_k1
            self.detailed_infos[name]["K1_stats"]["negative"]["Error"] = error_k1
            self.detailed_infos[name]["K1_stats"]["negative"]["Blocked"] = blocked_k1
            self.detailed_infos[name]["K1_stats"]["negative"]["Points"] = int(
                100 * points_k1 / total_k1 if total_k1 > 0 else 0
            )

            self.detailed_infos[name]["K2_stats"] = {
                "Error": error_k2,
                "Blocked": blocked_k2,
                "Points": int(100 * points_k2 / total_k2 if total_k2 > 0 else 0),
                "Total": total_k2,
            }

    def collect_stats_from_number(
        self, team: Team, player_number: str, rallies=None
    ) -> Dict:
        rallies = self.gamestate.rallies if rallies is None else rallies
        fulldata = {}
        fulldata["Attack"] = {}
        filterstring = str(team) + player_number + "h" + "@@@@@"
        fulldata["Attack"]["Total"] = len(
            action_filter_from_string(filterstring, rallies)
        )
        filterstring = str(team) + player_number + "h" + "#@@@@"
        fulldata["Attack"]["Points"] = len(
            action_filter_from_string(filterstring, rallies)
        )
        filterstring = str(team) + player_number + "h" + "=@@@@"
        fulldata["Attack"]["Error"] = len(
            action_filter_from_string(filterstring, rallies)
        )
        filterstring = str(team) + player_number + "h" + "o@@@@"
        fulldata["Attack"]["Blocked"] = len(
            action_filter_from_string(filterstring, rallies)
        )
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
        fulldata["Blocks"] = len(action_filter_from_string(filterstring, rallies))

        fulldata["Reception"] = {}
        filterstring = str(team) + player_number + "r" + "@"
        total_receptions = len(action_filter_from_string(filterstring, rallies))
        fulldata["Reception"]["Total"] = total_receptions
        filterstring = str(team) + player_number + "r" + "+"
        positive = len(action_filter_from_string(filterstring, rallies))
        filterstring = str(team) + player_number + "r" + "p"
        positive += len(action_filter_from_string(filterstring, rallies))
        fulldata["Reception"]["Positive"] = int(
            100 * (positive / total_receptions if total_receptions > 0 else 0)
        )
        filterstring = str(team) + player_number + "r" + "o"
        fulldata["Reception"]["Error"] = len(
            action_filter_from_string(filterstring, rallies)
        )
        filterstring = str(team) + player_number + "r" + "p"
        fulldata["Reception"]["Perfect"] = int(
            100
            * (
                len(action_filter_from_string(filterstring, rallies)) / total_receptions
                if total_receptions > 0
                else 0
            )
        )

        fulldata["Serve"] = {}
        filterstring = str(team) + player_number + "s" + "@"
        fulldata["Serve"]["Total"] = len(
            action_filter_from_string(filterstring, rallies)
        )
        filterstring = str(team) + player_number + "s" + "="
        fulldata["Serve"]["Error"] = len(
            action_filter_from_string(filterstring, rallies)
        )
        filterstring = str(team) + player_number + "s" + "#"
        fulldata["Serve"]["Points"] = len(
            action_filter_from_string(filterstring, rallies)
        )

        fulldata["Points"] = {}
        filterstring = str(team) + player_number + "@" + "#"
        total_points = len(action_filter_from_string(filterstring, rallies))
        fulldata["Points"]["Total"] = total_points
        filterstring = str(team) + player_number + "@" + "="
        total_errors = len(action_filter_from_string(filterstring, rallies))
        filterstring = str(team) + player_number + "@" + "o"
        total_errors += len(action_filter_from_string(filterstring, rallies))
        fulldata["Points"]["Plus_minus"] = total_points - total_errors

        break_rallies = ralley_filter_from_string(
            "@@@@@@@@@@@" + str(team), self.gamestate.rallies
        )
        filterstring = str(team) + player_number + "@#"
        fulldata["Points"]["BP"] = len(
            action_filter_from_string(filterstring, break_rallies)
        )
        return fulldata

    def compute_vote(self, team: Team, player_number: Player, fulldata: Dict) -> float:
        # here is the vote computation that we're never using
        votes = 0
        vote = 0
        filterstring = str(team) + "@@" + "s" + "@"
        total_serves = len(
            action_filter_from_string(filterstring, self.gamestate.rallies)
        )
        if fulldata["Serve"]["Total"] / total_serves > 0.05:
            filterstring = str(team) + player_number + "s" + "p"
            serve_overs = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            filterstring = str(team) + player_number + "s" + "+"
            serve_plus = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            filterstring = str(team) + player_number + "s" + "-"
            serve_minus = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            serve_vote = (
                fulldata["Serve"]["Points"] * 10
                + serve_overs * 8
                + serve_plus * 7
                + serve_minus * 4
            ) / fulldata["Serve"]["Total"]
            vote += serve_vote if serve_vote > 5.5 else 5.5
            votes += 1

        filterstring = str(team) + "@@" + "r" + "@"
        total_receptions = len(
            action_filter_from_string(filterstring, self.gamestate.rallies)
        )
        if fulldata["Reception"]["Total"] / total_serves > 0.07:
            filterstring = str(team) + player_number + "r" + "p"
            perfect = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            filterstring = str(team) + player_number + "r" + "+"
            positive = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            filterstring = str(team) + player_number + "r" + "-"
            negative = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            filterstring = str(team) + player_number + "r" + "o"
            errors = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            rece_vote = (
                perfect * 10 + positive * 7 + negative * -1 + errors * -3
            ) / fulldata["Reception"]["Total"]
            vote += rece_vote if rece_vote > 5.5 else 5.5
            votes += 1

        filterstring = str(team) + "@@" + "h" + "@"
        total_hits = len(
            action_filter_from_string(filterstring, self.gamestate.rallies)
        )
        if fulldata["Attack"]["Total"] / total_hits > 0.07:
            filterstring = str(team) + player_number + "h" + "#"
            kills = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            filterstring = str(team) + player_number + "r" + "+"
            positive = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            filterstring = str(team) + player_number + "r" + "-"
            negative = len(
                action_filter_from_string(filterstring, self.gamestate.rallies)
            )
            hit_vote = (kills * 10 + positive * 5 + negative * 5) / fulldata["Attack"][
                "Total"
            ]
            vote += hit_vote if hit_vote > 5.5 else 5.5
            votes += 1

        sets_played = 0
        for start in fulldata["Starts"]:
            if start != 0:
                sets_played += 1
        blocks_per_set = fulldata["Blocks"] / sets_played
        if blocks_per_set > 1:
            vote += 8.5
            votes += 1
        elif blocks_per_set > 0.8:
            vote += 8
            votes += 1
        elif blocks_per_set > 0.5:
            vote += 7
            votes += 1

        return round(vote / votes, 1) if votes > 0 else "."

    def collect_individual_statistics(self, team: Team, player: Player) -> Dict:
        player_number = "%02d" % player.Number
        fulldata = self.collect_stats_from_number(team, player_number)
        fulldata["Name"] = player.Name
        fulldata["Number"] = player.Number
        fulldata["Role"] = ""
        fulldata["IsSetter"] = player.PlayerPosition.Setter == player.Position
        if player.is_capitain:
            fulldata["Role"] = "C"
        elif player.Position == Player.PlayerPosition.Libera:
            fulldata["Role"] = "L"
        fulldata["Starts"] = [0, 0, 0, 0, 0]
        for rally in self.gamestate.rallies:
            setnumber = rally[3][0] + rally[3][1]
            if player.Position == Player.PlayerPosition.Libera:
                for action in rally[0]:
                    if isinstance(action, Gameaction):
                        if action.player == player.Number and action.team == team:
                            fulldata["Starts"][setnumber] = -1
                            continue
            else:
                for i in range(6):
                    if player.Number == rally[1].fields[int(team)].players[i].Number:
                        if rally[2][0] + rally[2][1] == 0:
                            fulldata["Starts"][setnumber] = i + 1
                        elif fulldata["Starts"][setnumber] == 0:
                            fulldata["Starts"][setnumber] = -1

        # currently disables as we don't need it
        if False:
            fulldata["Vote"] = self.compute_vote(team, player_number, fulldata)
        return fulldata

    def analyze(self) -> None:
        self.fill_scores()
        self.fill_global_info()
        self.fill_team_stats()
        self.fill_player_stats()
        self.fill_detailed_info()

        TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template")
        file_loader = FileSystemLoader(TEMPLATE_PATH)
        env = Environment(loader=file_loader)

        template = env.get_template("template.jinja2")

        output = template.render(
            scores=self.scores,
            global_info=self.global_info,
            playerstats=self.playerstats,
            teamstats=self.teamstats,
            detailed_infos=self.detailed_infos,
            template_path=TEMPLATE_PATH,
        )

        with open("gamestats.tex", "w") as f:
            f.write(output)
            f.close()
