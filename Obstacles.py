import pygame 
from os import path

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.image.load(path.join('images', 'wall.png')).convert()
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.wall_coords = (pos[0], pos[1])

class UnbreakableWall(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.image.load(path.join('images', 'unbreakable_wall.png')).convert()
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.image.load(path.join('images', 'floor_tile.png')).convert()
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
