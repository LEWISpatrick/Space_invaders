import pygame
from src.constants import WIDTH, HEIGHT, WHITE
from src.screens.base_screen import BaseScreen  # Make sure this path is correct

class HomeScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.selected_option = 0
        self.options = ["Single Player", "Local Multiplayer"]
        self.font = pygame.font.Font(None, 74)
    
    def draw(self, surface):
        surface.fill((30, 30, 30))  # Background
        
        # Draw title
        title = self.font.render("SPACE INVADERS", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
        surface.blit(title, title_rect)
        
        # Draw menu options
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
    
    def select_option(self):
        difficulty_screen = self.game.screens['difficulty']
        if self.selected_option == 0:  # Single Player
            difficulty_screen.set_game_mode('single')
        else:  # Multiplayer
            difficulty_screen.set_game_mode('multi')
        self.game.set_screen('difficulty')
