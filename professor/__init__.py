import pygame
from professor.pathfinder import backtracker
from os import path

from Tile import Tile

PROFESSOR_SPRITES_FOLDER = path.join('assets', 'images', 'professor_sprites')

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return y, x

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[1] * 25 + 12.5
    y = xy[0] * 25 + 87.5
    return x, y
        
class Professor(Tile):
    direction: bool
    speed: int
    route: list[int, int]
    dest: tuple[int, int]
    _seen: bool

    @property
    def seen(self):
        return self._seen

    @seen.setter
    def seen(self, value):
        if (not self.seen) and value:
            self._seen = True
            # print("FOUND YOU")

    @property
    def pixels(self):
        return self.rect.center
    
    @property
    def coords(self):
        return pixels_to_coords(self.pixels)

    def __init__(self, pos: tuple[int, int], speed = 2):
        super().__init__(pos, size=11)
        self.direction = True
        self.image = pygame.image.load(path.join(PROFESSOR_SPRITES_FOLDER, 'professor_bot_still.png'))
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = coords_to_pixels(pos))
        self.speed = speed
        self.dest = None
        self.route = []
        self._seen = False

    def follow_route(self):
        if not self.seen:
            return

        if len(self.route) <= 0:
            return

        xy = self.route[0]

        if self.coords == xy:
            del self.route[0]           
            self.dest = None 
            return
        
        # print(xy, self.coords, end="   ")
        
        xy = coords_to_pixels(xy)
        # print(xy, self.pixels)
        self.dest = xy

    def walk_to(self, xy: tuple[int, int]):
        if not xy:
            return

        dx, dy = xy[0] - self.rect.center[0], xy[1] - self.rect.center[1]

        if dx == 0 and dy == 0:
            return

        vector = pygame.Vector2()
        vector.xy = dx, dy

        vector = vector.normalize() * self.speed

        if vector.xy != (0, 0):
            self.set_animation_sprite(1, vector.y)
            self.set_animation_sprite(0, vector.x)

        if dx > 0:
            vector.x = min(vector.x, dx)
        else:
            vector.x = max(vector.x, dx)

        if dy > 0:
            vector.y = min(vector.y, dy)
        else:
            vector.y = max(vector.y, dy)
            
        self.rect.center += vector

    def update_destination(self, matrix, destination: tuple[int, int]):
        if self.seen and (len(self.route) <= 0 or self.route[-1] != destination):
            # print("UPDATE", self.coords, destination)
            # print(self.route)

            old_route = self.route
            self.route = []

            self.route = backtracker(matrix, self.coords, destination, 
                                     path=old_route)
            
    def _animate(self, path_list: tuple[str, str, str], time: int, flip: bool = False):
        if (time%400 >= 0 and time%400 < 100) or (time%400 >= 200 and time%400 < 300): 
            self.image = pygame.image.load(path.join(PROFESSOR_SPRITES_FOLDER, path_list[0]))
            if flip: self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (25, 25))
        elif (time%400 >= 100 and time%400 < 200):
            self.image = pygame.image.load(path.join(PROFESSOR_SPRITES_FOLDER, path_list[1]))
            if flip: self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (25, 25))
        elif (time%400 >= 300 and time%400 < 400):
            self.image = pygame.image.load(path.join(PROFESSOR_SPRITES_FOLDER, path_list[2]))
            if flip: self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (25, 25))

    def set_animation_sprite(self, axis, movement):
        time = pygame.time.get_ticks()
        if axis == 0 and movement < 0:
            path_list = ('professor_left_still.png', 'professor_left_frame_1.png', 'professor_left_frame_2.png')
            self._animate(path_list, time)
        elif axis == 0 and movement > 0:
            path_list = ('professor_left_still.png', 'professor_left_frame_1.png', 'professor_left_frame_2.png')
            self._animate(path_list, time, True)
        elif axis == 1 and movement > 0:
            path_list = ('professor_bot_still.png', 'professor_bot_frame_1.png', 'professor_bot_frame_2.png')
            self._animate(path_list, time)
        elif axis == 1 and movement < 0:
            path_list = ('professor_top_still.png', 'professor_top_frame_1.png', 'professor_top_frame_2.png')
            self._animate(path_list, time)
            
    def update(self):
        if len(self.route) > 0:
            self.follow_route()

        self.walk_to(self.dest)
