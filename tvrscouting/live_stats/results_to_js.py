import copy
import os
from pathlib import Path
from typing import Dict, List, OrderedDict

from jinja2 import Environment, FileSystemLoader

from tvrscouting.statistics.Gamestate.game_state import Court, GameState
from tvrscouting.statistics.Players.players import Player


def write_results_to_js(
    input_results: List[OrderedDict],
    game_state: GameState,
    input_court: Court,
    player_list: List[List[Player]],
):
    results = copy.deepcopy(input_results)
    scores = {
        "home": game_state.score[0],
        "guest": game_state.score[1],
        "set_home": game_state.set_score[0],
        "set_guest": game_state.set_score[1],
        "set_scores": [],
    }
    for score in game_state.final_scores:
        scores["set_scores"].append(str(score[0]) + ":" + str(score[1]))
    for _ in range(len(scores["set_scores"]), 5):
        scores["set_scores"].append("")

    court = {"home": [], "guest": []}
    for player in input_court.fields[0].players:
        full_label = str(player.Number)
        for player_in_list in player_list[0]:
            if player_in_list.Number == player.Number:
                full_label = str(player.Number) + " " + player_in_list.Name
                break
        if len(full_label) > 12:
            full_label = full_label[:11] + "."
        court["home"].append(full_label)
    for player in input_court.fields[1].players:
        full_label = str(player.Number)
        for player_in_list in player_list[1]:
            if player_in_list.Number == player.Number:
                full_label = str(player.Number) + " " + player_in_list.Name
                break
        if len(full_label) > 12:
            full_label = full_label[:11] + "."
        court["guest"].append(full_label)

    stats = {
        "team": [
            {
                "name": results[0]["team"]["name"],
                "kills": results[0]["team"]["points"],
                "errors": results[0]["team"]["error"],
                "hits": results[0]["team"]["hit"]["total"],
                "spikes": results[0]["team"]["hit"]["kill"],
                "kill_perc": results[0]["team"]["hit"]["perc"],
                "rece": results[0]["team"]["rece"]["total"],
                "rece_perc": results[0]["team"]["rece"]["perc"],
                "serve": results[0]["team"]["serve"]["kill"],
                "block": results[0]["team"]["block"],
                "players": [],
            },
            {
                "name": results[1]["team"]["name"],
                "kills": results[1]["team"]["points"],
                "errors": results[1]["team"]["error"],
                "hits": results[1]["team"]["hit"]["total"],
                "spikes": results[1]["team"]["hit"]["kill"],
                "kill_perc": results[1]["team"]["hit"]["perc"],
                "rece": results[1]["team"]["rece"]["total"],
                "rece_perc": results[1]["team"]["rece"]["perc"],
                "serve": results[1]["team"]["serve"]["kill"],
                "block": results[1]["team"]["block"],
                "players": [],
            },
        ],
        "names": [results[0]["team"]["name"], results[1]["team"]["name"]],
        "home_total": {
            "kills": results[0]["team"]["points"],
            "errors": results[0]["team"]["error"],
            "hits": results[0]["team"]["hit"]["total"],
            "spikes": results[0]["team"]["hit"]["kill"],
            "kill_perc": results[0]["team"]["hit"]["perc"],
            "rece": results[0]["team"]["rece"]["total"],
            "rece_perc": results[0]["team"]["rece"]["perc"],
            "serve": results[0]["team"]["serve"]["kill"],
            "block": results[0]["team"]["block"],
        },
        "home": [],
        "guest_total": {
            "kills": results[1]["team"]["points"],
            "errors": results[1]["team"]["error"],
            "hits": results[1]["team"]["hit"]["total"],
            "spikes": results[1]["team"]["hit"]["kill"],
            "kill_perc": results[1]["team"]["hit"]["perc"],
            "rece": results[1]["team"]["rece"]["total"],
            "rece_perc": results[1]["team"]["rece"]["perc"],
            "serve": results[1]["team"]["serve"]["kill"],
            "block": results[1]["team"]["block"],
        },
        "guest": [],
    }
    results[0].pop("team", None)
    results[1].pop("team", None)
    for k, v in results[0].items():
        stats["team"][0]["players"].append(
            {
                "name": v["name"],
                "kills": v["points"],
                "errors": v["error"],
                "hits": v["hit"]["total"],
                "spikes": v["hit"]["kill"],
                "kill_perc": v["hit"]["perc"],
                "rece": v["rece"]["total"],
                "rece_perc": v["rece"]["perc"],
                "serve": v["serve"]["kill"],
                "block": v["block"],
            }
        )
    for k, v in results[1].items():
        stats["team"][1]["players"].append(
            {
                "name": v["name"],
                "kills": v["points"],
                "errors": v["error"],
                "hits": v["hit"]["total"],
                "spikes": v["hit"]["kill"],
                "kill_perc": v["hit"]["perc"],
                "rece": v["rece"]["total"],
                "rece_perc": v["rece"]["perc"],
                "serve": v["serve"]["kill"],
                "block": v["block"],
            }
        )

    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template")
    file_loader = FileSystemLoader(TEMPLATE_PATH)
    env = Environment(loader=file_loader)
    path = Path(os.path.dirname(__file__))
    OUTPUT_PATH = os.path.join(
        os.path.join(path.parent.parent.absolute(), "hosted_stats"), "scores.js"
    )

    template = env.get_template("scores.jinja2")
    output = template.render(scores=scores, court=court, stats=stats)

    with open(OUTPUT_PATH, "w") as f:
        f.write(output)
        f.close()
