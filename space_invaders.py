import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.speed = 5
        self.color = (139, 69, 19)  # brown
        self.ball_radius = 15
        self.stick_width = 10

    def draw(self, surface):
        # Draw stick
        pygame.draw.rect(surface, self.color, (self.x + self.width//2 - self.stick_width//2, self.y, self.stick_width, self.height - self.ball_radius))
        
        # Draw left ball
        pygame.draw.circle(surface, self.color, (self.x + self.ball_radius, self.y + self.height - self.ball_radius), self.ball_radius)
        
        # Draw right ball
        pygame.draw.circle(surface, self.color, (self.x + self.width - self.ball_radius, self.y + self.height - self.ball_radius), self.ball_radius)

    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.speed
        elif direction == 'right' and self.x < WIDTH - self.width:
            self.x += self.speed

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20
        self.color = (255, 255, 255)  # White
        self.speed = 10

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 1
        self.color = (255, 0, 0)  # Red

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.speed
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.speed *= -1
            self.y += 20  # move down when reaching screen edge

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(WIDTH // 2 - 30, HEIGHT - 60)
        self.enemies = [Enemy(x * 60 + 50, 50) for x in range(10)]  # Create 10 enemies
        self.running = True
        self.bullets = []
        self.xp = 0 # user starting xp
        self.can_shoot = True #this is to make sure the player can only shoot one bullet at a time
        self.enemy_respawn_timer = 0
        self.enemy_respawn_delay = 10  # 3 seconds at 60 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.can_shoot:
                    self.bullets.append(Bullet(self.player.x + self.player.width // 2 - 5, self.player.y - 10))
                    self.can_shoot = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.can_shoot = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move('left')
        if keys[pygame.K_RIGHT]:
            self.player.move('right')

    def update(self):
        for enemy in self.enemies:
            enemy.move()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.y -= bullet.speed
            if bullet.y < 0:
                self.bullets.remove(bullet)
            else:
                for enemy in self.enemies[:]:
                    if (bullet.x < enemy.x + enemy.width and
                        bullet.x + bullet.width > enemy.x and
                        bullet.y < enemy.y + enemy.height and
                        bullet.y + bullet.height > enemy.y):
                        self.enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        self.xp += 10
                        break

        # Respawn enemies
        if len(self.enemies) < 10:
            self.enemy_respawn_timer += 1
            if self.enemy_respawn_timer >= self.enemy_respawn_delay:
                self.enemies.append(Enemy(random.randint(0, WIDTH - 40), 50))
                self.enemy_respawn_timer = 0

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        xp_text = pygame.font.Font(None, 36).render(f"XP: {self.xp}", True, (255, 255, 255))
        self.screen.blit(xp_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # fps

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
