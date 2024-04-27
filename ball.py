import random
import pygame

RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - 20)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 20)
