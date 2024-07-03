import pygame
from professor.pathfinder import backtracker

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return x, y

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[0] * 25 + 12.5
    y = xy[1] * 25 + 87.5
    return x, y

class Professor(pygame.sprite.Sprite):
    direction: bool
    speed: int
    route: list[int, int]

    @property
    def coords(self):
        return self.rect.center
    
    @property
    def matrix_coords(self):
        return pixels_to_coords(self.coords)

    def __init__(self, pos: tuple[int, int], speed = 2):
        super().__init__()
        self.image = pygame.Surface((11, 11))
        self.image.fill("Blue")
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.direction = True
        self.speed = speed
        self.route = []

    def follow_route(self):
        if len(self.route) <= 0:
            return

        xy = self.route[0]

        if pixels_to_coords(self.rect.center) == xy:
            del self.route[0]            
            return
        
        xy = coords_to_pixels(xy)
        self.walk_to(xy)

    def walk_to(self, xy: tuple[int, int]):

        vector = pygame.Vector2()
        dx, dy = xy[0] - self.rect.center[0], xy[1] - self.rect.center[1]
        vector.xy = dx, dy

        if dx == 0 and dy == 0:
            return

        vector = vector.normalize() * self.speed

        if dx > 0:
            vector.x = min(vector.x, dx)
        else:
            vector.x = max(vector.x, dx)

        if dy > 0:
            vector.y = min(vector.y, dy)
        else:
            vector.y = max(vector.y, dy)

        self.rect.center += vector

    def update_destination(self, matrix, destination: tuple[int, int]):
        if len(self.route) <= 0 or self.route[-1] != destination:
            coords = pixels_to_coords(self.rect.center)

            self.route = backtracker(matrix, pixels_to_coords(self.rect.center), 
                                     destination)

    def update(self):
        if len(self.route) == 0:
            return

        if len(self.route) > 0:
            self.follow_route()
        elif self.matrix_coords == self.route[-1]:
            self.route = []
