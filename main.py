import pygame 
from sys import exit
from os import path
from random import choice

import pygame.ftfont
from Obstacles import Floor
from Explosion import  Explosion, ActiveBomb
from itertools import chain
from game import Game
from menus import MainMenu, PauseMenu, DifficultyMenu, GameOverMenu, LeaderboardMenu, QuestionMenu, NameMenu
from leaderboard import Score, leaderboard
from question import select_question

from Tile import Tile

DEBUG = True
FONT_PATH = path.join('assets', 'fonts', 'Clarity.otf')

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

class Player(Tile):
    def __init__(self, life = 6, points = 0, coords = (0, 1), bomb_cooldown = 0, is_questioned = False, has_answered = False):
        super().__init__(coords, size=20)
        self.image.fill('Red')
        self._life = life
        self._points = points
        self._coords = coords
        self._bomb_cooldown = bomb_cooldown
        self._is_questioned = is_questioned
        self._has_aswered = has_answered
        self.invincible = False
        self.start_time = 0

    @property
    def has_answered(self):
        return self._has_aswered
    @has_answered.setter
    def has_answered(self, has_answered):
        self._has_aswered = has_answered

    @property
    def is_questioned(self):
        return self._is_questioned
    @is_questioned.setter
    def is_questioned(self, is_questioned):
        self._is_questioned = is_questioned

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
        self._life = min(life, 6)

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
        if self.rect.top < 70:
            self.rect.top = 70
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
        for item in game.items.sprites():
            if self.rect.colliderect(item.rect):
                item.act(self, game)

        if len(explosions.sprites()) > 0:
            for explosion in explosions.sprites():
                if self.rect.colliderect(explosion.rect) and explosion.explosion_hitbox:
                    self.damage()

        if pygame.sprite.spritecollide(player_class, game.exit_tile, 0):
            for tile in game.entrance_tile.sprites():
                self.place_player(coords_to_pixels((0, 1)))
            game.win = True
            game.extra_time = 0
        if pygame.sprite.spritecollide(player_class, game.classmate_group, 1):
           self.is_questioned = True


        # if self.rect.colliderect(professor.rect):
        #     self.is_questioned = True

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

    def reward_player(self, answer: bool):
        if answer:
            prize_list = ['p','p','p','p','p','l','l','l','l','b', 'b','b']
            prize = choice(prize_list)
            if prize == 'p':
                self.points += 200
            elif prize == 'l' and self.life < 6:
                self.life += 1
            else:
                game.inventory_slot.bomb_count += 1
        else: self.damage()
    #Função UPDATE, atualizada o tempo todo no Game Loop
    def update(self):
        self.invincible_timer()
        self.check_colisions()
        self.check_life_count()
        self.player_input()
        self.screen_limits()

#Desenha a pontação na tela
def display_score():
    text_font = pygame.font.Font(FONT_PATH, 20)
    score_surf = text_font.render(f'Score: {player_class.points}', False, 'White')
    score_rect = score_surf.get_rect(center = (90, 50))
    screen.blit(score_surf, score_rect)

#Desenha as coordenadas na tela
def display_coords():
    text_font = pygame.font.Font(FONT_PATH, 20)
    coords_surf = text_font.render(f'Coords: {player_class.coords}', False, 'White')
    coords_rect = coords_surf.get_rect(center = (475, 50))
    screen.blit(coords_surf, coords_rect)

#Desenha a tela de GAME OVER
def display_game_over():
    text_font = pygame.font.Font(FONT_PATH, 60)
    game_over_surf = text_font.render('GAME OVER', False, 'White')
    game_over_rect = game_over_surf.get_rect(center = (500, 288))
    screen.blit(game_over_surf, game_over_rect)


def display_you_win():
    text_font = pygame.font.Font(FONT_PATH, 60)
    you_win_surf = text_font.render('YOU WIN!', False, 'White')
    you_win_rect = you_win_surf.get_rect(center = (500, 80))
    screen.blit(you_win_surf, you_win_rect)

def display_new_highscore():
    text_font = pygame.font.Font(FONT_PATH, 20)
    new_highscore_surf = text_font.render('NEW HIGHSCORE', False, 'White')
    new_highscore_rect = new_highscore_surf.get_rect(center = (500, 140))
    screen.blit(new_highscore_surf, new_highscore_rect)

def display_title():
    text_font = pygame.font.Font(FONT_PATH, 50)
    title_surf = text_font.render('Os Labirintos da Unicamp', False, 'White')
    title_rect = title_surf.get_rect(center = (500, 188))
    screen.blit(title_surf, title_rect)

def display_difficulty():
    text_font = pygame.font.Font(FONT_PATH, 50)
    if game.difficulty == 3:
        difficulty_surf = text_font.render(f'Difficulty: Hard', False, 'White')
    elif game.difficulty == 2:
        difficulty_surf = text_font.render(f'Difficulty: Medium', False, 'White')
    else:
        difficulty_surf = text_font.render(f'Difficulty: Easy', False, 'White')
    difficulty_rect = difficulty_surf.get_rect(center = (500, 288))
    screen.blit(difficulty_surf, difficulty_rect)

