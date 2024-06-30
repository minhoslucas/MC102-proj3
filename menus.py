import pygame

class StartButton(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((100, 50))
        self.image.fill('Green')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.mouse_pos = (0, 0)
        self.is_clicked = False
    def check_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.mouse_pos = (mouse_x, mouse_y)
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(self.mouse_pos):
                self.is_clicked = True
        else:
            self.is_clicked = False

    def update(self):
        self.check_click()

class QuitButton(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((100, 50))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.mouse_pos = (0, 0)
        self.is_clicked = False
    def check_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.mouse_pos = (mouse_x, mouse_y)
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(self.mouse_pos):
                self.is_clicked = True
        else:
            self.is_clicked = False

    def update(self):
        self.check_click()
                   