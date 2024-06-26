import pygame 
from sys import exit
from os import path
from Obstacles import Floor
from Explosion import  Explosion, ActiveBomb
from itertools import chain
from game import Game
from menus import MainMenu, PauseMenu

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return x, y

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[0] * 25 + 12.5
    y = xy[1] * 25 + 87.5
    return x, y

class Player(pygame.sprite.Sprite):
    def __init__(self, life = 6, points = 0, coords = (1, 11), bomb_cooldown = 0):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center = coords_to_pixels(coords))
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

        if keys[pygame.K_ESCAPE]:
            game.pause = True

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

        for wall in chain(game.walls.sprites(), game.map_borders.sprites()):
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

        for floor in game.floors.sprites():
            if self.rect.colliderect(floor.rect):
                self.coords = pixels_to_coords(floor.rect.center)

    #Checa por colisões de player com itens ou explosões
    def check_colisions(self):
        for item in game.points_item.sprites():
            if self.rect.colliderect(item.rect):
                self.points += item._value
                pygame.sprite.Sprite.kill(item)

        for item in game.lifes_item.sprites():
            if self.rect.colliderect(item.rect):
                pygame.sprite.Sprite.kill(item)

                if self.life < 6:
                    self.life += item._value

        if len(explosions.sprites()) > 0:
            for explosion in explosions.sprites():
                if self.rect.colliderect(explosion.rect) and explosion.explosion_hitbox:
                    self.damage()

        if pygame.sprite.spritecollide(player_class, game.exit_tile, 0):
            self.place_player(coords_to_pixels((1, 11)))
            game.win = True

        if pygame.sprite.spritecollide(player_class, game.classmate_group, 0):
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

    def place_player(self, xy: tuple[int, int]):
        self.rect.center = xy

    def restart(self):
        self.points = 0
        self.life = 6
        self.place_player(coords_to_pixels((1, 11)))

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
    wallpaper_surf = pygame.image.load(path.join('assets', 'images', 'background_tile.png'))
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
        for wall in game.walls.sprites():
            if explosion.rect.colliderect(wall.rect):
                coords = wall.wall_coords
                pygame.sprite.Sprite.kill(wall)
                game.floors.add(Floor(coords))

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

explosions = pygame.sprite.Group()
bombs_item = pygame.sprite.Group()

main_menu_class = MainMenu()
pause_menu_class = PauseMenu()

game = Game()

#Game Loop
while True:
    if game_active:
        # se o jogo estava no modo pause 
        if game.pause:
            if restart:
                start_time = pygame.time.get_ticks()//1000
                time_diff = 0
                game.restart()
                player_class.restart()
                restart = False
            game.pause = False
            start_time += time_diff
        
        #se player encontrou a saída
        elif game.win:
            start_time = pygame.time.get_ticks()//1000
            time_diff = 0
            game.new_game()
            game.win = False

        #se o jogo acabou de começar
        else:
            start_time = pygame.time.get_ticks()//1000
            time_diff = 0
            game.place_game()

        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            #Plota na tela o plano de fundo e o chão
            set_wallpaper()  
            game.floors.draw(screen)

            #Atualiza player e o timer da bomba/explosão
            player.update()
            bombs_item.update()
            explosions.update()

            #Plota as coisas dependendo da matriz e desenha player
            game.walls.draw(screen)
            game.map_borders.draw(screen)
            player.draw(screen)
            game.points_item.draw(screen)
            game.lifes_item.draw(screen)
            bombs_item.draw(screen)
            explosions.draw(screen)
            game.professor_group.draw(screen)
            game.classmate_group.draw(screen)

            #professor
            for professor in game.professor_group:
                professor.dest = player_class.rect.center

            game.professor_group.update()

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
            if game.pause:
                pause_menu = True
                game_active = False
                break

            #checa se player está na saída
            if game.win:
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
            main_menu_class.menu_buttons.update()
            main_menu_class.menu_buttons.draw(screen)
            
            #checa se o botão 'Start' foi selecionado
            if main_menu_class.start_button.is_clicked:
                main_menu = False
                game_active = True
                break

            #checa se o botão 'Quit' foi selecionado
            elif main_menu_class.quit_button.is_clicked:
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
            pause_menu_class.pause_buttons.update()
            pause_menu_class.pause_buttons.draw(screen)

            #checa se o botão 'Resume' foi clicado
            if pause_menu_class.resume_button.is_clicked:
                pause_end = pygame.time.get_ticks()//1000
                pause_menu = False
                game_active = True
                time_diff = pause_end - pause_start
                break

            #checa se o botão 'Quit' foi clicado
            elif pause_menu_class.quit_button.is_clicked:
                pygame.quit()
                exit()

            #checa se o botão 'Restart' foi clicado
            elif pause_menu_class.restart_button.is_clicked:
                restart = True
                pause_menu = False
                game_active = True 
                break

            pygame.display.update()
            clock.tick(60)         