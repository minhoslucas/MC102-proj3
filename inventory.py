import pygame
from os import path

FONT_PATH = path.join('assets', 'fonts', 'Clarity.otf')

class Inventory(pygame.sprite.Sprite):
    def __init__(self, bomb_count = 1):
        super().__init__()
        self.image = pygame.image.load(path.join('assets', 'images', 'inventory_sprites', 'inventory_slot.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = (900, 735))
        self._bomb_count = bomb_count

    @property
    def bomb_count(self):
        return self._bomb_count
    @bomb_count.setter
    def bomb_count(self, bomb_count):
        self._bomb_count = bomb_count

    def display_bomb_count(self, screen):
        text_font = pygame.font.Font(FONT_PATH, 10)
        if self.bomb_count > 0:
            text_surf = text_font.render(f'{self.bomb_count}', False, 'White')
            self.display_item(screen)
        else: text_surf = text_font.render(' ', False, 'White')
        text_rect = text_surf.get_rect(center = (910, 743))
        screen.blit(text_surf, text_rect)

    def display_item(self, screen):
        item_surf = pygame.image.load(path.join('assets', 'images', 'black_bomb_sprite.png'))
        item_surf = pygame.transform.scale(item_surf, (25, 25))
        item_rect = item_surf.get_rect(center = (900, 735))
        screen.blit(item_surf, item_rect)




    

    
