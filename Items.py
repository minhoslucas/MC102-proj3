import pygame
from os import path
from Tile import Tile

ITEM_PATH = path.join('assets', 'images', 'item_sprites')

class Item(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = pygame.Surface((20,20))

    def act(self, player=None, game=None):
        self.kill()

class Points(Item):
    def __init__(self, pos, value = 200):
        super().__init__(pos)
        self.image = pygame.image.load(path.join(ITEM_PATH, 'point_item_sprite.png'))
        self.value = value

    def act(self, player, game=None):
        player.points += self.value
        super().act()

class Life(Item):
    def __init__(self, pos, value = 1):
        super().__init__(pos)
        self.image = pygame.image.load(path.join(ITEM_PATH, 'life_item_sprite.png'))
        # self.image = pygame.transform.scale(self.image, (20,20))
        self.value = value

    def act(self, player, game=None):
        player.life += self.value
        super().act()

class Time(Item):
    def __init__(self, pos, value = 1):
        super().__init__(pos)
        self.image = pygame.image.load(path.join(ITEM_PATH, 'time_item_sprite.png'))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.value = value
        
    def act(self, player, game):
        game.extra_time += self.value
        super().act()
