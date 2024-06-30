import pygame 
import random
from sys import exit
from os import path
from Obstacles import Wall, UnbreakableWall, Floor
from Explosion import  Explosion, ActiveBomb
from Items import Points, Life
from maze import mazes
from itertools import chain
from professor import Professor
from menus import StartButton, QuitButton

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return x, y

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[0] * 25 + 12.5
    y = xy[1] * 25 + 87.5
    return x, y

class Player(pygame.sprite.Sprite):
    def __init__(self, life = 6, points = 0, coords = (1, 6), bomb_cooldown = 0):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center = (75, 375))
        self._life = life
        self._points = points
        self._coords = coords
        self._bomb_cooldown = bomb_cooldown
        self.invincible = False
        self.start_time = 0

    @property
    def points(self):
        return self._points
    @points.setter
    def points(self, points):
        self._points = points
    
    @property
    def life(self):
        return self._life
    @life.setter
    def life(self, life):
        self._life = life

    @property
    def coords(self):
        return self._coords
    @coords.setter
    def coords(self, coords):
        self._coords = coords
    
    @property
    def bomb_cooldown(self):
        return self._bomb_cooldown
    @bomb_cooldown.setter
    def bomb_cooldown(self, bomb_cooldown):
        self._bomb_cooldown = bomb_cooldown

    #Checa os inputs do teclado para player
    def player_input(self):
        keys = pygame.key.get_pressed()

        vector = pygame.Vector2()
        vector.xy = 0, 0

        if keys[pygame.K_s]:
            vector.y += 3
        if keys[pygame.K_w]:
            vector.y -= 3

        if keys[pygame.K_d]:
            vector.x += 3
        if keys[pygame.K_a]:
            vector.x -= 3

        if vector.xy != (0, 0):
            vector = vector.normalize() * 3
            self.check_wall_colisions(vector)

        if keys[pygame.K_SPACE]:
            if self.bomb_cooldown == 0:
                self.place_bomb()

    #Impede que o player saia da tela
    def screen_limits(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > 1000:
            self.rect.right = 1000
        if self.rect.bottom > 1000:
            self.rect.bottom = 1000

    #Checa as colisões de player com paredes
    def check_wall_colisions(self, vector: pygame.Vector2):
        self._move(vector.x, 0)
        self._move(vector.y, 1)

    def _move(self, movement: int, axis: str):
        if axis == 0:
            self.rect.x += movement
        else:
            self.rect.y += movement

        for wall in chain(walls.sprites(), map_borders.sprites()):
            if self.rect.colliderect(wall.rect):
                if axis == 0:
                    if movement > 0:
                        self.rect.right = wall.rect.left
                    else:
                        self.rect.left = wall.rect.right
                else:
                    if movement > 0: 
                        self.rect.bottom = wall.rect.top
                    else: 
                        self.rect.top = wall.rect.bottom

        for floor in floors.sprites():
            if self.rect.colliderect(floor.rect):
                self.coords = pixels_to_coords(floor.rect.center)

    #Checa por colisões de player com itens ou explosões
    def check_colisions(self):
        for item in points_item.sprites():
            if self.rect.colliderect(item.rect):
                self.points += item._value
                pygame.sprite.Sprite.kill(item)

        for item in lifes_item.sprites():
            if self.rect.colliderect(item.rect):
                pygame.sprite.Sprite.kill(item)

                if self.life < 6:
                    self.life += item._value

        if len(explosions.sprites()) > 0:
            for explosion in explosions.sprites():
                if self.rect.colliderect(explosion.rect) and explosion.explosion_hitbox:
                    self.damage()

        # if self.rect.colliderect(professor.rect):
        #     self.damage()

    #Dá dano em player
    def damage(self):
        if not self.invincible:
            self.life -= 1
            self.activate_timer()
        
    #Coloca uma bomba no mapa
    def place_bomb(self):
        x_coords = (self.coords[0]*25) + 12.5
        y_coords = (self.coords[1]*25) + 87.5

        bomb = ActiveBomb((x_coords, y_coords))
        bombs_item.add(bomb)
        bomb.activate()

        self.bomb_cooldown = 1

    #Ativa o timer de invincibilidade
    def activate_timer(self):
        self.start_time = pygame.time.get_ticks()
        self.invincible = True

    #Timer de invincibilidade de player após levar dano da bomba
    def invincible_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            delta = current_time - self.start_time
            if delta >= 2000:
                self.start_time = 0
                self.invincible = False

    #Função UPDATE, atualizada o tempo todo no Game Loop
    def update(self):
        self.invincible_timer()
        self.check_colisions()
        self.player_input()
        self.screen_limits()

#Desenha a pontação na tela
def display_score():
    text_font = pygame.font.Font(None, 30)
    score_surf = text_font.render(f'Score: {player_class.points}', True, 'White')
    score_rect = score_surf.get_rect(center = (75, 50))
    screen.blit(score_surf, score_rect)

#Desenha a contagem de vidas na tela
def display_life_count():
    text_font = pygame.font.Font(None, 30)
    life_surf = text_font.render(f'Life Count: {player_class.life}', True, 'White')
    life_rect = life_surf.get_rect(center = (275, 50))
    screen.blit(life_surf, life_rect)

def check_life_count():
    if player_class.life == 0:
        return False
    return True

#Desenha as coordenadas na tela
def display_coords():
    text_font = pygame.font.Font(None, 30)
    coords_surf = text_font.render(f'Coords: {player_class.coords}', True, 'White')
    coords_rect = coords_surf.get_rect(center = (475, 50))
    screen.blit(coords_surf, coords_rect)

#Desenha o timer na tela
def display_timer(time_limit = 120):
    text_font = pygame.font.Font(None, 30)
    real_time = time_limit - pygame.time.get_ticks()//1000

    if real_time <= 0:
        player_class.rect.center = (75, 375)
        return False
    if real_time%60 < 10:
        timer_surf = text_font.render(f'Time: {real_time//60}:0{real_time%60}', True, 'White')
    else:
        timer_surf = text_font.render(f'Time: {real_time//60}:{real_time%60}', True, 'White')
    timer_rect = timer_surf.get_rect(center = (675, 50))
    screen.blit(timer_surf, timer_rect)
    return True

#Desenha a tela de GAME OVER
def display_game_over():
    text_font = pygame.font.Font(None, 200)
    game_over_surf = text_font.render('GAME OVER', True, 'White')
    game_over_rect = game_over_surf.get_rect(center = (500, 388))
    screen.blit(game_over_surf, game_over_rect)

#Define a área afetada pela bomba
def set_explosion(bomb):
    explosions.add(Explosion((bomb.bomb_coords)))
    explosions.add(Explosion((bomb.bomb_coords[0]+25, bomb.bomb_coords[1])))
    explosions.add(Explosion((bomb.bomb_coords[0]-25, bomb.bomb_coords[1])))
    explosions.add(Explosion((bomb.bomb_coords[0], bomb.bomb_coords[1]+25)))
    explosions.add(Explosion((bomb.bomb_coords[0], bomb.bomb_coords[1]-25)))
    for explosion in explosions.sprites():
        explosion.explode()

#Checa as colisões da bomba em relação à outros obstáculos
def explosion_damage():
    for explosion in explosions.sprites():
        for wall in walls.sprites():
            if explosion.rect.colliderect(wall.rect):
                coords = wall.wall_coords
                pygame.sprite.Sprite.kill(wall)
                floors.add(Floor(coords))

#Mata a explosão depos que acabar o timer dela
def kill_explosion():
    if len(explosions.sprites()) > 0:
        for explosion in explosions.sprites():
            if not explosion.explosion_animation:
                pygame.sprite.Sprite.kill(explosion) 

#Mata a bomba depois que acabar o timer dela
def kill_bomb():
    if len(bombs_item.sprites()) > 0:
        bomb = bombs_item.sprites()[0]
        if not bomb.active:
            player_class.bomb_cooldown = 0
            set_explosion(bomb)
            pygame.sprite.Sprite.kill(bomb)

SCREEN_WIDTH = 1000
SCREEN_HIGHT = 775

pygame.init()

game_active = False
game_over = False
main_menu = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Os Labirintos da Unicamp')

#Coloca o plano de fundo
background_surface = pygame.image.load(path.join('images', 'stone_background.jpg')).convert()

#Cria um grupo para player
player = pygame.sprite.GroupSingle()
player_class = Player()
player.add(player_class)

#Cria um grupo para todos os obtáculos e itens do jogo
walls = pygame.sprite.Group()
map_borders = pygame.sprite.Group()
floors = pygame.sprite.Group()
explosions = pygame.sprite.Group()

points_item = pygame.sprite.Group()
lifes_item = pygame.sprite.Group()
bombs_item = pygame.sprite.Group()

professor = Professor(coords_to_pixels((2, 10)), speed=2)
professor_group = pygame.sprite.GroupSingle()
professor_group.add(professor)

buttons = pygame.sprite.Group()
start_button = StartButton((250, 388))
quit_button = QuitButton((750, 388))
buttons.add(quit_button)
buttons.add(start_button)

#Mapa do labirinto
map = random.choice(mazes)

floor_coord_list = []
#Coloca os obstáculos nas suas respectivas posições
for line_index, line in enumerate(map):
    for tile_index, tile in enumerate(line):
        tile = str(tile)
        coords = coords_to_pixels((tile_index, line_index))

        if line_index == 0 or tile_index == 0 or line_index == len(map)-1 or tile_index == len(map[line_index])-1:
            map_borders.add(UnbreakableWall(coords))

        elif tile == ' ':
            floors.add(Floor(coords))
            if coords[0] > 200:
                floor_coord_list.append((coords, (line_index, tile_index)))

        elif tile == '#':
            walls.add(Wall(coords))

#escolhe posições livres do tabuleiro e plota 5 itens points e life
points_pos = random.sample(floor_coord_list, 5)
for pos in points_pos:
    map[pos[1][0]][pos[1][1]] = 'P'
    points_item.add(Points(pos[0]))

lifes_pos = random.sample(floor_coord_list, 5)
for pos in lifes_pos:
    map[pos[1][0]][pos[1][1]] = 'L'
    lifes_item.add(Life(pos[0]))

#Game Loop
while True:
    if game_active:
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            #Plota na tela o plano de fundo e player
            screen.blit(background_surface, (0,0))
            screen.fill('Black')   
            floors.draw(screen)

            #Atualiza player e o timer da bomba/explosão
            player.update()
            bombs_item.update()
            explosions.update()

            #Plota as coisas dependendo da matriz
            walls.draw(screen)
            map_borders.draw(screen)
            player.draw(screen)
            points_item.draw(screen)
            lifes_item.draw(screen)
            bombs_item.draw(screen)
            explosions.draw(screen)
            professor_group.draw(screen)

            professor.dest = player_class.rect.center

            professor_group.update()

            #Desenham a pontuação, vida, coordenadas, e tempo 
            display_score()
            display_life_count()
            display_coords()
            if not display_timer() or not check_life_count(): #Tempo em segundos, por padrão, 2 minutos
                game_over = True
                game_active = False
                break

            #Configurações da bomba
            explosion_damage()
            kill_explosion()
            kill_bomb()

            #Atualiza o jogo constantemente
            pygame.display.update()
            clock.tick(60)

    elif game_over:
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            #Plota na tela o plano de fundo
            screen.blit(background_surface, (0,0))
            screen.fill('Black')

            #Desenha a tela de GAME OVER
            display_game_over()

            pygame.display.update()
            clock.tick(60)
    elif main_menu:
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.blit(background_surface, (0, 0))
            screen.fill('Black')

            buttons.update()
            buttons.draw(screen)

            if start_button.is_clicked == True:
                main_menu = False
                game_active = True
                break
            elif quit_button.is_clicked == True:
                pygame.quit()
                exit()
       
            pygame.display.update()
            clock.tick(60)
        
