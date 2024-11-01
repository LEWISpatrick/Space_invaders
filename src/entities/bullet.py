import pygame
from src.constants import WHITE

class Bullet:
    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20
        self.color = WHITE
        self.speed = 10
        self.direction = direction  # 1 for up, -1 for down

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y -= (self.speed * self.direction)

