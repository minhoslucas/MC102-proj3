import pygame 
import random
from sys import exit
from Obstacles import Wall, UnbreakableWall, Floor
from Explosion import  Explosion
from Items import Points, Life, ActiveBomb
from maze import mazes

class Player(pygame.sprite.Sprite):
    def __init__(self, life = 6, points = 0, coords = (1, 6), bomb_cooldown = 0):
        super().__init__()
        self.image = pygame.Surface((25,25))
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
        if keys[pygame.K_w]:
            self.check_wall_colisions(0, -5)
        if keys[pygame.K_a]:
            self.check_wall_colisions(-5, 0)
        if keys[pygame.K_s]:
            self.check_wall_colisions(0, 5)
        if keys[pygame.K_d]:
            self.check_wall_colisions(5, 0)
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
    def check_wall_colisions(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in walls.sprites():
            if self.rect.colliderect(wall.rect):
                    if dx > 0: 
                        self.rect.right = wall.rect.left
                    if dx < 0: 
                        self.rect.left = wall.rect.right
                    if dy > 0: 
                        self.rect.bottom = wall.rect.top
                    if dy < 0: 
                        self.rect.top = wall.rect.bottom

        for unbreakable_wall in map_borders.sprites():
            if self.rect.colliderect(unbreakable_wall.rect):
                if dx > 0: 
                    self.rect.right = unbreakable_wall.rect.left
                if dx < 0: 
                    self.rect.left = unbreakable_wall.rect.right
                if dy > 0: 
                    self.rect.bottom = unbreakable_wall.rect.top
                if dy < 0: 
                    self.rect.top = unbreakable_wall.rect.bottom

    #Checa por colisões de player com itens ou explosões
    def check_colisions(self):
        for floor in floors.sprites():
            if self.rect.colliderect(floor.rect):
                x_coords = (floor.rect.centerx - 25)//50
                y_coords = (floor.rect.centery - 100)//50
                self.coords = (x_coords, y_coords)

        for item in points_item.sprites():
            if self.rect.colliderect(item.rect):
                self.points += item._value
                pygame.sprite.Sprite.kill(item)

        for item in lifes_item.sprites():
            if self.rect.colliderect(item.rect):
                if self.life == 6:
                    pygame.sprite.Sprite.kill(item)
                else:
                    self.life += item._value
                    pygame.sprite.Sprite.kill(item)

        if len(explosions.sprites()) > 0:
            for explosion in explosions.sprites():
                if self.rect.colliderect(explosion.rect):
                    if not self.invincible:
                        self.life -= 1
                        self.activate_timer()

    #Coloca uma bomba no mapa
    def place_bomb(self):
        x_coords = (self.coords[0]*50) + 25
        y_coords = (self.coords[1]*50) + 100

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
    explosions.add(Explosion((bomb.bomb_coords[0]+50, bomb.bomb_coords[1])))
    explosions.add(Explosion((bomb.bomb_coords[0]-50, bomb.bomb_coords[1])))
    explosions.add(Explosion((bomb.bomb_coords[0], bomb.bomb_coords[1]+50)))
    explosions.add(Explosion((bomb.bomb_coords[0], bomb.bomb_coords[1]-50)))
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
            if not explosion.explosion:
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

game_active = True
game_over = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Os Labirintos da Unicamp')

#Coloca o plano de fundo
background_surface = pygame.image.load('images\stone_background.jpg')

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


#Mapa do labirinto
map = random.choice(mazes)

#Coloca os itens em seus respectivos grupos dependendo do mapa
for line_index in range(len(map)):
    for tile_index in range(len(map[line_index])):
        tile = str(map[line_index][tile_index])
        coords = ((tile_index*50) + 25, (line_index*50) + 100)

        if line_index == 0 or tile_index == 0 or line_index == len(map)-1 or tile_index == len(map[line_index])-1:
            map_borders.add(UnbreakableWall(coords))

        elif tile == ' ':
            floors.add(Floor(coords))

        elif tile == '#':
            walls.add(Wall(coords))

        elif tile == 'P':
            floors.add(Floor(coords))
            points_item.add(Points(coords))

        elif tile == 'L':
            floors.add(Floor(coords))
            lifes_item.add(Life(coords))



#Game Loop
if game_active:
    while True:
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                pygame.quit()
                exit()

        #Plota na tela o plano de fundo e player
        screen.blit(background_surface, (0,0))
        screen.fill('Black')   
        player.draw(screen)

        #Atualiza player e o timer da bomba/explosão
        player.update()
        bombs_item.update()
        explosions.update()

        #Plota as coisas dependendo da matriz
        walls.draw(screen)
        map_borders.draw(screen)
        points_item.draw(screen)
        lifes_item.draw(screen)
        bombs_item.draw(screen)
        explosions.draw(screen)

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

if game_over:
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