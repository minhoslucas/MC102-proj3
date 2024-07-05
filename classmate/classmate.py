import pygame

from Tile import Tile, coords_to_pixels

#colegas perdidos no labirinto

class Classmate(Tile):
    def __init__(self, pos: tuple[int, int], sprite: str):
        super().__init__(pos, size=20)
        self.image = pygame.image.load(sprite).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = coords_to_pixels(pos))
