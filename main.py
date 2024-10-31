import pygame
from src.game.game import Game

def main():
    pygame.init()
    pygame.display.set_caption("Space Invaders")
    
    game = Game()
    game.run()

if __name__ == "__main__":
    main()