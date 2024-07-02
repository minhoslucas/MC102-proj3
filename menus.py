import pygame
from buttons import Start, Quit, Restart, Resume, Back, Difficulty, SliderCase, SliderButton

class MainMenu:
    def __init__(self):
        self.menu_buttons = pygame.sprite.Group()
        self.start_button = Start((250, 388))
        self.quit_button = Quit((750, 388))
        self.difficulty_button = Difficulty((500, 288))
        self.menu_buttons.add(self.start_button, self.quit_button, self.difficulty_button)
        
class PauseMenu:
    def __init__(self):
        self.pause_buttons = pygame.sprite.Group()
        self.restart_button = Restart((250, 200))
        self.resume_button = Resume((250, 300))
        self.quit_button = Quit((250, 400))
        self.pause_buttons.add(self.restart_button, self.quit_button, self.resume_button)

class DifficultyMenu:
    def __init__(self):
        self.difficulty_buttons = pygame.sprite.Group()
        self.back_button = Back((50, 50))
        self.difficulty_buttons.add(self.back_button)
        self.sliders = pygame.sprite.Group()
        self.slider_button = SliderButton((500, 388), 50)
        self.slider_case = self.slider_button.slider_case
        self.sliders.add(self.slider_case, self.slider_button)

    
    
