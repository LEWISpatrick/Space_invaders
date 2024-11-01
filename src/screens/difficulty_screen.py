import pygame
from src.constants import WIDTH, HEIGHT, WHITE
from src.screens.base_screen import BaseScreen

class DifficultyScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.selected_option = 0
        self.options = ["Easy", "Medium", "Impossible 🫤💀"]
        self.speeds = [5, 15, 30]  # Corresponding speeds for each difficulty
        self.font = pygame.font.Font(None, 74)
        self.game_mode = None  # Will be set to 'single' or 'multi'
    
    def draw(self, surface):
        surface.fill((30, 30, 30))
        
        # Draw title
        title = self.font.render("Select Difficulty", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
        surface.blit(title, title_rect)
        
        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 100))
            surface.blit(text, rect)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                if event.key == pygame.K_SPACE:
                    self.select_option()
    
    def set_game_mode(self, mode):
        self.game_mode = mode
    
    def select_option(self):
        speed = self.speeds[self.selected_option]
        if self.game_mode == 'single':
            self.game.screens['game'].set_difficulty(speed)
            self.game.set_screen('game')
        else:
            self.game.screens['multiplayer'].set_difficulty(speed)
            self.game.set_screen('multiplayer')
