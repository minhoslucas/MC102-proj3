import pygame 
import random
from sys import exit
from os import path
from Obstacles import Wall, UnbreakableWall, Floor, Entrance, Exit
from Explosion import  Explosion, ActiveBomb
from Items import Points, Life
from maze import mazes
from itertools import chain
from professor import Professor
from classmate import Classmate
from menus import Start, Quit, Resume, SaveAndQuit, Save, Restart

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return x, y

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[0] * 25 + 12.5
    y = xy[1] * 25 + 87.5
    return x, y

class Player(pygame.sprite.Sprite):
    def __init__(self, life = 6, points = 0, coords = (1, 6), bomb_cooldown = 0, pause_key = False):
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
        self._pause_key = pause_key
        self._is_at_exit = False


    @property
    def is_at_exit(self):
        return self._is_at_exit
    @is_at_exit.setter
    def is_at_exit(self, is_at_exit):
        self._is_at_exit = is_at_exit

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

    @property
    def pause_key(self):
        return self._pause_key
    @pause_key.setter
    def pause_key(self, pause_key):
        self._pause_key = pause_key

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

        if keys[pygame.K_ESCAPE]:
            self.pause_key = True

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

        if self.rect.colliderect(exit_class.rect):
            self.is_at_exit = True

        if pygame.sprite.spritecollide(player_class, classmate_group, 0):
            print(True) #temporário

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

#Desenha as coordenadas na tela
def display_coords():
    text_font = pygame.font.Font(None, 30)
    coords_surf = text_font.render(f'Coords: {player_class.coords}', True, 'White')
    coords_rect = coords_surf.get_rect(center = (475, 50))
    screen.blit(coords_surf, coords_rect)

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

def set_wallpaper():
    wallpaper_surf = pygame.image.load(path.join('images', 'background_tile.png'))
    for i in range(20):
        for j in range(16):
            wallpaper_rect = wallpaper_surf.get_rect(center = (i*50 + 25, j*50 + 25))
            screen.blit(wallpaper_surf, wallpaper_rect)

#Desenha o timer na tela
def display_timer(time_limit = 120, start_time = 0):
    text_font = pygame.font.Font(None, 30)
    real_time = start_time + time_limit - pygame.time.get_ticks()//1000

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

def display_title():
    text_font = pygame.font.Font(None, 100)
    title_surf = text_font.render('Os Labirintos da Unicamp', True, 'White')
    title_rect = title_surf.get_rect(center = (500, 188))
    screen.blit(title_surf, title_rect)

def display_level():
    text_font = pygame.font.Font(None, 30)
    level_surf = text_font.render(f'Level: {level}', True, 'White')
    level_rect = level_surf.get_rect(center = (75, 750))
    screen.blit(level_surf, level_rect)

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

def place_map(floor_coord_list):
    global exit_class #POR PREGUIÇA, AJEITAR
    map = random.choice(mazes)
    for line_index, line in enumerate(map):
        for tile_index, tile in enumerate(line):
            tile = str(tile)
            coords = coords_to_pixels((tile_index, line_index))

            if line_index == 0 or tile_index == 0 or line_index == len(map)-1 or tile_index == len(map[line_index])-1:
                if (tile_index == 0 and line_index == 11) or (tile_index == 39 and line_index == 11):
                    entrance_class = Entrance(coords)
                    exit_class = Exit(coords)
                    entrance_tile.add(entrance_class)
                    exit_tile.add(exit_class)
                else: map_borders.add(UnbreakableWall(coords))

            elif tile == ' ':
                floors.add(Floor(coords))
                if coords[0] > 200:
                    floor_coord_list.append((coords, (line_index, tile_index)))

            elif tile == '#':
                walls.add(Wall(coords))
    return map
        
def place_items(map):

    points_pos = random.sample(floor_coord_list, 5)
    for pos in points_pos:
        map[pos[1][0]][pos[1][1]] = 'P'
        points_item.add(Points(pos[0]))

    lifes_pos = random.sample(floor_coord_list, 5)
    for pos in lifes_pos:
        map[pos[1][0]][pos[1][1]] = 'L'
        lifes_item.add(Life(pos[0]))

def place_entities(map):

    professor_pos = random.sample(floor_coord_list, 2)
    for pos in professor_pos:
        map[pos[1][0]][pos[1][1]] = 'p'
        professor_group.add(Professor(pos[0]))
    classmate_pos = random.sample(floor_coord_list, 4)
    for pos in classmate_pos:
        map[pos[1][0]][pos[1][1]] = 'c'
        classmate_group.add(Classmate(pos[0]))

SCREEN_WIDTH = 1000
SCREEN_HIGHT = 775

pygame.init()

#Diferentes modos de jogo e contador de levels
game_active = False
game_over = False
main_menu = True
pause_menu = False
level = 1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Os Labirintos da Unicamp')

#Cria um grupo para player
player = pygame.sprite.GroupSingle()
player_class = Player()
player.add(player_class)

