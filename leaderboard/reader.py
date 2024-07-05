from yaml import safe_load, safe_dump
import os
from io import TextIOWrapper

LEADERBOARD_PATH = os.path.join("data", "leaderboard.yml")
#lê o arquivo da leaderboard
def read() -> dict[str, dict]:
    if not os.path.isfile(LEADERBOARD_PATH):
        return {}

    with open(LEADERBOARD_PATH) as file:
        lb = safe_load(file)
        return lb if lb else {}

def add(score: dict) -> bool:
    is_high_score = False

    scores = read()

    if not scores or len(scores) <= 0:
        scores = { score["player"]: score }
        is_high_score = True
    elif score["player"] not in scores:
        scores[score["player"]] = score
        is_high_score = True
    elif scores[score["player"]]["score"] < score["score"]:
        scores[score["player"]] = score
        is_high_score = True

    if is_high_score:
        with open(LEADERBOARD_PATH, "w") as file:
            safe_dump(scores, file)

    return is_high_score

def clear():
    if os.path.isfile(LEADERBOARD_PATH):
        os.remove(LEADERBOARD_PATH)
