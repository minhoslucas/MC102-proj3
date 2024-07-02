import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((12.5, 12.5))
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        
class Points(Item):
    def __init__(self, pos, value = 200):
        super().__init__(pos)
        self.image.fill('Green')
        self._value = value

class Life(Item):
    def __init__(self, pos, value = 1):
        super().__init__(pos)
        self.image.fill('Orange')
        self._value = value

class Time(Item):
    def __init__(self, pos, value = 1):
        super().__init__(pos)
        self.image.fill('Purple')
        self._value = value
