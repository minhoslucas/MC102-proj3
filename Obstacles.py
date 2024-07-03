import pygame 
from os import path

imagePath = path.join("assets", "images")

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.image.load(path.join(imagePath, 'wall.png')).convert()
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.wall_coords = pos

class UnbreakableWall(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.image.load(path.join(imagePath, 'unbreakable_wall.png')).convert()
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.image.load(path.join(imagePath, 'floor_tile.png')).convert()
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.floor_coords = pos

class Entrance(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill('Green')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

class Exit(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))   