def display_question(question: str):
    question_list = list(question.split())
    text_font = pygame.font.Font(FONT_PATH, 20)
    if len(question_list) > 6:
        question_1 =  ' '.join(question_list[:6])
        question_surf = text_font.render(f'{question_1}', False, 'White')
        question_rect = question_surf.get_rect(center = (500, 223))
        screen.blit(question_surf, question_rect)

        question_2 =  ' '.join(question_list[6:])
        question_surf = text_font.render(f'{question_2}', False, 'White')
        question_rect = question_surf.get_rect(center = (500, 243))
        screen.blit(question_surf, question_rect)
    else:
        question_surf = text_font.render(f'{question}', False, 'White')
        question_rect = question_surf.get_rect(center = (500, 188))
        screen.blit(question_surf, question_rect)

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
                coords = wall.pos
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
main_menu = True
pause_menu = False
difficulty_menu = False
leaderboard_menu = False
question_menu = False
name_menu = False

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
name_menu_class = NameMenu()

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

        elif player_class.has_answered:
            start_time += time_diff
            player_class.has_answered = False
        
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
            game.items.draw(screen)
            game.inventory_slot_group.draw(screen)
            game.inventory_slot.display_bomb_count(screen)
            bombs_item.draw(screen)
            explosions.draw(screen)
            game.professor_group.draw(screen)
            game.classmate_group.draw(screen)

            #professor

            prof_coords = [player_class.coords]

            for professor in game.professor_group:
                prof_coords.append(professor.coords)

                if not professor.seen:
                    circle = pygame.draw.circle(transparent, "#ffffffdd", 
                                                professor.rect.center, 100, 0)

                    if circle.colliderect(player_class.rect):
                        professor.seen = True

                    continue

                line = pygame.draw.line(transparent, "#ffffffdd", 
                                        professor.rect.center, 
                                        player_class.rect.center)
                has_sight = True

                for wall in game.walls.sprites():
                    if line.colliderect(wall.rect):
                        has_sight = False
                        break

                if has_sight:
                    professor.route = []
                    professor.dest = player_class.rect.center
                else:
                    professor.update_destination(game.matrix, player_class.coords)

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

            if player_class.is_questioned:
                question_menu = True
                game_active = False
                break

            if game.level > 1:
                leaderboard_menu = True
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
                name_menu = True
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
            
            if difficulty_menu_class.slider_button.val >= 70:
                game.difficulty = 3
            elif difficulty_menu_class.slider_button.val >= 30 and difficulty_menu_class.slider_button.val < 70:
                game.difficulty = 2
            else:
                game.difficulty = 1

            pygame.display.update()
            clock.tick(60)                               
    elif leaderboard_menu:
        new_score = Score(user_text, time=999, score=player_class.points, maze=game.level)
        is_high_score = new_score.save()

        scores = leaderboard()
        
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            game.set_wallpaper(screen)
            display_you_win()

            leaderboard_menu_class.leaderboard_buttons.update()
            leaderboard_menu_class.leaderboard_buttons.draw(screen)
            leaderboard_menu_class.display_scores(screen, scores[2])

            if is_high_score:
                display_new_highscore()

            if leaderboard_menu_class.main_menu_button.is_clicked:
                pygame.quit()
                exit()

            pygame.display.update()
            clock.tick(60) 
    elif question_menu:
        question_start = pygame.time.get_ticks()//1000
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()

            game.set_wallpaper(screen)
            if player_class.is_questioned:
                player_class.is_questioned = False
                question = select_question(game.difficulty)
                question_menu_class = QuestionMenu(question.choices)

            question_menu_class.question_buttons.update()
            question_menu_class.question_buttons.draw(screen)
            display_question(question.question)
            question_end = 0

            for button in question_menu_class.question_buttons.sprites():
                if button.is_clicked:
                    question_end = pygame.time.get_ticks()//1000
                    if button.choice == question.answer:
                        player_class.reward_player(True)
                        player_class.has_answered = True
                        game_active = True
                        question_menu = False
                    else:
                        player_class.reward_player(False)
                        player_class.has_answered = True
                        game_active = True
                        question_menu = False
            time_diff = question_end - question_start
            if not question_menu:
                break
            
            pygame.display.update()
            clock.tick(60)    
    elif name_menu:
        user_text = ''
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()   

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                        user_text = user_text.strip()
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.KSCAN_KP_ENTER:
                        game_active = True
                        name_menu = False
                    elif len(user_text) > 8:
                        pass
                    else:
                        user_text += event.unicode
                        user_text = user_text.strip()
            
            if not name_menu: break

            game.set_wallpaper(screen)
            name_menu_class.name_buttons.update()
            name_menu_class.name_buttons.draw(screen)
            name_menu_class.name_box(screen)
            name_menu_class.display_name_title(screen)
            name_menu_class.display_name(screen, user_text)

            if name_menu_class.start_button.is_clicked:
                game_active = True
                name_menu = False
                break
            

            pygame.display.update()
            clock.tick(60)          