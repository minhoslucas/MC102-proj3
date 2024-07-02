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

