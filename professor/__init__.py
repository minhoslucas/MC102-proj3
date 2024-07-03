import pygame
from professor.pathfinder import backtracker

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return y, x

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[1] * 25 + 12.5
    y = xy[0] * 25 + 87.5
    return x, y
        
class Professor(pygame.sprite.Sprite):
    direction: bool
    speed: int
    route: list[int, int]
    dest: tuple[int, int]
    _seen: bool

    @property
    def seen(self):
        return self._seen

    @seen.setter
    def seen(self, value):
        if (not self.seen) and value:
            self._seen = True
            # print("FOUND YOU")

    @property
    def pixels(self):
        return self.rect.center
    
    @property
    def coords(self):
        return pixels_to_coords(self.pixels)

    def __init__(self, pos: tuple[int, int], speed = 2):
        super().__init__()
        self.image = pygame.Surface((11, 11))
        self.image.fill("Blue")
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.direction = True
        self.speed = speed
        self.dest = None
        self.route = []
        self._seen = False

    def follow_route(self):
        if not self.seen:
            return

        if len(self.route) <= 0:
            return

        xy = self.route[0]

        if self.coords == xy:
            del self.route[0]           
            self.dest = None 
            return
        
        # print(xy, self.coords, end="   ")
        
        xy = coords_to_pixels(xy)
        # print(xy, self.pixels)
        self.dest = xy

    def walk_to(self, xy: tuple[int, int]):
        if not xy:
            return

        dx, dy = xy[0] - self.rect.center[0], xy[1] - self.rect.center[1]

        if dx == 0 and dy == 0:
            return

        vector = pygame.Vector2()
        vector.xy = dx, dy

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
        if self.seen and (len(self.route) <= 0 or self.route[-1] != destination):
            # print("UPDATE", self.coords, destination)
            # print(self.route)

            old_route = self.route
            self.route = []

            self.route = backtracker(matrix, self.coords, destination, 
                                     path=old_route)
            
    def update(self):
        if len(self.route) > 0:
            self.follow_route()

        self.walk_to(self.dest)
