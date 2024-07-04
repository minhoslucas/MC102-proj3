from yaml import safe_load, safe_dump
import os
from io import TextIOWrapper

LEADERBOARD_PATH = os.path.join("data", "leaderboard.yml")

def read() -> dict[int, dict[str, dict]]:
    if not os.path.isfile(LEADERBOARD_PATH):
        return {}

    with open(LEADERBOARD_PATH) as file:
        return safe_load(file)

def add(score: dict) -> bool:
    is_high_score = False

    scores = read()

    if not scores or len(scores) <= 0:
        scores = { score["maze"]: { score["player"]: score } }
        is_high_score = True
    elif score["maze"] not in scores:
        scores[score["maze"]] = { score["player"]: score }
        is_high_score = True
    elif score["player"] not in scores[score["maze"]]:
        scores[score["maze"]][score["player"]] = score
        is_high_score = True
    else:
        curr_score = scores[score["maze"]][score["player"]]

        new_score = (curr_score["score"], score["score"])
        curr_score = (score["time"], curr_score["score"])

        if new_score > curr_score:
            scores[score["maze"]][score["player"]] = score
            is_high_score = True

    if is_high_score:
        with open(LEADERBOARD_PATH, "w") as file:
            safe_dump(scores, file)

    return is_high_score

def clear():
    if os.path.isfile(LEADERBOARD_PATH):
        os.remove(LEADERBOARD_PATH)
