import pygame
from src.constants import WIDTH
from src.entities.bullet import Bullet

class Player:
    def __init__(self, x, y, controls=None, shoot_direction=1):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.speed = 5
        self.color = (139, 69, 19)  # brown
        self.ball_radius = 15
        self.stick_width = 10
        self.shoot_direction = shoot_direction
        self.controls = controls or {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'shoot': pygame.K_SPACE
        }

    def draw(self, surface):
        # Draw stick
        pygame.draw.rect(surface, self.color, (self.x + self.width//2 - self.stick_width//2, self.y, self.stick_width, self.height - self.ball_radius))
        
        # Draw left ball
        pygame.draw.circle(surface, self.color, (self.x + self.ball_radius, self.y + self.height - self.ball_radius), self.ball_radius)
        
        # Draw right ball
        pygame.draw.circle(surface, self.color, (self.x + self.width - self.ball_radius, self.y + self.height - self.ball_radius), self.ball_radius)

    def shoot(self, surface):
        bullet_x = self.x + self.width//2 - 5
        bullet_y = self.y
        bullet = Bullet(bullet_x, bullet_y, self.shoot_direction)
        bullet.draw(surface)
        return bullet

    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.speed
        elif direction == 'right' and self.x < WIDTH - self.width:
            self.x += self.speed

    def handle_input(self, surface):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']]:
            self.move('left')
        if keys[self.controls['right']]:
            self.move('right')
        if keys[self.controls['shoot']]:
            return self.shoot(surface)
        return None
