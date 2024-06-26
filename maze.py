from dataclasses import dataclass
from os import path
import os

@dataclass
class Tile: 
    empty: bool

    def __str__(self) -> str:
        return " " if self.empty else "#"

@dataclass
class Wall(Tile):
    def __post_init__(self):
        self.empty = False

mazes: list[list[Tile | None]] = []

MAZE_FOLDER = "mazes"

for file in os.scandir(MAZE_FOLDER):
    if not file.is_file():
        continue

    mazes.append([])
    maze = open(file.path)

    for i, line in enumerate(maze):
        line = line.strip()
        mazes[-1].append([])

        for j, cell in enumerate(line):
            if cell == " ":
                mazes[-1][i].append(Tile(True))
            else:
                mazes[-1][i].append(Wall(False))