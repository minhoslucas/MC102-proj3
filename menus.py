import pygame
from buttons import Start, Quit, Restart, Resume

class MainMenu:
    def __init__(self):
        self.menu_buttons = pygame.sprite.Group()
        self.start_button = Start((250, 388))
        self.quit_button = Quit((750, 388))
        self.menu_buttons.add(self.start_button, self.quit_button)
        
class PauseMenu:
    def __init__(self):
        self.pause_buttons = pygame.sprite.Group()
        self.restart_button = Restart((250, 200))
        self.resume_button = Resume((250, 300))
        self.quit_button = Quit((250, 400))
        self.pause_buttons.add(self.restart_button, self.quit_button, self.resume_button)