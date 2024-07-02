DIRECTIONS = { "R", "U", "L", "D" }

type point = tuple[int, int]

def define_directions(pos: point, destination: point):
    directions = [None] * 4
    x_delta = destination[0] - pos[0]
    y_delta = destination[1] - pos[1]

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

def backtracker(maze: list[list[str]], initial_pos: point,
                destination: point, path: list[point]=None):
    if path == None or len(path) <= 0:
        path = [initial_pos]

    line_len = len(maze[0])

    directions = define_directions(initial_pos, destination)

    if not _backtracker_inner(maze, destination, None, path, directions, first=True):
        raise ValueError("nao ta tendo :c e etc")

    del path[0]
    return path

def _backtracker_inner(maze: list[list[str]], destination: point,
                       direction: str, path: list[tuple[int, int]], directions, first=False):
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

    if maze[pos[1]][pos[0]] == "#":
        return False

    if pos in path and not first:
        return False

    path.append(pos)
    # print(path)

    if maze[pos[1]][pos[0]] == "S" or pos == destination:
        return True

    for next_direction in directions:
        if _backtracker_inner(maze, destination, next_direction, path, directions):
            return True

    path.pop()
    return False
