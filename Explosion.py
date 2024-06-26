import pygame
from os import path
class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.explosion_animation = False
        self.explosion_hitbox = False
        self.animation_start_time = 0
        self.hitbox_start_time = 0

    def explode(self):
        self.animation_start_time = pygame.time.get_ticks()
        self.explosion_animation = True
        self.explode_hitbox()
        
    def explode_hitbox(self):
        self.explosion_animation_start_time = pygame.time.get_ticks()
        self.explosion_hitbox = True

    def update(self):
        if self.explosion_animation:
            current_time = pygame.time.get_ticks()
            delta_animation = current_time - self.animation_start_time
            delta_hitbox = current_time - self.explosion_animation_start_time
            if delta_animation >= 500:
                self.animation_start_time = 0
                self.explosion_animation = False
            if delta_hitbox >= 10:
                self.explosion_animation_start_time = 0
                self.explosion_hitbox = False
class ActiveBomb(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(path.join('images', 'black_bomb_sprite.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 20))
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
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
                self.image = pygame.image.load(path.join('images', 'red_bomb_sprite.png')).convert_alpha()
                self.image = pygame.transform.scale(self.image, (15, 20))
            elif (delta >= 1000 and delta < 1500) or (delta >= 2000 and delta < 2500):
                self.image = pygame.image.load(path.join('images', 'black_bomb_sprite.png')).convert_alpha()
                self.image = pygame.transform.scale(self.image, (15, 20))