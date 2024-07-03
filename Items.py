import pygame
from os import path

class Item(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        
class Points(Item):
    def __init__(self, pos, value = 200):
        super().__init__(pos)
        self.image = pygame.image.load(path.join('assets', 'images', 'item_sprites', 'point_item_sprite.png'))
        self._value = value

class Life(Item):
    def __init__(self, pos, value = 1):
        super().__init__(pos)
        self.image = pygame.image.load(path.join('assets', 'images', 'item_sprites', 'life_item_sprite.png'))
        # self.image = pygame.transform.scale(self.image, (20,20))
        self._value = value

class Time(Item):
    def __init__(self, pos, value = 1):
        super().__init__(pos)
        self.image = pygame.image.load(path.join('assets', 'images', 'item_sprites', 'time_item_sprite.png'))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self._value = value
