DIRECTIONS = { "R", "U", "L", "D" }

def define_directions(pos: tuple[int, int], destination: tuple[int, int]):
    directions = [None] * 4
    x_delta = destination[0] - pos[0]
    y_delta = destination[1] - pos[1]

    if x_delta == 0 and y_delta == 0:
        return list(DIRECTIONS)

    offset = 0 if abs(x_delta) >= abs(y_delta) else 1

    if x_delta <= 0:
        directions[0 + offset] = "U"
        directions[2 + offset] = "D"
    else:
        directions[0 + offset] = "D"
        directions[2 + offset] = "U"

    if y_delta <= 0:
        directions[1 - offset] = "L"
        directions[3 - offset] = "R"
    else:
        directions[1 - offset] = "R"
        directions[3 - offset] = "L"

    return directions

def backtracker(maze: list[list[str]], initial_pos: tuple[int, int],
                destination: tuple[int, int], path: list[tuple[int, int]]=None):
    if path == None or len(path) <= 0:
        path = [initial_pos]

    line_len = len(maze[0])

    # print("START", initial_pos, destination)

    if not _backtracker_inner(maze, destination, None, path, first=True):
        # print("ERRO", end="")
        # print(initial_pos, destination, end="")
        # i_tile = maze[initial_pos[0]][initial_pos[1]]
        # d_tile = maze[destination[0]][destination[1]]
        # print((i_tile, initial_pos), (d_tile, destination))
        return []

    del path[0]
    return path

def _backtracker_inner(maze: list[list[str]], destination: tuple[int, int],
                       direction: str, path: list[tuple[int, int]], first=False):
    pos = path[-1]

    if direction == "D":
        pos = (pos[0]+1, pos[1])
    elif direction == "U":
        pos = (pos[0]-1, pos[1])
    elif direction == "L":
        pos = (pos[0], pos[1]-1)
    elif direction == "R":
        pos = (pos[0], pos[1]+1)

    if pos[0] < 0 or pos[1] < 0:
        return False

    if not first and maze[pos[0]][pos[1]] in { "#", "E", "S" }:
        return False

    if not first and pos in path:
        # print(path)
        return False

    path.append(pos)

    # print_maze(maze, "caminho.out", pos, time=1)

    if pos == destination:
        return True

    directions = define_directions(pos, destination)
    # print(directions)

    # print(pos, destination)

    for next_direction in directions:
        if _backtracker_inner(maze, destination, next_direction, path):
            return True

    path.pop()
    return False