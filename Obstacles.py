import pygame 
from os import path

from Tile import Tile

imagePath = path.join("assets", "images")

#todos os obstáculos do jogo

class Wall(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, size=25)
        self.image = pygame.image.load(path.join(imagePath, 'wall.png')).convert()

class UnbreakableWall(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, size=25)
        self.image = pygame.image.load(path.join(imagePath, 'unbreakable_wall.png')).convert()

class Floor(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, size=25)
        self.image = pygame.image.load(path.join(imagePath, 'floor_tile.png')).convert()

class Entrance(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, size=25)
        self.image.fill('Green')

class Exit(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, size=25)
        self.image.fill('Red')