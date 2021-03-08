#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader


global_info = {
    "teamnames": {
        "home": "Volley Rueschlikon",
        "guest": "Tracteur Rueschlikon",
    },
    "coaches": {
        "home": {
            "HC": "Adi Wicky",
            "AC": "Somother Name",
        },
        "guest": {
            "HC": "Nicole Roth",
        },
    },
    "match_number": 0000,
    "date": "10/01/2020",
    "time": "00:00:00",
    "City": "Rueschlikon",
    "Spectators": 000,
    "Hall": "Gulliver",
    "Refs": ["Some Name,", "Other Name"],
    "Liga": "1.Liga",
    "Saison": "20/22",
    "Runde": "Runde 12",
}

scores = {
    "set_score": {"home": 3, "guest": 2},
    "final_score": {"duration": 100, "score": {"home": 99, "guest": 110}},
    "setresults": [
        {
            "setnumber": 1,
            "time": 20,
            "results": [
                {"home": 6, "guest": 0},
                {"home": 14, "guest": 0},
                {"home": 21, "guest": 0},
            ],
            "finalresult": {"home": 25, "guest": 21},
        },
        {
            "setnumber": 2,
            "time": 22,
            "results": [
                {"home": 6, "guest": 2},
                {"home": 13, "guest": 14},
                {"home": 21, "guest": 20},
            ],
            "finalresult": {"home": 20, "guest": 25},
        },
        {
            "setnumber": 3,
            "time": 10,
            "results": [
                {"home": 0, "guest": 6},
                {"home": ".", "guest": "."},
                {"home": ".", "guest": "."},
            ],
            "finalresult": {"home": 8, "guest": 10},
        },
    ],
}

playerstats = {
    "home": [
        {
            "Name": "Franziska Zehnder",
            "Number": 14,
            "Role": "C",
            "Starts": [1, 2, 3, -1, 0],
            "Vote": 10,
            "Points": {
                "Total": 11,
                "BP": 3,
                "Plus_minus": 5,
            },
            "Serve": {
                "Total": 5,
                "Error": 2,
                "Points": ".",
            },
            "Reception": {
                "Total": 5,
                "Error": 2,
                "Positive": 10,
                "Perfect": ".",
            },
            "Attack": {
                "Total": 5,
                "Error": 2,
                "Blocked": ".",
                "Points": 10,
                "Percentage": 30,
            },
            "Blocks": 10,
        },
        {
            "Name": "June Lindegger",
            "Number": 20,
            "Role": "L",
            "Starts": [-1, -1, -1, -1, -1],
            "Vote": 10,
            "Points": {
                "Total": 2,
                "BP": 5,
                "Plus_minus": 2,
            },
            "Serve": {
                "Total": 5,
                "Error": 2,
                "Points": ".",
            },
            "Reception": {
                "Total": 5,
                "Error": 2,
                "Positive": 10,
                "Perfect": ".",
            },
            "Attack": {
                "Total": 5,
                "Error": 2,
                "Blocked": ".",
                "Points": 10,
                "Percentage": 30,
            },
            "Blocks": 10,
        },
    ],
    "guest": [
        {
            "Name": "AJune BLindegger",
            "Number": 20,
            "Role": "L",
            "Starts": [-1, -1, -1, -1, -1],
            "Vote": 10,
            "Points": {
                "Total": 2,
                "BP": 5,
                "Plus_minus": 2,
            },
            "Serve": {
                "Total": 5,
                "Error": 2,
                "Points": ".",
            },
            "Reception": {
                "Total": 5,
                "Error": 2,
                "Positive": 10,
                "Perfect": ".",
            },
            "Attack": {
                "Total": 5,
                "Error": 2,
                "Blocked": ".",
                "Points": 10,
                "Percentage": 30,
            },
            "Blocks": 10,
        },
    ],
}


