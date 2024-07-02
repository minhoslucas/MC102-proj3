from typing import Any
import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.font = pygame.font.Font(None, 50)
        self.image = self.font.render('Button', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
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
        self.image = self.font.render('Start', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Start', True, 'White')
        else: self.image = self.font.render('Start', True, 'White')

class Quit(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Quit', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Quit', True, 'White')
        else: self.image = self.font.render('Quit', True, 'White')

class Resume(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Resume', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Resume', True, 'White')
        else: self.image = self.font.render('Resume', True, 'White')
    
class SaveAndQuit(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Save and Quit', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Save and Quit', True, 'White')
        else: self.image = self.font.render('Save and Quit', True, 'White')
    
class Save(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Save', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Save', True, 'White')
        else: self.image = self.font.render('Save', True, 'White')

class Restart(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Restart', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Restart', True, 'White')
        else: self.image = self.font.render('Restart', True, 'White')

class Difficulty(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('Difficulty', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.image = self.font.render('>  Difficulty', True, 'White')
        else: self.image = self.font.render('Difficulty', True, 'White')

class Back(Button):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.image = self.font.render('<', True, 'White')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))

    def update_image(self):
        if self.is_hovering:
            self.font = pygame.font.Font(None, 80)
            self.image = self.font.render('<', True, 'White')
        else: 
            self.font = pygame.font.Font(None, 50)
            self.image = self.font.render('<', True, 'White')

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