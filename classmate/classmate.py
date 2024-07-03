import pygame

class Classmate(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], sprite: str):
        super().__init__()
        self.image = pygame.image.load(sprite).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
