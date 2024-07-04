from pygame.sprite import Sprite
from pygame import Surface

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return y, x

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[1] * 25 + 12.5
    y = xy[0] * 25 + 87.5
    return x, y

class Tile(Sprite):
    pos: tuple[int, int]

    def __init__(self, pos: tuple[int, int], size=20):
        super().__init__()
        self.pos = pos
        self.image = Surface((size, size))
        self.rect = self.image.get_rect(center = coords_to_pixels(pos))

    @property
    def center(self):
        return coords_to_pixels(self.pos)
