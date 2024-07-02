from yaml import safe_load, safe_dump
import os
from io import TextIOWrapper

LEADERBOARD_PATH = os.path.join("data", "leaderboard.yml")

def read() -> list[dict]:
    with open(LEADERBOARD_PATH) as file:
        return safe_load(file)

def add(score: dict):
    with open(LEADERBOARD_PATH, "w+") as file:
        scores = safe_load(file)
        
        if not scores:
            scores = [score]
        else:
            scores.append(score)

        safe_dump(scores, file)

def clear():
    if os.path.isfile(LEADERBOARD_PATH):
        os.remove(LEADERBOARD_PATH)
