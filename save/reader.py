from yaml import safe_dump, safe_load
from os.path import join

from maze.reader import MazeTemplate

SAVE_PATH = join("data", "save.yml")
MAZE_PATH = join("data", "maze.txt")

def read() -> dict:
    with open(MAZE_PATH) as maze_file:
        matrix = [list(line.strip()) for line in maze_file]

    with open(SAVE_PATH) as save_file:
        save = safe_load(save_file)

    save["maze"]["matrix"] = matrix
    save["maze"] = MazeTemplate(**save["maze"])

    return save

def write(save: dict):
    save["maze"] = save["maze"].__dict__
    maze = save["maze"]["matrix"]
    del save["maze"]["matrix"]

    with open(MAZE_PATH, "w") as maze_file:
        maze = ["".join(line) for line in maze]
        maze_file.write("\n".join(maze))

    with open(SAVE_PATH, "w") as save_file:
        safe_dump(save, save_file)
