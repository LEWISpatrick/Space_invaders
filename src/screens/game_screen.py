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
        self.xp_p1 = 0
        self.xp_p2 = 0
        self.can_shoot_p1 = True
        self.can_shoot_p2 = True
        self.shoot_cooldown_p1 = 0
        self.shoot_cooldown_p2 = 0
        self.game_over = False
        self.enemy_speed = 15  # Default speed
        self.init_game()
    
    def init_game(self):
        if self.multiplayer:
            # Player 1 (top) with WASD and F, shoots down
            p1_controls = {
                'left': pygame.K_a,
                'right': pygame.K_d,
                'shoot': pygame.K_f
            }
            self.player = Player(WIDTH // 2 - 30, HEIGHT - 400, p1_controls, shoot_direction=-1)
            self.player = Player(WIDTH // 2 - 30, HEIGHT - 200, p1_controls)
            # Player 2 (bottom) with arrow keys and space, shoots up
            self.player2 = Player(WIDTH // 2 + 30, HEIGHT - 60)
        else:
            # Single player with arrow keys and space
            self.player = Player(WIDTH // 2 - 30, HEIGHT - 60)

        self.enemies = [Enemy(x * 60 + 50, 50, self.enemy_speed) for x in range(ENEMY_COUNT)]

    def set_difficulty(self, speed):
        self.enemy_speed = speed
        for enemy in self.enemies:
            enemy.speed = speed

    def update(self):
        if self.game_over:
            return

        # Check if all enemies are defeated
        if len(self.enemies) == 0:
            self.game_over = True
            return

        # Handle player 1 shooting cooldown
        if not self.can_shoot_p1:
            self.shoot_cooldown_p1 += 1
            if self.shoot_cooldown_p1 >= 20:
                self.can_shoot_p1 = True
                self.shoot_cooldown_p1 = 0

        # Handle player 2 shooting cooldown in multiplayer
        if self.multiplayer and not self.can_shoot_p2:
            self.shoot_cooldown_p2 += 1
            if self.shoot_cooldown_p2 >= 20:
                self.can_shoot_p2 = True
                self.shoot_cooldown_p2 = 0

        # Check enemy collisions with players
        for enemy in self.enemies:
            if check_collision_player(self.player, enemy):
                self.game_over = True
                return
            if self.multiplayer and check_collision_player(self.player2, enemy):
                self.game_over = True
                return

        # Handle player 1 input
        if self.can_shoot_p1:
            bullet = self.player.handle_input(self.game.screen)
            if bullet:
                self.bullets.append(('p1', bullet))
                self.can_shoot_p1 = False

        # Handle player 2 input in multiplayer
        if self.multiplayer and self.can_shoot_p2:
            bullet = self.player2.handle_input(self.game.screen)
            if bullet:
                self.bullets.append(('p2', bullet))
                self.can_shoot_p2 = False

        # Update bullets and check collisions
        for bullet_info in self.bullets[:]:
            player_id, bullet = bullet_info
            bullet.move()
            # Check if bullet is off screen (both directions)
            if bullet.y < 0 or bullet.y > HEIGHT:
                self.bullets.remove(bullet_info)
            else:
                for enemy in self.enemies[:]:
                    if check_collision(bullet, enemy):
                        self.enemies.remove(enemy)
                        self.bullets.remove(bullet_info)
                        if player_id == 'p1':
                            self.xp_p1 += 10
                        else:
                            self.xp_p2 += 10
                        break

        # Update enemy positions
        for enemy in self.enemies:
            enemy.move()

    def draw(self, surface):
        surface.fill((30, 30, 30))  # Background
        
        # Draw players and game elements
        self.player.draw(surface)
        if self.multiplayer:
            self.player2.draw(surface)
        
        for enemy in self.enemies:
            enemy.draw(surface)
        for _, bullet in self.bullets:
            bullet.draw(surface)

        # Draw scores
        font = pygame.font.Font(None, 36)
        if self.multiplayer:
            p1_text = font.render(f'Player 1: {self.xp_p1}', True, (255, 255, 255))
            p2_text = font.render(f'Player 2: {self.xp_p2}', True, (255, 255, 255))
            surface.blit(p1_text, (10, 10))
            surface.blit(p2_text, (10, 50))
        else:
            score_text = font.render(f'Score: {self.xp_p1}', True, (255, 255, 255))
            surface.blit(score_text, (10, 10))

        # Draw game over screen
        if self.game_over:
            self.draw_game_over(surface)

    def draw_game_over(self, surface):
        font = pygame.font.Font(None, 74)
        game_over_text = font.render('GAME OVER', True, (255, 0, 0))
        
        if self.multiplayer:
            score_text = font.render(f'P1: {self.xp_p1} | P2: {self.xp_p2}', True, (255, 255, 255))
        else:
            score_text = font.render(f'Final Score: {self.xp_p1}', True, (255, 255, 255))
            
        restart_text = font.render('Press SPACE to continue', True, (255, 255, 255))
        
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
        
        surface.blit(game_over_text, game_over_rect)
        surface.blit(score_text, score_rect)
        surface.blit(restart_text, restart_rect)
    def reset_game(self):
        self.bullets = []
        self.xp_p1 = 0
        self.xp_p2 = 0
        self.can_shoot_p1 = True
        self.can_shoot_p2 = True
        self.shoot_cooldown_p1 = 0
        self.shoot_cooldown_p2 = 0
        self.game_over = False
        self.init_game()

    def handle_events(self, events):
        if self.game_over:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.game.set_screen('home')