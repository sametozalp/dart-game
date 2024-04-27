import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)


class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 50
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_left:
            if self.rect.x > 0:
                self.rect.x -= 5
        elif self.moving_right:
            if self.rect.x < SCREEN_WIDTH-20:
                self.rect.x += 5
        elif self.moving_up:
            if self.rect.y > 0:
                self.rect.y -= 5
        elif self.moving_down:
            if self.rect.y < SCREEN_HEIGHT-20:
                self.rect.y += 5

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