import os
from dataclasses import dataclass

@dataclass
class MazeTemplate:
    size: tuple[int, int]
    index: int
    entrance: tuple[int, int]
    exit: tuple[int, int]
    matrix: list[list[str]]

mazes: list[MazeTemplate] = []

MAZE_FOLDER = os.path.join("assets", "mazes")

index = 0

while True:
    index += 1

    path = os.path.join(MAZE_FOLDER, f"maze{index}.txt")

    if not os.path.isfile(path):
        break

    with open(path) as maze:
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
        mazes.append(MazeTemplate(size, index, entry, exit, matrix))