#Cria um grupo para todos os obtáculos e itens do jogo
walls = pygame.sprite.Group()
map_borders = pygame.sprite.Group()
floors = pygame.sprite.Group()
exit_tile = pygame.sprite.GroupSingle()
entrance_tile = pygame.sprite.GroupSingle()

explosions = pygame.sprite.Group()

points_item = pygame.sprite.Group()
lifes_item = pygame.sprite.Group()
bombs_item = pygame.sprite.Group()


professor_group = pygame.sprite.Group()
classmate_group = pygame.sprite.Group()

menu_buttons = pygame.sprite.Group()
start_button = Start((250, 388))
quit_button_menu = Quit((750, 388))
menu_buttons.add(start_button, quit_button_menu)

pause_buttons = pygame.sprite.Group()
quit_button_pause = Quit((250, 400))
resume_button = Resume((250, 300))
restart_button = Restart((250, 200))
pause_buttons.add(quit_button_pause, resume_button, restart_button)

#Game Loop
while True:
    if game_active:

        #se o jogo estava no modo pause 
        if player_class.pause_key == True:
            if restart:
                start_time = pygame.time.get_ticks()//1000
                time_diff = 0
                map = place_map(floor_coord_list)
                points_item.empty()
                lifes_item.empty()
                place_items(map)
                classmate_group.empty()
                professor_group.empty()
                place_entities(map)
                restart = False
            player_class.pause_key = False
            start_time += time_diff
        
        #se player encontrou a saída
        elif player_class.is_at_exit:
            start_time = pygame.time.get_ticks()//1000
            time_diff = 0
            floor_coord_list.clear()
            floors.empty()
            walls.empty()
            map_borders.empty()
            map = place_map(floor_coord_list)
            points_item.empty()
            lifes_item.empty()
            place_items(map)
            classmate_group.empty()
            professor_group.empty()
            place_entities(map)
            player_class.is_at_exit = False        

        #se o jogo acabou de começar
        else: 
            start_time = pygame.time.get_ticks()//1000
            time_diff = 0
            floor_coord_list = []
            map = place_map(floor_coord_list)
            place_items(map)
            place_entities(map)

        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            #Plota na tela o plano de fundo e o chão
            set_wallpaper()  
            floors.draw(screen)

            #Atualiza player e o timer da bomba/explosão
            player.update()
            bombs_item.update()
            explosions.update()

            #Plota as coisas dependendo da matriz e desenha player
            walls.draw(screen)
            map_borders.draw(screen)
            player.draw(screen)
            points_item.draw(screen)
            lifes_item.draw(screen)
            bombs_item.draw(screen)
            explosions.draw(screen)
            professor_group.draw(screen)
            classmate_group.draw(screen)

            #professor
            for professor in professor_group:
                professor.dest = player_class.rect.center

            professor_group.update()

            #Desenham a pontuação, vida, coordenadas, e tempo
            display_score()
            display_life_count()
            display_coords()
            display_level()

            #critérios para GAME OVER
            if not display_timer(start_time=start_time) or not check_life_count(): #Tempo em segundos, por padrão, 2 minutos
                game_over = True
                game_active = False
                break

            #checa se player apertou o botão 'ESC'
            if player_class.pause_key == True:
                pause_menu = True
                game_active = False
                break

            #checa se player está na saída
            if player_class.is_at_exit:
                mazes.remove(map)
                player_class.rect.x, player_class.rect.y = 75, 375
                level += 1
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
            set_wallpaper()  

            #Desenha a tela de GAME OVER
            display_game_over()

            pygame.display.update()
            clock.tick(60)

    #menu inicial 
    elif main_menu:
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            #plota o plano de fundo e o título do jogo
            set_wallpaper()  
            display_title()

            #atualiza o estado dos botões
            menu_buttons.update()
            menu_buttons.draw(screen)
            
            #checa se o botão 'Start' foi selecionado
            if start_button.is_clicked == True:
                main_menu = False
                game_active = True
                break

            #checa se o botão 'Quit' foi selecionado
            elif quit_button_menu.is_clicked == True:
                pygame.quit()
                exit()
       
            pygame.display.update()
            clock.tick(60)

    #menu de pause
    elif pause_menu:
        pause_start = pygame.time.get_ticks()//1000
        while True:
            restart = False

            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            #plota o plano de fundo
            set_wallpaper()

            #atualiza o estado dos botões
            pause_buttons.update()
            pause_buttons.draw(screen)

            #checa se o botão 'Resume' foi clicado
            if resume_button.is_clicked == True:
                pause_end = pygame.time.get_ticks()//1000
                pause_menu = False
                game_active = True
                time_diff = pause_end - pause_start
                break

            #checa se o botão 'Quit' foi clicado
            elif quit_button_pause.is_clicked == True:
                pygame.quit()
                exit()

            #checa se o botão 'Restart' foi clicado
            elif restart_button.is_clicked == True:
                restart = True
                pause_menu = False
                game_active = True
                player_class.rect.x, player_class.rect.y = 75, 375
                player_class.points = 0
                player_class.life = 6 
                break

            pygame.display.update()
            clock.tick(60)         