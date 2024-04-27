import pygame
import threading
import time
from ball import Ball
from gun import Gun

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ball_timer = 7
score = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.mixer.init()
sound = pygame.mixer.Sound("gun.mp3")

def main():
    pygame.init()
    global score
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dart Game")

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    balls_group = pygame.sprite.Group()

    gun = Gun()
    all_sprites.add(gun)

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get(): # olayları al
            
            if event.type == pygame.QUIT:
                running = False
                global ball_timer
                ball_timer = 0
                
            # tus bas kontrol
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gun.move_left()
                elif event.key == pygame.K_RIGHT:
                    gun.move_right()
                elif event.key == pygame.K_DOWN:
                    gun.move_down()
                elif event.key == pygame.K_UP:
                    gun.move_up()
                elif event.key == pygame.K_SPACE:
                    sound.play()
                    if gun.fire(balls_group):
                        score += 1
                        score_balltimer()
                        

            # tus bırak kontrol
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    gun.stop_move_left()
                elif event.key == pygame.K_RIGHT:
                    gun.stop_move_right()
                elif event.key == pygame.K_UP:
                    gun.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    gun.stop_move_down()
                    

        if len(balls_group) < 1:
            ball = Ball()
            balls_group.add(ball)
            all_sprites.add(ball)  # ana grup

        if ball_timer == 0:    
            score_balltimer()
            for ball in balls_group:
                 ball.reset_position()
            
        all_sprites.update()

        screen.fill(WHITE)
        all_sprites.draw(screen)

        score_text = font.render("Skor: {}".format(score), True, BLACK)
        ball_timer_text = font.render("Topun yerinin değişmesine kalan süre: {}".format(ball_timer), True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(ball_timer_text, (10, 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def time_counter():
    global ball_timer
    while(ball_timer >= 0):
        if ball_timer == 0:
            score_balltimer()
        time.sleep(1)
        ball_timer = ball_timer - 1
        
def score_balltimer():
    global ball_timer        
    if score < 5:
        ball_timer = 2
    elif score < 10:
        ball_timer = 6 
    elif score < 15:
        ball_timer = 5
    elif score < 20:
        ball_timer = 4

if __name__ == "__main__":
    thread = threading.Thread(target=time_counter)
    thread.start()
    main()