from src.screens.home_screen import HomeScreen
from src.screens.game_screen import GameScreen
from src.screens.difficulty_screen import DifficultyScreen
import pygame
from src.constants import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize screens
        self.screens = {
            'home': HomeScreen(self),
            'game': GameScreen(self, multiplayer=False),
            'multiplayer': GameScreen(self, multiplayer=True),
            'difficulty': DifficultyScreen(self)
        }
        self.current_screen = 'home'
    
    def set_screen(self, screen_name):
        self.current_screen = screen_name
    
    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            current = self.screens[self.current_screen]
            current.handle_events(events)
            current.update()
            current.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def render(self):
        current_screen = self.get_current_screen()
        if current_screen:
            current_screen.draw(self.screen)
        pygame.display.flip()

    def get_current_screen(self):
        return self.screens.get(self.current_screen)

    def draw(self):
        self.game.screen.fill((30, 30, 30))  # Background
        self.player.draw(self.game.screen)
        for enemy in self.enemies:
            enemy.draw(self.game.screen)
        if self.multiplayer:
            self.player2.draw(self.game.screen)

    def update(self):
        self.player.handle_input()
        if self.multiplayer:
            self.player2.handle_input()
        for enemy in self.enemies:
            enemy.move()