import os
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader

from tvrscouting.statistics.Actions import Action, GameAction
from tvrscouting.statistics.Actions.GameAction import Gameaction, Quality
from tvrscouting.statistics.Actions.SpecialAction import Substitute, Timeout
from tvrscouting.statistics.Gamestate.game import Game
from tvrscouting.statistics.Gamestate.game_state import GameState, Rally
from tvrscouting.statistics.Players.players import Player, Team


class PlayByPlay:
    def __init__(self, game: Game) -> None:
        self.players: List[List[Player]] = [[], []]
        self.game: Game = game
        self.game_state: GameState = game.game_state
        self.players: List[List[Player]] = self.game_state.get_players_from_game_state()
        pass

    @staticmethod
    def action_shows_in_play_by_play(action: GameAction) -> bool:
        if action.quality == Quality.Kill:
            return action.team, True
        elif action.quality == Quality.Error or action.quality == Quality.Over:
            return Team.inverse(action.team), True
        else:
            return None, False

    @staticmethod
    def expand_action_name(action: Action) -> str:
        if action == Action.Set:
            return "Set"
        if action == Action.Hit:
            return "Attack"
        if action == Action.Block:
            return "Block"
        if action == Action.Serve:
            return "Serve"
        if action == Action.Reception:
            return "Reception"
        if action == Action.Defense:
            return "Defense"
        if action == Action.Freeball:
            return "Freeball"
        raise NotImplementedError()

    @staticmethod
    def expand_action_quality(action: Gameaction) -> str:
        if action.quality == Quality.Kill and action.action == Action.Hit:
            return "Kill"
        if action.quality == Quality.Kill and action.action == Action.Serve:
            return "Ace"
        if action.quality == Quality.Kill and action.action == Action.Block:
            return "Stuff"
        if action.quality == Quality.Over and action.action == Action.Hit:
            return "Blocked"
        if action.quality == Quality.Kill:
            return "Kill"
        if action.quality == Quality.Over or action.quality == Quality.Error:
            return "Error"
        raise NotImplementedError()

    def expand_player_name_from_number(self, team: Team, number: int) -> str:
        for player in self.players[int(team)]:
            if player.Number == number:
                return "(" + str(player.Number) + ") " + player.Name

    def game_action_to_play_by_play_string(self, action: Gameaction, serving_team: Team) -> str:
        if action.quality == Quality.Over:
            color = "\\textcolor{red}{ {\\footnotesize "
            appendix = "} }"
        elif action.quality == Quality.Error:
            color = "\\textcolor{red}{"
            appendix = "}"
        elif action.team == serving_team and serving_team == Team.Home:
            color = "\\textcolor{blue}{\\textbf{BP }}"
            appendix = ""
        elif action.team == serving_team and serving_team == Team.Away:
            color = ""
            appendix = "\\textcolor{blue}{\\textbf{ BP}}"
        else:
            color = ""
            appendix = ""
        returnvalue = (
            color
            + self.expand_action_name(action.action)
            + " "
            + self.expand_action_quality(action)
            + " "
            + self.expand_player_name_from_number(action.team, action.player)
            + appendix
        )
        return returnvalue

    def timeout_to_play_by_play_string(self, action: Timeout) -> str:
        alignment = "l" if action.team == Team.Away else "r|"
        return "\\multicolumn{4}{" + alignment + "}{\\textcolor{orange}{Timeout}}"

    def sub_to_play_by_play_string(self, action: Substitute) -> Optional[str]:
        player_in = ""
        player_out = ""
        alignment = "l" if action.team_ == Team.Away else "r|"
        for player in self.players[int(action.team_)]:
            if player.Number == action.player_in:
                player_in = player.Name + " "
                break
        if action.player_out:
            for player in self.players[int(action.team_)]:
                if player.Number == action.player_out:
                    player_out = "out: " + player.Name
                    break
        if len(player_out):
            return (
                "\\multicolumn{4}{"
                + alignment
                + "}{\\textcolor{orange}{Sub in: "
                + player_in
                + player_out
                + "}}"
            )
        else:
            return None

    def generate_play_by_play_lines_from_rally(self, rally: Rally) -> str:
        team_strings = [["", "", "", "", ""], ["", "", "", "", ""]]
        setter_changed = [False, False]
        had_game_actions = False
        for action in rally.actions:
            if isinstance(action, Timeout):
                if action.team_ == Team.Home:
                    return "& " + self.timeout_to_play_by_play_string(action) + "&\\\\"
                else:
                    return "&&&&& " + self.timeout_to_play_by_play_string(action) + "\\\\"
            elif isinstance(action, Substitute):
                string = self.sub_to_play_by_play_string(action)
                if action.team_ == Team.Home:
                    if string:
                        return "& " + string + "&\\\\"
                else:
                    if string:
                        return "&&&&& " + string + "\\\\"
            if isinstance(action, Gameaction):
                had_game_actions = True
                scoring_team, was_score = self.action_shows_in_play_by_play(action)
                if was_score:
                    team_strings[int(action.team)][1] = self.game_action_to_play_by_play_string(
                        action, rally.last_serve
                    )
                if scoring_team:
                    if scoring_team == Team.Home:
                        team_strings[int(scoring_team)][2] = (
                            "\\textbf{" + str(rally.score[0] + 1) + "}-" + str(rally.score[1])
                        )
                    elif scoring_team == Team.Away:
                        team_strings[int(scoring_team)][2] = (
                            str(rally.score[0]) + "-\\textbf{" + str(rally.score[1] + 1) + "}"
                        )
                rece_team = rally.find_receiveing_team()
                if rece_team:
                    serving_team = Team.inverse(rece_team)
                    serving_player = str(rally.court.fields[int(serving_team)].players[0].Number)
                    team_strings[int(serving_team)][3] = serving_player

                for team in [0, 1]:
                    if self.setters[team] != rally.court.fields[team].get_setter_position():
                        setter_changed[team] = True
                        team_strings[team][0] = str(rally.court.fields[team].get_setter_position())
                        self.setters[team] = rally.court.fields[team].get_setter_position()
                if scoring_team and scoring_team == Team.Home:
                    delta = rally.score[0] + 1 - rally.score[1]
                elif scoring_team and scoring_team == Team.Away:
                    delta = rally.score[0] - rally.score[1] - 1
                else:
                    delta = rally.score[0] - rally.score[1]
                if delta > 0:
                    box = "\\bluebox" if delta >= self.olddelta else "\\redbox"
                    team_strings[0][4] = delta * box
                    self.olddelta = delta
                else:
                    box = "\\bluebox" if delta <= self.olddelta else "\\redbox"
                    team_strings[1][4] = abs(delta) * box
                    self.olddelta = delta
        team_strings[1].reverse()
        returnvalue = ""
        if setter_changed[0]:
            returnvalue += "\\cline{1-4}"
        if setter_changed[1]:
            returnvalue += "\\cline{7-10}"
        returnvalue += "\n"
        for team in [0, 1]:
            for string in team_strings[team]:
                returnvalue += string + "&"
        returnvalue = returnvalue[:-1]
        returnvalue += "\\\\"
        if had_game_actions:
            return returnvalue
        else:
            return ""

    def generate_play_by_play_lines_from_game_state(self, setnumber: int):
        self.setters = [-1, -1]
        self.olddelta = 0
        self.full_string = ""
        for rally in self.game_state.rallies:
            if rally.set_score[0] + rally.set_score[1] + 1 == setnumber:
                self.full_string += self.generate_play_by_play_lines_from_rally(rally)

    def generate_game_meta_info(self):
        self.meta_info = {
            "teams": {
                "home": self.game_state.teamnames[0],
                "guest": self.game_state.teamnames[1],
            },
            "set_score": {
                "home": self.game_state.set_score[0],
                "guest": self.game_state.set_score[1],
            },
            "final_scores": {
                "home": [score[0] for score in self.game_state.final_scores],
                "guest": [score[1] for score in self.game_state.final_scores],
            },
            "total_scores": {
                "home": sum([score[0] for score in self.game_state.final_scores]),
                "guest": sum([score[1] for score in self.game_state.final_scores]),
            },
            "date": "",
            "time": "",
            "season": "",
            "league": "",
            "phase": "",
        }
        if self.game._meta_info:
            self.meta_info["date"] = self.game._meta_info.date
            self.meta_info["time"] = self.game._meta_info.time
            self.meta_info["season"] = self.game._meta_info.season
            self.meta_info["league"] = self.game._meta_info.league
            self.meta_info["phase"] = self.game._meta_info.phase

    def analyze(self, setnumber: int):
        TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template")
        file_loader = FileSystemLoader(TEMPLATE_PATH)
        env = Environment(loader=file_loader)

        template = env.get_template("playbyplay.jinja2")
        self.generate_play_by_play_lines_from_game_state(setnumber)
        self.generate_game_meta_info()
        self.meta_info["analysis"] = "Set " + str(setnumber)

        output = template.render(
            action_strings=self.full_string,
            meta_info=self.meta_info,
            template_path=TEMPLATE_PATH,
        )

        with open("playbyplay.tex", "w") as f:
            f.write(output)
            f.close()


if __name__ == "__main__":
    import sys

    from tvrscouting.serializer.serializer import Serializer

    file = sys.argv[1]
    ser = Serializer(None)
    game = ser.deserialize(file)
    pbp = PlayByPlay(game)
    pbp.analyze(2)
