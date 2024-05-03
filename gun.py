import pygame
import tkinter as tk

root = tk.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
BLACK = (0, 0, 0)


class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("hedef.png")  # Resim dosyasının doğru yolunu gir
        self.image = pygame.transform.scale(self.original_image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 200
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_left:
            if self.rect.x > 0:
                self.rect.x -= 15
        elif self.moving_right:
            if self.rect.x < SCREEN_WIDTH-200:
                self.rect.x += 15
        elif self.moving_up:
            if self.rect.y > 0:
                self.rect.y -= 15
        elif self.moving_down:
            if self.rect.y < SCREEN_HEIGHT-200:
                self.rect.y += 15

    def move_left(self):
        self.moving_left = True

    def move_right(self):
        self.moving_right = True
        
    def move_up(self):
        self.moving_up = True

    def move_down(self):
        self.moving_down = True

    def stop_move_left(self):
        self.moving_left = False

    def stop_move_right(self):
        self.moving_right = False
        
    def stop_move_up(self):
        self.moving_up = False

    def stop_move_down(self):
        self.moving_down = False

    def fire(self, balls_group):
        for ball in balls_group:
            if self.rect.colliderect(ball.rect):
                ball.reset_position()
                return True
        return False