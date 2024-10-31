import pygame
from src.constants import WHITE, RED
from src.constants import WIDTH

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 15
        self.color = (255, 0, 0)  # Red

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.speed
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.speed *= -1
            self.y += 80