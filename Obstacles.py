import pygame 
from coords import *

class Tile(pygame.sprite.Sprite):
    position: tuple[int, int]
    surface: pygame.Surface
    rect: pygame.Rect

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect(center = coords_to_pixels(pos[0], pos[1]))
        self.position = (pos[0], pos[1])

class Wall(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image.fill('Blue')

class UnbreakableWall(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image.fill('Purple')

class Floor(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image.fill('Black')
