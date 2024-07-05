import pygame
from pygame.sprite import Group, GroupSingle
from os import path
from itertools import chain
from maze import mazes, MazeTemplate
from Obstacles import Wall, UnbreakableWall, Entrance, Exit, Floor
from Items import Points, Life, Time
from professor import Professor
from inventory import Inventory
from classmate.classmate import Classmate
from classmate.reader import classmate_sprites_list
import random

FONT_PATH = path.join('assets', 'fonts', 'Clarity.otf')

def load(*args):
    return pygame.image.load(path.join(*args)).convert_alpha()

class Game:
    _map: MazeTemplate
    walls: Group
    map_borders: Group
    floors: Group
    professor_group: Group
    classmate_group: Group

    def __init__(self, map = None, win = False, pause = False, over = False, restart = False, difficulty = 2, time = 0, level = 1):
        self._map = map
        self._win = win
        self._pause = pause
        self._over = over
        self._restart = restart
        self._time = time
        self._level = level
        self.mazes = mazes
        self.all_mazes = self.mazes.copy()
        self.extra_time = 0
        self._difficulty = difficulty
        self.floor_coord_list = []
        self.exit_tile = pygame.sprite.GroupSingle()
        self.entrance_tile = pygame.sprite.GroupSingle()
        self.map_borders = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.professor_group = pygame.sprite.Group()
        self.classmate_group = pygame.sprite.Group()
        self.inventory_slot_group = pygame.sprite.Group()
        self.inventory_slot = Inventory()

    @property
    def restart(self):
        return self._restart
    @restart.setter
    def restart(self, restart):
        self._restart = restart

    @property
    def matrix(self):
        return self._map.matrix

    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, level):
        self._level = level

    @property
    def over(self):
        return self._over
    @over.setter
    def over(self, over):
        self._over = over

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, time):
        self._time = time

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
    
    def display_timer(self, screen,  time_limit = 120, start_time = 0):
        text_font = pygame.font.Font(FONT_PATH, 20)
        self.time = start_time + time_limit - pygame.time.get_ticks()//1000
        self.time += 10*self.extra_time

        if self.time <= 0:
            self.over = True
        if self.time%60 < 10:
            timer_surf = text_font.render(f'Time: {self.time//60}:0{self.time%60}', False, 'White')
        else:
            timer_surf = text_font.render(f'Time: {self.time//60}:{self.time%60}', False, 'White')
        timer_rect = timer_surf.get_rect(center = (675, 50))
        screen.blit(timer_surf, timer_rect)

    def display_life_count(self, screen, life_count):
        surface_path = path.join('assets', 'images', 'life_count_sprites')
        life_surf = load(surface_path, f'life_count_{life_count}.png')
        life_rect = life_surf.get_rect(midleft = (200, 40))
        screen.blit(life_surf, life_rect)

    def set_wallpaper(self, screen):
        wallpaper_surf = pygame.image.load(path.join('assets', 'images', 'background_tile.png'))
        for i in range(20):
            for j in range(16):
                wallpaper_rect = wallpaper_surf.get_rect(center = (i*50 + 25, j*50 + 25))
                screen.blit(wallpaper_surf, wallpaper_rect)

    def display_level(self, screen):
        text_font = pygame.font.Font(FONT_PATH, 20)
        level_surf = text_font.render(f'Level: {self.level}', False, 'White')
        level_rect = level_surf.get_rect(center = (75, 735))
        screen.blit(level_surf, level_rect)

    def _place_map(self):
        if self.over or (not self.map):
            self.map = random.choice(self.all_mazes)
            self.mazes = self.all_mazes.copy()
        elif self.restart:
            pass
        elif self.map not in self.mazes:
            self.map = random.choice(self.mazes)

        matrix = self.map.matrix

        for line_index, line in enumerate(matrix):
            for tile_index, tile in enumerate(line):
                tile = str(tile)
                coords = (line_index, tile_index)

                if tile == 'S':
                    exit_class = Exit(coords)
                    self.exit_tile.add(exit_class)
                elif tile == 'E':
                    self.entrance_tile.add(Entrance(coords))
                elif line_index == 0 or tile_index == 0 or line_index == len(matrix)-1 or tile_index == len(matrix[line_index])-1:
                    self.map_borders.add(UnbreakableWall(coords))
                elif tile == '#':
                    self.walls.add(Wall(coords))
                elif tile == ' ':
                    self.floors.add(Floor(coords))
                    self.floor_coord_list.append(coords)
        
        for wall in self.walls.sprites():  #remove na marra os tiles com overlapping
            for tile in self.floor_coord_list:
                if wall.pos == tile[0]:
                   self.floor_coord_list.remove(tile)

    def _place_items(self):
        points_pos = random.sample(self.floor_coord_list, 5)
        for pos in points_pos:
            self.floor_coord_list.remove(pos)
            self.items.add(Points(pos))

        lifes_pos = random.sample(self.floor_coord_list, 5)
        for pos in lifes_pos:
            self.floor_coord_list.remove(pos)
            self.items.add(Life(pos))

        time_pos = random.sample(self.floor_coord_list, 3)
        for pos in time_pos:
            self.floor_coord_list.remove(pos)
            self.items.add(Time(pos))

    def _place_entities(self):
        if self.difficulty == 3:
            num_prof = 4
            num_class = 4
            prof_speed = 3
        elif self.difficulty == 2:
            num_prof = 3
            num_class = 4
            prof_speed = 2
        else:
            num_prof = 2
            num_class = 3
            prof_speed = 1

        professor_pos = random.sample(self.floor_coord_list, num_prof)
        for pos in professor_pos:
            print(pos)
            self.professor_group.add(Professor(pos, prof_speed))

        classmate_pos = random.sample(self.floor_coord_list, num_class)
        classmate_sprites = random.sample(classmate_sprites_list, num_class)
        for ind, pos in enumerate(classmate_pos):
            self.classmate_group.add(Classmate(pos, classmate_sprites[ind]))

    def _load_inventory_slot(self):
        self.inventory_slot_group.add(self.inventory_slot)
    
    def place_game(self):
        self._place_map()
        self._place_entities()
        self._place_items()
        self._load_inventory_slot()

    def _clear_groups(self):
        self.classmate_group.empty()
        self.professor_group.empty()
        self.floors.empty()
        self.walls.empty()
        self.map_borders.empty()
        self.items.empty()
        self.inventory_slot_group.empty()
        self.floor_coord_list = []
    
    def _remove_maze(self):
        self.mazes.remove(self.map)

    def new_game(self):
        self._clear_groups()
        self._remove_maze()
        self.place_game()

    def full_restart(self):
        self.classmate_group.empty()
        self.professor_group.empty()
        self.items.empty()
        self.inventory_slot_group.empty()
        self.floor_coord_list = []
        self.place_game()

    def restart_game(self):
        self.classmate_group.empty()
        self.professor_group.empty()
        self.items.empty()
        self.inventory_slot_group.empty()
        self.place_game()

    def start(self):
        self.place_game()
