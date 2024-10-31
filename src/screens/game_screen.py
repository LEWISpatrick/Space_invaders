import pygame
from src.screens.base_screen import BaseScreen
from src.entities.player import Player
from src.constants import WIDTH, HEIGHT
from src.entities.enemy import Enemy
from src.constants import ENEMY_COUNT
from src.utils.collision import check_collision, check_collision_player
class GameScreen(BaseScreen):
    def __init__(self, game, multiplayer=False):
        super().__init__(game)
        self.multiplayer = multiplayer
        self.bullets = []
        self.xp = 0
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.game_over = False
        self.init_game()
    
    def init_game(self):
        # Player 1 with arrow keys
        self.player = Player(WIDTH // 2 - 30, HEIGHT - 60)
        
        if self.multiplayer:
            # Player 2 with WASD and LCTRL
            p2_controls = {
                'left': pygame.K_a,
                'right': pygame.K_d,
                'shoot': pygame.K_LCTRL
            }
            self.player2 = Player(WIDTH // 2 + 30, HEIGHT - 60, p2_controls)

        self.enemies = [Enemy(x * 60 + 50, 50) for x in range(ENEMY_COUNT)]

    def draw(self, surface):
        surface.fill((30, 30, 30))  # Background
        self.player.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        if self.multiplayer:
            self.player2.draw(surface)
            
        # Draw XP counter
        font = pygame.font.Font(None, 36)
        xp_text = font.render(f'XP: {self.xp}', True, (255, 255, 255))
        surface.blit(xp_text, (10, 10))

        if self.game_over:
            font = pygame.font.Font(None, 74)
            game_over_text = font.render('GAME OVER', True, (255, 0, 0))
            score_text = font.render(f'Final Score: {self.xp}', True, (255, 255, 255))
            restart_text = font.render('Press SPACE to continue', True, (255, 255, 255))
            
            game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
            restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
            
            surface.blit(game_over_text, game_over_rect)
            surface.blit(score_text, score_rect)
            surface.blit(restart_text, restart_rect)

    def update(self):
        if self.game_over:
            return

        for enemy in self.enemies:
            if check_collision_player(self.player, enemy):
                self.game_over = True
                return

        if not self.can_shoot:
            self.shoot_cooldown += 1
            if self.shoot_cooldown >= 20:
                self.can_shoot = True
                self.shoot_cooldown = 0

        if self.can_shoot:
            bullet = self.player.handle_input(self.game.screen)
            if bullet:
                self.bullets.append(bullet)
                self.can_shoot = False

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)
            else:
                for enemy in self.enemies[:]:
                    if check_collision(bullet, enemy):
                        self.enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        self.xp += 10
                        break

        for enemy in self.enemies:
            enemy.move()

    def handle_events(self, events):
        if self.game_over:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()  # Reset the game state
                        self.game.set_screen('home')

    def reset_game(self):
        self.bullets = []
        self.xp = 0
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.game_over = False
        self.init_game()