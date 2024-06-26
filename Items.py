import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
class Points(Item, pygame.sprite.Sprite):
    def __init__(self, pos, value = 200):
        super().__init__(pos)
        self.image.fill('Green')
        self._value = value
class Life(Item, pygame.sprite.Sprite):
    def __init__(self, pos, value = 1):
        super().__init__(pos)
        self.image.fill('Orange')
        self._value = value
class ActiveBomb(Item, pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(pos)
        self.image.fill('Yellow')
        self.start_time = 0
        self.active = False
        self.bomb_coords = (pos[0], pos[1])

    def activate(self):
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def deactivate(self):
        self.start_time = 0
        self.active = False

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            delta = current_time - self.start_time
            if delta >= 3000:
                self.deactivate()
            elif (delta >= 2500 and delta < 3000) or (delta >= 1500 and delta < 2000) or (delta >= 500 and delta < 1000):
                self.image.fill('Red')
            elif (delta >= 1000 and delta < 1500) or (delta >= 2000 and delta < 2500):
                self.image.fill('Yellow')





    
        
        
        
    
    