import pygame
from maze import mazes, MazeTemplate
from Obstacles import Wall, UnbreakableWall, Entrance, Exit, Floor
from Items import Points, Life
from professor import Professor
from classmate import Classmate
import random

class Game:
    def __init__(self, map = None, win = False, pause = False, difficulty = 50):
        self._map = map
        self._win = win
        self._pause = pause
        self._difficulty = difficulty
        self.floor_coord_list = []
        self.exit_tile = pygame.sprite.GroupSingle()
        self.entrance_tile = pygame.sprite.GroupSingle()
        self.map_borders = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.points_item = pygame.sprite.Group()
        self.lifes_item = pygame.sprite.Group()
        self.professor_group = pygame.sprite.Group()
        self.classmate_group = pygame.sprite.Group()

    @property
    def difficulty(self):
        return self._difficulty
    @difficulty.setter
    def difficulty(self, difficulty):
        self._difficulty = difficulty

    @property
    def pause(self):
        return self._pause
    
    @pause.setter
    def pause(self, pause):
        self._pause = pause


    @property
    def win(self):
        return self._win
    
    @win.setter
    def win(self, win):
        self._win = win

    @property
    def map(self):
        return self._map
    @map.setter
    def map(self, map):
        self._map = map

    def _pixels_to_coords(self, xy: tuple[int, int]):
        x = round((xy[0] - 12.5) // 25)
        y = round((xy[1] - 87.5) // 25)
        return x, y

    def _coords_to_pixels(self, xy: tuple[int, int]):
        x = xy[0] * 25 + 12.5
        y = xy[1] * 25 + 87.5
        return x, y

    def _place_map(self):
        if (not self.map) or (self.map not in mazes):
            self.map = random.choice(mazes)
        matrix = self.map.matrix

        for line_index, line in enumerate(matrix):
            for tile_index, tile in enumerate(line):
                tile = str(tile)
                coords = self._coords_to_pixels((tile_index, line_index))

                if tile == 'S':
                    exit_class = Exit(coords)
                    self.exit_tile.add(exit_class)
                elif tile == 'E':
                    self.entrance_tile.add(Entrance(coords))
                elif line_index == 0 or tile_index == 0 or line_index == len(matrix)-1 or tile_index == len(matrix[line_index])-1:
                    self.map_borders.add(UnbreakableWall(coords))
                elif tile == ' ':
                    self.floors.add(Floor(coords))
                    if coords[0] > 200:
                        self.floor_coord_list.append((coords, (line_index, tile_index)))
                elif tile == '#':
                    self.walls.add(Wall(coords))

    def _place_items(self):

        points_pos = random.sample(self.floor_coord_list, 5)
        for pos in points_pos:
            self.map.matrix[pos[1][0]][pos[1][1]] = 'P'
            self.points_item.add(Points(pos[0]))

        lifes_pos = random.sample(self.floor_coord_list, 5)
        for pos in lifes_pos:
            self.map.matrix[pos[1][0]][pos[1][1]] = 'L'
            self.lifes_item.add(Life(pos[0]))

    def _place_entities(self):
        professor_pos = random.sample(self.floor_coord_list, 2)
        for pos in professor_pos:
            self.map.matrix[pos[1][0]][pos[1][1]] = 'p'
            self.professor_group.add(Professor(pos[0]))
        classmate_pos = random.sample(self.floor_coord_list, 4)
        for pos in classmate_pos:
            self.map.matrix[pos[1][0]][pos[1][1]] = 'c'
            self.classmate_group.add(Classmate(pos[0]))
    
    def place_game(self):
        self._place_map()
        self._place_entities()
        self._place_items()

    def _clear_groups(self):
        self.classmate_group.empty()
        self.professor_group.empty()
        self.floors.empty()
        self.walls.empty()
        self.map_borders.empty()
        self.points_item.empty()
        self.lifes_item.empty()
        self.floor_coord_list.clear()
    
    def _remove_maze(self):
        mazes.remove(self.map)

    def new_game(self):
        self._clear_groups()
        self._remove_maze()
        self.place_game()

    def restart(self):
        self.classmate_group.empty()
        self.professor_group.empty()
        self.points_item.empty()
        self.lifes_item.empty()
        self.place_game()

    def start(self):
        self.place_game()
