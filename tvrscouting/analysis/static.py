import os
from typing import Dict

from jinja2 import Environment, FileSystemLoader

from tvrscouting.analysis.filters import (
    action_filter_from_string,
    compare_action_to_string,
    rally_filter_from_string,
)
from tvrscouting.organization.game_meta_info import GameMetaInfo
from tvrscouting.statistics.Actions.GameAction import Gameaction, Quality
from tvrscouting.statistics.Actions.SpecialAction import Endset
from tvrscouting.statistics.Gamestate.game_state import GameState, Rally
from tvrscouting.statistics.Players.players import Player, Team
from typing import List, Optional
from tvrscouting.statistics.Actions import Action


class StaticWriter:
    """
    writes out the datavolley-like file
    """

    # all the required information to fill out the template
    global_info = {}
    scores = {}
    playerstats = {}
    teamstats = {}
    detailed_infos = {}

    gamestate: GameState

    def __init__(self, game_state: GameState, game_meta_info):
        super().__init__()
        self.gamestate = game_state
        self.meta_info: GameMetaInfo = game_meta_info
        self.collected_stats: Dict = {}

    def fill_scores(self) -> None:
        partialscores = []
        start_times = []
        end_times = []
        intermediates = [8, 16, 21]
        intermediate = intermediates[0]
        totalscore = 25
        for rally in self.gamestate.rallies:
            setnumber = rally.set_score[0] + rally.set_score[1] + 1
            if len(partialscores) < setnumber:
                partialscores.append({"finalscore": [], "mid_results": []})
                if setnumber == 5:
                    intermediates = [5, 10, 12]
                    intermediate = intermediates[0]
            if len(start_times) < setnumber:
                for action in rally.actions:
                    if action.time_stamp:
                        if isinstance(action, Gameaction):
                            start_times.append(action.time_stamp)
                            break
            if len(end_times) < setnumber:
                for action in rally.actions:
                    if isinstance(action, Endset):
                        end_times.append(action.time_stamp)
                        break

            if rally.score[0] == intermediate or rally.score[1] == intermediate:
                partialscores[setnumber - 1]["mid_results"].append(rally.score)
                try:
                    intermediate = intermediates[intermediates.index(intermediate) + 1]
                except IndexError:
                    intermediate = intermediates[0]
            # TODO: rename
            totalscore = 25 if rally.set_score[0] + rally.set_score[1] < 4 else 15
            if (rally.score[0] >= totalscore and rally.score[0] > rally.score[1] + 1) or (
                rally.score[1] >= totalscore and rally.score[1] > rally.score[0] + 1
            ):
                totalscore = max(rally.score)
                partialscores[setnumber - 1]["finalscore"] = rally.score
        if len(start_times) != len(end_times):
            end_times.append(self.gamestate.rallies[-1].actions[-1].time_stamp)
        last = self.gamestate.score
        if last[0] != totalscore and last[1] != totalscore and (last[0] != 0 or last[1] != 0):
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
            if len(start_times) > i and len(end_times) > i and start_times[i] and end_times[i]:
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
        self.global_info["coaches"] = {
            "home": {
                "HC": "",
                "AC": "",
            },
            "guest": {
                "HC": "",
                "AC": "",
            },
        }
        if self.meta_info:
            self.global_info["coaches"]["home"]["HC"] = (
                self.meta_info.teams[0].head_coach if self.meta_info.teams[0] else ""
            )
            self.global_info["coaches"]["home"]["AC"] = (
                self.meta_info.teams[0].assistant_coach if self.meta_info.teams[0] else ""
            )
            self.global_info["coaches"]["guest"]["HC"] = (
                self.meta_info.teams[1].head_coach if self.meta_info.teams[1] else ""
            )
            self.global_info["coaches"]["guest"]["AC"] = (
                self.meta_info.teams[1].assistant_coach if self.meta_info.teams[1] else ""
            )
            self.global_info["Liga"] = self.meta_info.league
            self.global_info["Saison"] = self.meta_info.season
            self.global_info["Runde"] = self.meta_info.phase
            self.global_info["Spectators"] = self.meta_info.spectators
            self.global_info["date"] = self.meta_info.date
            self.global_info["time"] = self.meta_info.time
            self.global_info["Hall"] = self.meta_info.hall
            self.global_info["City"] = self.meta_info.city
            self.global_info["match_number"] = self.meta_info.matchnumber
            self.global_info["Refs"] = []
            for ref in self.meta_info.refs:
                self.global_info["Refs"].append(ref)

        self.global_info["serving_teams"] = self.collect_serving_teams()

    @staticmethod
    def rally_contains_gameaction(rally):
        for action in rally.actions:
            if isinstance(action, Gameaction):
                return True
        return False

    def collect_serving_teams(self):
        result = {}
        number_of_sets = self.gamestate.set_score[0] + self.gamestate.set_score[1]
        for rally in self.gamestate.rallies:
            setnumber = rally.set_score[0] + rally.set_score[1] + 1
            if setnumber not in result and rally.last_serve:
                if self.rally_contains_gameaction(rally):
                    result[setnumber] = str(int(rally.last_serve))
        return result

    def fill_team_stats(self):
        self.teamstats["home"] = {
            "Total": self.init_data_dict(),
            "Per_set": [],
        }
        self.teamstats["guest"] = {
            "Total": self.init_data_dict(),
            "Per_set": [],
        }
        # self.teamstats = {
        #     "home": {
        #         "Total": {},
        #         "Per_set": [],
        #     },
        #     "guest": {
        #         "Total": {},
        #         "Per_set": [],
        #     },
        # }

        # self.teamstats["home"]["Total"] = self.collect_stats_from_number(
        #     Team.from_string("*"), "@@"
        # )
        # self.teamstats["guest"]["Total"] = self.collect_stats_from_number(
        #     Team.from_string("/"), "@@"
        # )

        number_of_sets = self.gamestate.set_score[0] + self.gamestate.set_score[1]
        if self.gamestate.score[0] + self.gamestate.score[1] != 0:
            number_of_sets += 1
        for i in range(number_of_sets):

            rally_filter_string = "@@@@@@@@@@" + str(i) + "@"
            current_rallies = rally_filter_from_string(rally_filter_string, self.gamestate.rallies)
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
            # self.teamstats["home"]["Per_set"].append(setstat_home)

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
            # self.teamstats["guest"]["Per_set"].append(setstat_guest)

    @staticmethod
    def init_data_dict() -> Dict:
        fulldata = {
            "Attack": {"Total": 0, "Points": 0, "Errors": 0, "Blocked": 0, "Percentage": 0},
            "Blocks": 0,
            "Reception": {"Total": 0, "Positive": 0, "Errors": 0, "Perfect": 0, "Percentage": 0},
            "Serve": {"Total": 0, "Errors": 0, "Points": 0},
            "Points": {"Total": 0, "Errors": 0, "Plus_minus": 0, "BP": 0},
        }
        return fulldata

    @staticmethod
    def player_key_from_action(game_action: Gameaction):
        return str(game_action.team) + "%02d" % game_action.player

    @staticmethod
    def team_key_from_action(game_action: Gameaction) -> str:
        return StaticWriter.team_key_from_team(game_action.team)

    @staticmethod
    def team_key_from_team(team: Team) -> str:
        if team == Team.Home:
            return "home"
        else:
            return "guest"

    def add_set_stats_if_needed(self, rally):
        if len(self.teamstats["home"]["Per_set"]) <= rally.set_score[0] + rally.set_score[1]:
            for team in ["home", "guest"]:
                self.teamstats[team]["Per_set"].append(self.init_data_dict())
                self.teamstats[team]["Per_set"][-1]["setnumber"] = (
                    rally.set_score[0] + rally.set_score[1] + 1
                )
                self.teamstats[team]["Per_set"][-1]["SABO"] = {
                    "serve": 0,
                    "attack": 0,
                    "block": 0,
                    "errors": 0,
                }

    @staticmethod
    def can_be_break_point(action: Gameaction, rally: Rally) -> bool:
        return action.team == Team.inverse(rally.find_receiveing_team())

    @staticmethod
    def update_percentages_in_dict(dict):
        dict["Attack"]["Percentage"] = int(
            100
            * (
                (dict["Attack"]["Points"] / dict["Attack"]["Total"])
                if dict["Attack"]["Total"] > 0
                else 0
            )
        )
        dict["Reception"]["Percentage"] = int(
            100
            * (
                (dict["Reception"]["Positive"] / dict["Reception"]["Total"])
                if dict["Reception"]["Total"] > 0
                else 0
            )
        )
        dict["Points"]["Plus_minus"] = dict["Points"]["Total"] - dict["Points"]["Errors"]

    @staticmethod
    def update_percentages(dict):
        for k, v in dict.items():
            StaticWriter.update_percentages_in_dict(v)

    def fill_stats_from_rallies(self, rallies: Optional[List[Rally]] = None):
        rallies = self.gamestate.rallies if rallies is None else rallies
        can_break = False
        for rally in rallies:
            self.add_set_stats_if_needed(rally)
            for action in rally.actions:
                try:
                    if isinstance(action, Gameaction):
                        can_break = self.can_be_break_point(action, rally)
                        team_stats = self.teamstats[self.team_key_from_action(action)]["Total"]
                        player_stats = self.collected_stats[self.player_key_from_action(action)]
                        set_stats = self.teamstats[self.team_key_from_action(action)]["Per_set"][
                            rally.set_score[0] + rally.set_score[1]
                        ]
                        if action.quality == Quality.Kill:
                            player_stats["Points"]["Total"] += 1
                            team_stats["Points"]["Total"] += 1
                            if can_break:
                                player_stats["Points"]["BP"] += 1
                                team_stats["Points"]["BP"] += 1
                        elif action.quality == Quality.Error:
                            player_stats["Points"]["Errors"] += 1
                            team_stats["Points"]["Errors"] += 1
                            self.teamstats[self.team_key_from_team(Team.inverse(action.team))][
                                "Per_set"
                            ][rally.set_score[0] + rally.set_score[1]]["SABO"]["errors"] += 1
                        elif action.quality == Quality.Over:
                            player_stats["Points"]["Errors"] += 1
                            team_stats["Points"]["Errors"] += 1

                        if action.action == Action.Hit:
                            player_stats["Attack"]["Total"] += 1
                            team_stats["Attack"]["Total"] += 1
                            set_stats["Attack"]["Total"] += 1

                            if action.quality == Quality.Kill:
                                player_stats["Attack"]["Points"] += 1
                                team_stats["Attack"]["Points"] += 1
                                set_stats["Attack"]["Points"] += 1
                                set_stats["SABO"]["attack"] += 1

                            elif action.quality == Quality.Error:
                                player_stats["Attack"]["Errors"] += 1
                                team_stats["Attack"]["Errors"] += 1
                                set_stats["Attack"]["Errors"] += 1

                            elif action.quality == Quality.Over:
                                player_stats["Attack"]["Blocked"] += 1
                                team_stats["Attack"]["Blocked"] += 1
                                set_stats["Attack"]["Blocked"] += 1

                        elif action.action == Action.Block:
                            if action.quality == Quality.Kill:
                                player_stats["Blocks"] += 1
                                team_stats["Blocks"] += 1
                                set_stats["Blocks"] += 1
                                set_stats["SABO"]["block"] += 1

                        elif action.action == Action.Reception:
                            player_stats["Reception"]["Total"] += 1
                            team_stats["Reception"]["Total"] += 1
                            set_stats["Reception"]["Total"] += 1

                            if action.quality == Quality.Error or action.quality == Quality.Over:
                                player_stats["Reception"]["Errors"] += 1
                                team_stats["Reception"]["Errors"] += 1
                                set_stats["Reception"]["Errors"] += 1

                            elif action.quality == Quality.Good:
                                player_stats["Reception"]["Positive"] += 1
                                team_stats["Reception"]["Positive"] += 1
                                set_stats["Reception"]["Positive"] += 1

                            elif action.quality == Quality.Perfect:
                                player_stats["Reception"]["Positive"] += 1
                                team_stats["Reception"]["Positive"] += 1
                                set_stats["Reception"]["Positive"] += 1
                                player_stats["Reception"]["Perfect"] += 1
                                team_stats["Reception"]["Perfect"] += 1
                                set_stats["Reception"]["Perfect"] += 1

                        elif action.action == Action.Serve:
                            player_stats["Serve"]["Total"] += 1
                            team_stats["Serve"]["Total"] += 1
                            set_stats["Serve"]["Total"] += 1

                            if action.quality == Quality.Kill:
                                player_stats["Serve"]["Points"] += 1
                                team_stats["Serve"]["Points"] += 1
                                set_stats["Serve"]["Points"] += 1
                                set_stats["SABO"]["serve"] += 1

                            elif action.quality == Quality.Error:
                                player_stats["Serve"]["Errors"] += 1
                                team_stats["Serve"]["Errors"] += 1
                                set_stats["Serve"]["Errors"] += 1
                except KeyError:
                    print("a bad thing was found")
        self.update_percentages(self.collected_stats)
        for team in ["home", "guest"]:
            self.update_percentages_in_dict(self.teamstats[team]["Total"])
            for current_set in self.teamstats[team]["Per_set"]:
                self.update_percentages_in_dict(current_set)

    def fill_player_stats(self) -> None:
        self.playerstats["home"] = []
        self.playerstats["guest"] = []
        for team, name in [
            (Team.from_string("*"), "home"),
            (Team.from_string("/"), "guest"),
        ]:
            # self.teamstats[name] = self.init_data_dict()
            for player in self.gamestate.players[int(team)]:
                self.collect_individual_statistics(team, player)

        self.fill_stats_from_rallies()

        for k, v in self.collected_stats.items():
            index = "home" if k[0] == "*" else "guest"
            self.playerstats[index].append(v)

        for team, name in [
            (Team.from_string("*"), "home"),
            (Team.from_string("/"), "guest"),
        ]:
            for player in self.gamestate.players[int(team)]:
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
            plus_minus_rotations = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
            for rally in self.gamestate.rallies:
                setter_position = rally.court.fields[int(team)].get_setter_position()
                if setter_position > 0:
                    team_stats_in_rotation = self.collect_stats_from_number(team, "@@", [rally])
                    points = team_stats_in_rotation["Points"]["Total"]
                    errors = team_stats_in_rotation["Points"]["Errors"]
                    opponent_stats_in_rotation = self.collect_stats_from_number(
                        Team.inverse(team), "@@", [rally]
                    )
                    opponent_points = opponent_stats_in_rotation["Points"]["Total"]
                    opponent_errors = opponent_stats_in_rotation["Points"]["Errors"]
                    plus_minus_rotations[setter_position] += (points + opponent_errors) - (
                        opponent_points + errors
                    )
            for k, v in plus_minus_rotations.items():
                self.detailed_infos[name]["plus_minus_rotations"].append((v, k))

            # Number of sideout points
            rece_rallies = rally_filter_from_string(
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
            serve_rallies = rally_filter_from_string(
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
            rece_rallies = []
            for rally in self.gamestate.rallies:
                if len(action_filter_from_string(str(Team.inverse(team)) + "@@s", [rally])) > 0:
                    rece_rallies.append(rally)

            positive_rallies = []
            negative_rallies = []
            for rally in rece_rallies:
                has_positive = len(
                    action_filter_from_string(str(team) + "@@r+@@@@", [rally])
                ) + len(action_filter_from_string(str(team) + "@@rp@@@@", [rally]))
                has_negative = len(
                    action_filter_from_string(str(team) + "@@r-@@@@", [rally])
                ) + len(action_filter_from_string(str(team) + "@@ro@@@@", [rally]))
                if has_positive > 0:
                    positive_rallies.append(rally)
                elif has_negative > 0:
                    negative_rallies.append(rally)
            total_k1 = 0
            error_k1 = 0
            blocked_k1 = 0
            points_k1 = 0
            total_k2 = 0
            error_k2 = 0
            blocked_k2 = 0
            points_k2 = 0
            for rally in positive_rallies:
                k1_found = False
                for action in rally.actions:
                    if isinstance(action, Gameaction):
                        current_action = str(action)
                        if not k1_found:
                            if compare_action_to_string(
                                current_action, str(Team.inverse(team)) + "@@h@"
                            ):
                                k1_found = True
                            if compare_action_to_string(current_action, str(team) + "@@h@"):
                                total_k1 += 1
                                k1_found = True
                            if compare_action_to_string(current_action, str(team) + "@@h="):
                                error_k1 += 1
                                k1_found = True
                            if compare_action_to_string(current_action, str(team) + "@@ho"):
                                blocked_k1 += 1
                                k1_found = True
                            if compare_action_to_string(current_action, str(team) + "@@h#"):
                                points_k1 += 1
                                k1_found = True
                        else:
                            if compare_action_to_string(current_action, str(team) + "@@h@"):
                                total_k2 += 1
                            if compare_action_to_string(current_action, str(team) + "@@h="):
                                error_k2 += 1
                            if compare_action_to_string(current_action, str(team) + "@@ho"):
                                blocked_k2 += 1
                            if compare_action_to_string(current_action, str(team) + "@@h#"):
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
            for rally in negative_rallies:
                k1_found = False
                for action in rally.actions:
                    if isinstance(action, Gameaction):
                        current_action = str(action)
                        if not k1_found:
                            if compare_action_to_string(
                                current_action, str(Team.inverse(team)) + "@@h@"
                            ):
                                k1_found = True
                            if compare_action_to_string(current_action, str(team) + "@@h@"):
                                total_k1 += 1
                                k1_found = True
                            if compare_action_to_string(current_action, str(team) + "@@h="):
                                error_k1 += 1
                                k1_found = True
                            if compare_action_to_string(current_action, str(team) + "@@ho"):
                                blocked_k1 += 1
                                k1_found = True
                            if compare_action_to_string(current_action, str(team) + "@@h#"):
                                points_k1 += 1
                                k1_found = True
                        else:
                            if compare_action_to_string(current_action, str(team) + "@@h@"):
                                total_k2 += 1
                            if compare_action_to_string(current_action, str(team) + "@@h="):
                                error_k2 += 1
                            if compare_action_to_string(current_action, str(team) + "@@ho"):
                                blocked_k2 += 1
                            if compare_action_to_string(current_action, str(team) + "@@h#"):
                                points_k2 += 1
            serve_rallies = []
            for rally in self.gamestate.rallies:
                if len(action_filter_from_string(str(team) + "@@s", [rally])) > 0:
                    serve_rallies.append(rally)
            for rally in serve_rallies:
                for action in rally.actions:
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

    def collect_stats_from_number(self, team: Team, player_number: str, rallies=None) -> Dict:
        rallies = self.gamestate.rallies if rallies is None else rallies
        fulldata = {}
        fulldata["Attack"] = {}
        filterstring = str(team) + player_number + "h" + "@@@@@"
        fulldata["Attack"]["Total"] = len(action_filter_from_string(filterstring, rallies))
        filterstring = str(team) + player_number + "h" + "#@@@@"
        fulldata["Attack"]["Points"] = len(action_filter_from_string(filterstring, rallies))
        filterstring = str(team) + player_number + "h" + "=@@@@"
        fulldata["Attack"]["Error"] = len(action_filter_from_string(filterstring, rallies))
        filterstring = str(team) + player_number + "h" + "o@@@@"
        fulldata["Attack"]["Blocked"] = len(action_filter_from_string(filterstring, rallies))
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
        fulldata["Reception"]["Error"] = len(action_filter_from_string(filterstring, rallies))
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
        fulldata["Serve"]["Total"] = len(action_filter_from_string(filterstring, rallies))
        filterstring = str(team) + player_number + "s" + "="
        fulldata["Serve"]["Error"] = len(action_filter_from_string(filterstring, rallies))
        filterstring = str(team) + player_number + "s" + "#"
        fulldata["Serve"]["Points"] = len(action_filter_from_string(filterstring, rallies))

        fulldata["Points"] = {}
        filterstring = str(team) + player_number + "@" + "#"
        total_points = len(action_filter_from_string(filterstring, rallies))
        fulldata["Points"]["Total"] = total_points
        filterstring = str(team) + player_number + "@" + "="
        total_errors = len(action_filter_from_string(filterstring, rallies))
        fulldata["Points"]["Errors"] = total_errors
        filterstring = str(team) + player_number + "@" + "o"
        total_errors += len(action_filter_from_string(filterstring, rallies))
        fulldata["Points"]["Plus_minus"] = total_points - total_errors

        break_rallies = rally_filter_from_string("@@@@@@@@@@@" + str(team), self.gamestate.rallies)
        filterstring = str(team) + player_number + "@#"
        fulldata["Points"]["BP"] = len(action_filter_from_string(filterstring, break_rallies))
        return fulldata

    def compute_vote(self, team: Team, player_number: Player, fulldata: Dict) -> float:
        # here is the vote computation that we're never using
        votes = 0
        vote = 0
        filterstring = str(team) + "@@" + "s" + "@"
        total_serves = len(action_filter_from_string(filterstring, self.gamestate.rallies))
        if fulldata["Serve"]["Total"] / total_serves > 0.05:
            filterstring = str(team) + player_number + "s" + "p"
            serve_overs = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            filterstring = str(team) + player_number + "s" + "+"
            serve_plus = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            filterstring = str(team) + player_number + "s" + "-"
            serve_minus = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            serve_vote = (
                fulldata["Serve"]["Points"] * 10
                + serve_overs * 8
                + serve_plus * 7
                + serve_minus * 4
            ) / fulldata["Serve"]["Total"]
            vote += serve_vote if serve_vote > 5.5 else 5.5
            votes += 1

        filterstring = str(team) + "@@" + "r" + "@"
        total_receptions = len(action_filter_from_string(filterstring, self.gamestate.rallies))
        if fulldata["Reception"]["Total"] / total_serves > 0.07:
            filterstring = str(team) + player_number + "r" + "p"
            perfect = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            filterstring = str(team) + player_number + "r" + "+"
            positive = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            filterstring = str(team) + player_number + "r" + "-"
            negative = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            filterstring = str(team) + player_number + "r" + "o"
            errors = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            rece_vote = (perfect * 10 + positive * 7 + negative * -1 + errors * -3) / fulldata[
                "Reception"
            ]["Total"]
            vote += rece_vote if rece_vote > 5.5 else 5.5
            votes += 1

        filterstring = str(team) + "@@" + "h" + "@"
        total_hits = len(action_filter_from_string(filterstring, self.gamestate.rallies))
        if fulldata["Attack"]["Total"] / total_hits > 0.07:
            filterstring = str(team) + player_number + "h" + "#"
            kills = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            filterstring = str(team) + player_number + "r" + "+"
            positive = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            filterstring = str(team) + player_number + "r" + "-"
            negative = len(action_filter_from_string(filterstring, self.gamestate.rallies))
            hit_vote = (kills * 10 + positive * 5 + negative * 5) / fulldata["Attack"]["Total"]
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

    def collect_individual_statistics(self, team: Team, player: Player) -> None:
        self.collected_stats[str(team) + "%02d" % player.Number] = self.init_data_dict()
        self.collected_stats[str(team) + "%02d" % player.Number]["Name"] = player.Name
        self.collected_stats[str(team) + "%02d" % player.Number]["Number"] = player.Number
        self.collected_stats[str(team) + "%02d" % player.Number]["Role"] = ""
        if self.meta_info and self.meta_info.teams[int(team)]:
            for player_from_team in self.meta_info.teams[int(team)].players:
                if (
                    player_from_team.Name == player.Name
                    and player_from_team.Number == player.Number
                    and player_from_team.is_capitain
                ):
                    self.collected_stats[str(team) + "%02d" % player.Number]["Role"] = "C"
        self.collected_stats[str(team) + "%02d" % player.Number]["IsSetter"] = (
            player.PlayerPosition.Setter == player.Position
        )
        if player.is_capitain:
            self.collected_stats[str(team) + "%02d" % player.Number]["Role"] = "C"
        elif player.Position == Player.PlayerPosition.Libera:
            self.collected_stats[str(team) + "%02d" % player.Number]["Role"] = "L"
        self.collected_stats[str(team) + "%02d" % player.Number]["Starts"] = [0, 0, 0, 0, 0]
        for rally in self.gamestate.rallies:
            setnumber = rally.set_score[0] + rally.set_score[1]
            if player.Position == Player.PlayerPosition.Libera:
                for action in rally.actions:
                    if isinstance(action, Gameaction):
                        if action.player == player.Number and action.team == team:
                            self.collected_stats[str(team) + "%02d" % player.Number]["Starts"][
                                setnumber
                            ] = -1
                            continue
            elif self.collected_stats[str(team) + "%02d" % player.Number]["Starts"][setnumber] == 0:
                for i in range(6):
                    if player.Number == rally.court.fields[int(team)].players[i].Number:
                        if rally.score[0] + rally.score[1] == 0:
                            self.collected_stats[str(team) + "%02d" % player.Number]["Starts"][
                                setnumber
                            ] = (i + 1)
                        else:
                            self.collected_stats[str(team) + "%02d" % player.Number]["Starts"][
                                setnumber
                            ] = -1

        # currently disables as we don't need it
        if False:
            self.collected_stats[str(team) + "%02d" % player.Number]["Vote"] = self.compute_vote(
                team,
                "%02d" % player.Number,
                self.collected_stats[str(team) + "%02d" % player.Number],
            )
        return self.collected_stats[str(team) + "%02d" % player.Number]

    def analyze(self, set_number: int) -> None:
        self.fill_scores()
        self.fill_global_info()
        self.fill_team_stats()
        print("team_stats")
        self.fill_player_stats()
        print("player stats")
        self.fill_detailed_info()
        print("details")

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
        print("template")

        with open("gamestats.tex", "w") as f:
            f.write(output)
            f.close()
