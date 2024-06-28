import pygame 

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill('Blue')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.wall_coords = (pos[0], pos[1])

class UnbreakableWall(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill('Purple')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill('Black')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
