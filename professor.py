import pygame

class Professor(pygame.sprite.Sprite):
    direction: bool
    speed: int
    dest: tuple[int, int]
    
    @property
    def coords(self):
        return self.rect.center

    def __init__(self, pos: tuple[int, int], speed = 2):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill("Blue")
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.direction = True
        self.speed = speed
        self.dest = None

    def walk_to(self, xy: tuple[int, int]):
        if self.rect.center == xy:
            self.dest = None
            return

        if self.dest == None:
            self.dest = xy

        vector = pygame.Vector2()
        vector.xy = xy[0] - self.rect.center[0], xy[1] - self.rect.center[1]

        vector = vector.normalize() * self.speed

        self.rect.center += vector

    def update(self):
        if self.dest and self.dest != self.coords:
            self.walk_to(self.dest)