teamstats = {
    "home": {
        "Total": {
            "Points": {
                "Total": 11,
                "BP": 3,
                "Plus_minus": 5,
            },
            "Serve": {
                "Total": 5,
                "Error": 2,
                "Points": ".",
            },
            "Reception": {
                "Total": 5,
                "Error": 2,
                "Positive": 10,
                "Perfect": ".",
            },
            "Attack": {
                "Total": 5,
                "Error": 2,
                "Blocked": ".",
                "Points": 10,
                "Percentage": 30,
            },
            "Blocks": 10,
        },
        "Per_set": [
            {
                "setnumber": 1,
                "SABO": {
                    "serve": 0,
                    "attack": 10,
                    "block": 20,
                    "errors": 15,
                },
                "Serve": {
                    "Total": 5,
                    "Error": 2,
                    "Points": ".",
                },
                "Reception": {
                    "Total": 5,
                    "Error": 2,
                    "Positive": 10,
                    "Perfect": ".",
                },
                "Attack": {
                    "Total": 5,
                    "Error": 2,
                    "Blocked": ".",
                    "Points": 10,
                    "Percentage": 30,
                },
                "Blocks": 10,
            },
        ],
    },
    "guest": {
        "Total": {
            "Points": {
                "Total": 11,
                "BP": 3,
                "Plus_minus": 5,
            },
            "Serve": {
                "Total": 5,
                "Error": 2,
                "Points": ".",
            },
            "Reception": {
                "Total": 5,
                "Error": 2,
                "Positive": 10,
                "Perfect": ".",
            },
            "Attack": {
                "Total": 5,
                "Error": 2,
                "Blocked": ".",
                "Points": 10,
                "Percentage": 30,
            },
            "Blocks": 10,
        },
        "Per_set": [
            {
                "setnumber": 1,
                "SABO": {
                    "serve": 0,
                    "attack": 10,
                    "block": 20,
                    "errors": 15,
                },
                "Serve": {
                    "Total": 5,
                    "Error": 2,
                    "Points": ".",
                },
                "Reception": {
                    "Total": 5,
                    "Error": 2,
                    "Positive": 10,
                    "Perfect": ".",
                },
                "Attack": {
                    "Total": 5,
                    "Error": 2,
                    "Blocked": ".",
                    "Points": 10,
                    "Percentage": 30,
                },
                "Blocks": 10,
            },
            {
                "setnumber": 1,
                "SABO": {
                    "serve": 0,
                    "attack": 10,
                    "block": 20,
                    "errors": 15,
                },
                "Serve": {
                    "Total": 5,
                    "Error": 2,
                    "Points": ".",
                },
                "Reception": {
                    "Total": 5,
                    "Error": 2,
                    "Positive": 10,
                    "Perfect": ".",
                },
                "Attack": {
                    "Total": 5,
                    "Error": 2,
                    "Blocked": ".",
                    "Points": 10,
                    "Percentage": 30,
                },
                "Blocks": 10,
            },
        ],
    },
}

detailed_infos = {
    "home": {
        "plus_minus_rotations": [(10, 6), (6, 5), (6, 4), (3, 3), (2, 2), (2, 1)],
        "SideOut": 40,
        "Rece_per_point": 1.88,
        "Break_Points": 31,
        "Serve_per_break": 2.88,
        "K1_stats": {
            "positive": {
                "Error": 3,
                "Blocked": 2,
                "Points": 20,
                "Total": 30,
            },
            "negative": {
                "Error": 3,
                "Blocked": 2,
                "Points": 20,
                "Total": 30,
            },
        },
        "K2_stats": {
            "Error": 3,
            "Blocked": 2,
            "Points": 20,
            "Total": 30,
        },
    },
    "guest": {
        "plus_minus_rotations": [(10, 6), (6, 5), (6, 4), (3, 3), (2, 2), (2, 1)],
        "SideOut": 40,
        "Rece_per_point": 1.88,
        "Break_Points": 31,
        "Serve_per_break": 2.88,
        "K1_stats": {
            "positive": {
                "Error": 3,
                "Blocked": 2,
                "Points": 20,
                "Total": 30,
            },
            "negative": {
                "Error": 3,
                "Blocked": 2,
                "Points": 20,
                "Total": 30,
            },
        },
        "K2_stats": {
            "Error": 3,
            "Blocked": 2,
            "Points": 20,
            "Total": 30,
        },
    },
}

file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)

template = env.get_template("template.jinja2")

output = template.render(
    scores=scores,
    global_info=global_info,
    playerstats=playerstats,
    teamstats=teamstats,
    detailed_infos=detailed_infos,
)

with open("template.tex", "w") as f:
    f.write(output)
    f.close()
