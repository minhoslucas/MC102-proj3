import pygame

class Classmate(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill('Gray')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        