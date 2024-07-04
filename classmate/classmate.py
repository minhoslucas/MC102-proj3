import pygame

from Tile import Tile

class Classmate(Tile):
    def __init__(self, pos: tuple[int, int], sprite: str):
        super().__init__(pos, size=20)
        self.image = pygame.image.load(sprite).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
