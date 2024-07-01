import os
from dataclasses import dataclass

@dataclass
class MazeTemplate:
    size: tuple[int, int]
    entrance: tuple[int, int]
    exit: tuple[int, int]
    matrix: list[list[str]]

mazes: list[MazeTemplate] = []

MAZE_FOLDER = os.path.join("assets", "mazes")

for file in os.scandir(MAZE_FOLDER):
    if not file.is_file():
        continue

    with open(file.path) as maze:
        entry = None
        exit = None

        matrix = []

        for i, line in enumerate(maze):
            line = list(line.strip())

            if "E" in line:
                entry = (i, line.index("E"))
            
            if "S" in line:
                exit = (i, line.index("S"))

            matrix.append(line)

        size = (len(matrix[0]), len(matrix))
        mazes.append(MazeTemplate(size, entry, exit, matrix))
