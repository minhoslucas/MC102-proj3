from Obstacles import Floor, Wall, UnbreakableWall
from pygame import sprite
from reader import mazes
from random import choice
from itertools import chain

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return x, y

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[0] * 25 + 12.5
    y = xy[1] * 25 + 87.5
    return x, y

class Maze():
    _walls: sprite.Group[Wall]
    _border: sprite.Group[UnbreakableWall]
    _floors: sprite.Group[Floor]
    _misc: sprite.Group

    def __init__(self, map_index: int):
        map_matrix = mazes[map_matrix]

    @property
    def floor(self):
        return self._floors.sprites

    @property
    def walls(self):
        return self._walls.sprites
    
    @property 
    def borders(self):
        return self._border.sprites

    @property
    def all_walls(self):
        return chain(self.walls, self.borders)
    
    @property
    def all_sprites(self):
        return chain(self.walls, self.borders, self._misc.sprites)

    def _load_matrix(self, maze: list[list[str]]):
        for i, line in enumerate(maze):
            for j, tile in enumerate(line):
                tile = str(tile)
                coords = (i, j)

                if i == 0 or j == 0 or i == len(maze)-1 or j == len(maze[i])-1:
                    self._borders.add(UnbreakableWall(coords))
                elif tile == ' ':
                    self._floors.add(Floor(coords))
                elif tile == '#':
                    self._walls.add(Wall(coords))

    def spread(self, sprite, amount: int):
        """Takes a sprite constructor and spawns a set number of the 
           sprite instances on the board."""
        pass

    def spawn(self, sprite, coords: tuple[int, int]):
        element = sprite(coords)
        self._misc.add(element)

    def draw(self):
        self._walls.draw()
        self._border.draw()

maze = Maze(0)

#escolhe posições livres do tabuleiro e plota 5 itens points e life
# points_pos = random.sample(floor_coords, 5)
# for pos in points_pos:
#     map[pos[1][0]][pos[1][1]] = 'P'
#     points_item.add(Points(pos[0]))

# lifes_pos = random.sample(floor_coords, 5)
# for pos in lifes_pos:
#     map[pos[1][0]][pos[1][1]] = 'L'
#     lifes_item.add(Life(pos[0]))
