from yaml import safe_load, safe_dump
import os
from io import TextIOWrapper

LEADERBOARD_PATH = os.path.join("data", "leaderboard.yml")

type Leaderboard = dict[int, dict[str, dict]]

def read() -> Leaderboard:
    with open(LEADERBOARD_PATH) as file:
        return safe_load(file)

def add(score: dict) -> bool:
    is_high_score = False

    with open(LEADERBOARD_PATH, "w+") as file:
        scores: Leaderboard = safe_load(file)

        if not scores:
            scores = { score["maze"]: { score["player"]: score } }
        else:
            curr_score = scores["maze"][score["name"]]
            curr_score = (curr_score["time"], curr_score["score"])

            new_score = (score["time"], score["score"])

            if new_score > curr_score:
                scores["maze"][score["player"]] = score
                is_high_score = True

        safe_dump(scores, file)
    return is_high_score

def clear():
    if os.path.isfile(LEADERBOARD_PATH):
        os.remove(LEADERBOARD_PATH)
