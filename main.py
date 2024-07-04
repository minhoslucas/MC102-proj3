import pygame 
from sys import exit
from os import path
from Obstacles import Floor
from Explosion import  Explosion, ActiveBomb
from itertools import chain
from game import Game
from menus import MainMenu, PauseMenu, DifficultyMenu, GameOverMenu, LeaderboardMenu

DEBUG = True

def pixels_to_coords(xy: tuple[int, int]):
    x = round((xy[0] - 12.5) // 25)
    y = round((xy[1] - 87.5) // 25)
    return y, x

def coords_to_pixels(xy: tuple[int, int]):
    x = xy[1] * 25 + 12.5
    y = xy[0] * 25 + 87.5
    return x, y

def print_maze(maze, *movables):
    old_pos = []

    movables = set(movables)

    for movable in movables:
        old_pos.append((movable, maze[movable[0]][movable[1]]))
        maze[movable[0]][movable[1]] = "@"

    with open("output.out", "w") as file:
        for line in maze:
            file.write("".join(line) + "\n")

    for pos, old in old_pos:
        maze[pos[0]][pos[1]] = old

class Player(pygame.sprite.Sprite):
    def __init__(self, life = 6, points = 0, coords = (11, 1), bomb_cooldown = 0):
        super().__init__()
        self.image = pygame.Surface((20, 20))
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
            self.set_animation_sprite(0, vector.x)
            self.set_animation_sprite(1, vector.y)

        if keys[pygame.K_SPACE]:
            if self.bomb_cooldown == 0 and game.inventory_slot.bomb_count > 0:
                self.place_bomb()
                game.inventory_slot.bomb_count -= 1

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
    def _move(self, movement: int, axis: int):
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

        for item in game.time_item.sprites():
            if self.rect.colliderect(item.rect):
                pygame.sprite.Sprite.kill(item)
                game.extra_time += item._value

        if len(explosions.sprites()) > 0:
            for explosion in explosions.sprites():
                if self.rect.colliderect(explosion.rect) and explosion.explosion_hitbox:
                    self.damage()

        if pygame.sprite.spritecollide(player_class, game.exit_tile, 0):
            self.place_player(coords_to_pixels((1, 11)))
            game.win = True
            game.extra_time = 0
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
        x_coords, y_coords = coords_to_pixels(self.coords)

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

    def _animate(self, path_list: tuple[str, str, str], time: int, flip: bool = False):
        if (time%400 >= 0 and time%400 < 100) or (time%400 >= 200 and time%400 < 300): 
            self.image = pygame.image.load(path.join(PLAYER_SPRITES_FOLDER, path_list[0]))
            if flip: self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (25, 25))
        elif (time%400 >= 100 and time%400 < 200):
            self.image = pygame.image.load(path.join(PLAYER_SPRITES_FOLDER, path_list[1]))
            if flip: self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (25, 25))
        elif (time%400 >= 300 and time%400 < 400):
            self.image = pygame.image.load(path.join(PLAYER_SPRITES_FOLDER, path_list[2]))
            if flip: self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (25, 25))
    def set_animation_sprite(self, axis, movement):
        time = pygame.time.get_ticks()
        if axis == 0 and movement < 0:
            path_list = ('player_left_still.png', 'player_left_frame_1.png', 'player_left_frame_2.png')
            self._animate(path_list, time)
        elif axis == 0 and movement > 0:
            path_list = ('player_left_still.png', 'player_left_frame_1.png', 'player_left_frame_2.png')
            self._animate(path_list, time, True)
        elif axis == 1 and movement > 0:
            path_list = ('player_bot_still.png', 'player_bot_frame_1.png', 'player_bot_frame_2.png')
            self._animate(path_list, time)
        elif axis == 1 and movement < 0:
            path_list = ('player_top_still.png', 'player_top_frame_1.png', 'player_top_frame_2.png')
            self._animate(path_list, time)
        
    def place_player(self, xy: tuple[int, int]):
        self.rect.center = xy

    def restart(self):
        self.points = 0
        self.life = 6
        self.place_player(coords_to_pixels((11, 1)))

    def check_life_count(self):
        if self.life == 0:
            game.over = True

    #Função UPDATE, atualizada o tempo todo no Game Loop
    def update(self):
        self.invincible_timer()
        self.check_colisions()
        self.check_life_count()
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

#Desenha a tela de GAME OVER
def display_game_over():
    text_font = pygame.font.Font(None, 100)
    game_over_surf = text_font.render('GAME OVER', True, 'White')
    game_over_rect = game_over_surf.get_rect(center = (500, 288))
    screen.blit(game_over_surf, game_over_rect)

def display_title():
    text_font = pygame.font.Font(None, 100)
    title_surf = text_font.render('Os Labirintos da Unicamp', True, 'White')
    title_rect = title_surf.get_rect(center = (500, 188))
    screen.blit(title_surf, title_rect)

