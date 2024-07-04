from os import path
import pygame

FONT_PATH = path.join('assets', 'fonts', 'Clarity.otf')

class Button(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.font = pygame.font.Font(FONT_PATH, 30)
        self.image = self.font.render('Button', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.pos = pos
        self.mouse_pos = (0, 0)
        self.is_clicked = False
        self.is_hovering = False

    def _get_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.mouse_pos = (mouse_x, mouse_y)

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(self.mouse_pos):
                self.is_clicked = True
        else: self.is_clicked = False

    def check_hover(self):
        if self.rect.collidepoint(self.mouse_pos):
            self.is_hovering = True
        else: self.is_hovering = False      
    def update_image(self):
        return
    
    def update(self):
        self.update_image()
        self._get_mouse_pos()
        self.check_hover()
        self.check_click()

class Start(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Start', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Start', False, 'White')
        else: self.image = self.font.render('Start', False, 'White')

class Quit(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Quit', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Quit', False, 'White')
        else: self.image = self.font.render('Quit', False, 'White')

class Resume(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Resume', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Resume', False, 'White')
        else: self.image = self.font.render('Resume', False, 'White')
    
class SaveAndQuit(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Save and Quit', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Save and Quit', False, 'White')
        else: self.image = self.font.render('Save and Quit', False, 'White')
    
class Save(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Save', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Save', False, 'White')
        else: self.image = self.font.render('Save', False, 'White')

class Restart(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Restart', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Restart', False, 'White')
        else: self.image = self.font.render('Restart', False, 'White')

class Difficulty(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Difficulty', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Difficulty', False, 'White')
        else: self.image = self.font.render('Difficulty', False, 'White')

class Back(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('<', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.font = pygame.font.Font(FONT_PATH, 80)
            self.image = self.font.render('<', False, 'White')
        else: 
            self.font = pygame.font.Font(FONT_PATH, 50)
            self.image = self.font.render('<', False, 'White')

class BackToMenu(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render(f'Main Menu', False, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render(f'>  Main Menu', False, 'White')
        else: self.image = self.font.render(f'Main Menu', False, 'White')

class QuestionButton(Button):
    def __init__(self, pos: tuple[int, int], choice: str):
        super().__init__(pos)
        self._choice = choice
        self.image = self.font.render(f'{self.choice}', False, 'White')
        self.rect = self.image.get_rect(center = pos)

    @property
    def choice(self):
        return self._choice 
    @choice.setter
    def choice(self, choice):
        self._choice = choice

    def update_image(self):
        if len(self.choice) > 10:
            self.font = pygame.font.Font(FONT_PATH, 20)
            self.rect = self.image.get_rect(center = self.pos)
        if self.is_hovering:
            self.image = self.font.render(f'>  {self.choice}', False, 'White')
        else: self.image = self.font.render(f'{self.choice}', False, 'White')


class SliderButton(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], val: float):
        super().__init__()
        self.ini_val = val
        self.ini_pos = pos[0]
        self._pos = pos
        self._val = val
        self.slider_case = SliderCase(pos)
        self.image = pygame.Surface((25, 25))
        self.image.fill('Blue')
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        self.is_clicked = False
        self.mouse_pos = (0, 0)

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, pos):
        self._pos = pos 

    @property
    def val(self):
        return self._val
    @val.setter
    def val(self, val):
        self._val = val

    def _get_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.mouse_pos = (mouse_x, mouse_y)

    def _check_slider_pos(self):
        if self.rect.collidepoint(self.slider_case.rect.midleft):
            self.rect.left = self.slider_case.rect.left
        elif self.rect.collidepoint(self.slider_case.rect.midright):
            self.rect.right = self.slider_case.rect.right
    def move_slider(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.mouse_pos):
            self.rect.centerx = self.mouse_pos[0]
            self.pos = self.rect.center

    def get_value(self):
        self.val = self.ini_val - (self.ini_pos - self.pos[0])

    def update(self):
        self.get_value()
        self._check_slider_pos()
        self._get_mouse_pos()
        self.move_slider()

class SliderCase(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]) -> None:  
        super().__init__()
        self.image = pygame.Surface((100, 25))
        self.image.fill('Gray')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))