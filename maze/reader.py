import os

ALLOWED_CHARS = {" ", "#", "E", "S"}

mazes: list[list[str]] = []

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
            if cell in ALLOWED_CHARS:
                mazes[-1][i].append(cell if cell == " " else "#")
            else:
                raise ValueError("Maze incorretly constructed. " 
                                 + f"Invalid char '{cell}' in {file.path}")

    maze.close()