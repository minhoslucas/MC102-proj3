import pygame
from os import path
from Obstacles import Tile
from maze.maze import maze

class Explosion(Tile):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image.fill('Red')

        for sprite in maze.all_sprites:
            if self.rect.colliderect(sprite.rect) and hasattr(sprite, "damage"):
                sprite.damage()

        self.start_time = pygame.time.get_ticks()
        self.animation_start = self.start_time
        self.animation_state = True

    def update(self):
        time = pygame.time.get_ticks()

        delta = time - self.start_time

        if delta >= 500:
            self.kill()
            return
        
        animation_delta = time - self.animation_start

        if animation_delta >= 60:
            self.animation_start = time
            self.animation_state = not self.animation_state

            if self.animation_state:
                self.image.fill("Red")
            else:
                self.image.fill("Orange")

class Bomb(Tile):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load(path.join('images', 'black_bomb_sprite.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 20))
        self.start_time = pygame.time.get_ticks()

    def explode(self):
        self.kill()
        coords = self.position
        maze.spawn(Explosion, coords)
        maze.spawn(Explosion, (coords[0], coords[1] + 1))
        maze.spawn(Explosion, (coords[0], coords[1] - 1))
        maze.spawn(Explosion, (coords[0] + 1, coords[1]))
        maze.spawn(Explosion, (coords[0] - 1, coords[1]))

    def update(self):
        delta = pygame.time.get_ticks() - self.start_time

        if delta >= 3000:
            self.explode()
            return

        if (delta >= 2500 and delta < 3000) \
            or (delta >= 1500 and delta < 2000) \
            or (delta >= 500 and delta < 1000):
            self.image = pygame.image \
                .load(path.join('images', 'red_bomb_sprite.png')) \
                .convert_alpha()
            self.image = pygame.transform.scale(self.image, (15, 20))
        elif (delta >= 1000 and delta < 1500) or (delta >= 2000 and delta < 2500):
            self.image = pygame.image \
                .load(path.join('images', 'black_bomb_sprite.png')) \
                .convert_alpha()
            self.image = pygame.transform.scale(self.image, (15, 20))
