import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.explosion = False
        self.start_time = 0

    def explode(self):
        self.start_time = pygame.time.get_ticks()
        self.explosion = True

    def update(self):
        if self.explosion:
            current_time = pygame.time.get_ticks()
            delta = current_time - self.start_time
            if delta >= 500:
                self.start_time = 0
                self.explosion = False
