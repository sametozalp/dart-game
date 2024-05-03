import random
import pygame
import tkinter as tk

root = tk.Tk()
RED = (255, 0, 0)
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.Surface([50, 50])
        #self.image.fill(RED)
        #self.image = pygame.image.load("drone.png")
        self.original_image = pygame.image.load("drone.png")  # Resim dosyasının doğru yolunu gir
        self.image = pygame.transform.scale(self.original_image, (200, 200))
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - 200)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 200)