def display_difficulty():
    text_font = pygame.font.Font(None, 50)
    if game.difficulty >= 70:
        difficulty_surf = text_font.render(f'Difficulty: Hard', True, 'White')
    elif game.difficulty < 70 and game.difficulty >= 30:
        difficulty_surf = text_font.render(f'Difficulty: Medium', True, 'White')
    else:
        difficulty_surf = text_font.render(f'Difficulty: Easy', True, 'White')
    difficulty_rect = difficulty_surf.get_rect(center = (500, 288))
    screen.blit(difficulty_surf, difficulty_rect)

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
                game.update_matrix(coords)

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
PLAYER_SPRITES_FOLDER = path.join('assets', 'images', 'player_sprites')

pygame.init()

#Diferentes modos de jogo e contador de levels
game_active = False
game_over = False
main_menu = False
pause_menu = False
difficulty_menu = False
leaderboard_menu = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
transparent = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

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
difficulty_menu_class = DifficultyMenu()
game_over_menu_class = GameOverMenu()
leaderboard_menu_class = LeaderboardMenu()

game = Game()

#Game Loop
while True:
    if game_active:
        # se o jogo estava no modo pause 
        if game.pause:
            if game.restart:
                start_time = pygame.time.get_ticks()//1000
                game.extra_time = 0
                time_diff = 0
                game.restart_game()
                player_class.restart()
                game.restart = False
            game.pause = False
            start_time += time_diff
        
        #se player encontrou a saída
        elif game.win:
            start_time = pygame.time.get_ticks()//1000
            time_diff = 0
            game.new_game()
            game.win = False

        elif game.over:
            start_time = pygame.time.get_ticks()//1000
            time_diff = 0
            game.full_restart()
            player_class.restart()
            game.over = False

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
            game.set_wallpaper(screen)  
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
            game.time_item.draw(screen)
            game.inventory_slot_group.draw(screen)
            game.inventory_slot.display_bomb_count(screen)
            bombs_item.draw(screen)
            explosions.draw(screen)
            game.professor_group.draw(screen)
            game.classmate_group.draw(screen)

            #professor

            prof_coords = [player_class.coords]

            for professor in game.professor_group:
                line = pygame.draw.line(transparent, "#ffffffdd", 
                                        professor.rect.center, 
                                        player_class.rect.center)
                
                has_sight = True

                for wall in game.walls.sprites():
                    if line.colliderect(wall.rect):
                        has_sight = False
                        break

                if has_sight:
                    professor.seen = True
                    professor.route = []
                    professor.dest = player_class.rect.center
                else:
                    professor.update_destination(game.matrix, player_class.coords)

                prof_coords.append(professor.coords)

            game.professor_group.update()

            if DEBUG:
                print_maze(game.matrix, *prof_coords)

            #Desenham a pontuação, vida, coordenadas, e tempo
            display_score()
            game.display_life_count(screen, player_class.life)
            display_coords()
            game.display_level(screen)
            game.display_timer(screen=screen, start_time=start_time) #Tempo em segundos, por padrão, 2 minutos
            #critérios para GAME OVER
            if game.over: 
                game.level = 1
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
                game.level += 1
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
            game.set_wallpaper(screen)  

            #Desenha a tela de GAME OVER
            display_game_over()
            game_over_menu_class.game_over_buttons.draw(screen)
            game_over_menu_class.game_over_buttons.update()

            if game_over_menu_class.main_menu_button.is_clicked:
                main_menu = True
                game_over = False
                break

            elif game_over_menu_class.quit_button.is_clicked:
                pygame.quit()
                exit()
            
            elif game_over_menu_class.restart_button.is_clicked:
                game_active = True
                game_over = False
                restart = True
                break

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
            game.set_wallpaper(screen)  
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

            elif main_menu_class.difficulty_button.is_clicked:
                main_menu = False
                difficulty_menu = True
                break

            pygame.display.update()
            clock.tick(60)

    #menu de pause
    elif pause_menu:
        pause_start = pygame.time.get_ticks()//1000
        while True:

            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            #plota o plano de fundo
            game.set_wallpaper(screen)

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
                game.restart = True
                pause_menu = False
                game_active = True 
                break

            pygame.display.update()
            clock.tick(60)
    elif difficulty_menu:
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            game.set_wallpaper(screen)
            display_difficulty()

            difficulty_menu_class.difficulty_buttons.update()
            difficulty_menu_class.sliders.update()
            difficulty_menu_class.difficulty_buttons.draw(screen)
            difficulty_menu_class.sliders.draw(screen)

            if difficulty_menu_class.back_button.is_clicked:
                difficulty_menu = False
                main_menu = True
                break
            
            game.difficulty = difficulty_menu_class.slider_button.val

            pygame.display.update()
            clock.tick(60)                               
    elif leaderboard_menu:
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            game.set_wallpaper(screen)
            leaderboard_menu_class.leaderboard_buttons.draw(screen)
            leaderboard_menu_class.leaderboard_buttons.update()

            if leaderboard_menu_class.main_menu_button.is_clicked:
                main_menu = True
                leaderboard_menu = False
                break

            pygame.display.update()
            clock.tick(60)      