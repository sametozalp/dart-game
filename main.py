import pygame
import threading
import time
from ball import Ball
from gun import Gun
import tkinter as tk
import serial
import pydirectinput
from tkinter import messagebox

root = tk.Tk()

SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

ball_timer = 7
timer = 23
score = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

running = True

pygame.mixer.init()
sound = pygame.mixer.Sound("gun.mp3")

arduino = serial.Serial('COM8', 115200, timeout=.1)     #serial input from arduino. change COM port to wherever your arduino is connected

pydirectinput.PAUSE = 0

keysDown = {}   #list of currently pressed keys
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg = pygame.image.load('sky.png')
def background_sky():
    size = pygame.transform.scale(bg, (1920,1080))
    screen.blit(size, (0,0))

def keyDown(key):               #what to do if key pressed. takes value from handleJoyStickAsArrowKeys
    keysDown[key] = True        #adds key to KeysDown list
    pydirectinput.keyDown(key)  #runs pydirectinput using key from (argument)
    #print('Down: ', key)       #remove '#' from print to test data stream


def keyUp(key):                     #what to do if key released. takes value from handleJoyStickAsArrowKeys
    if key in keysDown:
        del (keysDown[key])         #remove key from KeysDown
        pydirectinput.keyUp(key)    #runs pydirectinput using key from (argument)
        #print('Up: ', key)         #remove '#' from print to test data stream


def handleJoyStickAsArrowKeys(x, y, z):      #note that the x and y directions are swapped due to the way I orient my thumbstick
    if x == 2:          #0 is up on joystick
        keyDown('up')   #add up key to keyDown (argument)
        keyUp('down')   #add down key to keyUp (argument), as you can't press up and down together
    elif x == 0:        #2 is down on joystick
        keyDown('down')
        keyUp('up')
    else:               #1 is neutral on joystick
        keyUp('up')
        keyUp('down')

    if y == 2:          #2 is right on joystick
        keyDown('right')
        keyUp('left')
    elif y == 0:        #0 is left on joystick
        keyDown('left')
        keyUp('right')
    else:               #1 is neutral on joystick
        keyUp('left')
        keyUp('right')
        
def main():
    pygame.init()
    global score
    global running
    
    pygame.display.set_caption("Dart Game")

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    balls_group = pygame.sprite.Group()

    gun = Gun()
    all_sprites.add(gun)

    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get(): # olayları al
            
            if event.type == pygame.QUIT:
                running = False
                global ball_timer
                global timer
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
                        if score % 3 == 0:
                            timer = timer + 3
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

        #screen.fill(WHITE)
        background_sky()
        all_sprites.draw(screen)

        score_text = font.render("Skor: {}".format(score), True, BLACK)
        ball_timer_text = font.render("Topun yerinin değişmesine kalan süre: {}".format(ball_timer), True, BLACK)
        timer_text = font.render("Kalan zaman: {}".format(timer), True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(ball_timer_text, (10, 40))
        screen.blit(timer_text, (10, 70))

        pygame.display.flip()
        clock.tick(60)
        
        #############################################################3
        rawdata = arduino.readline()            #read serial data from arduino one line at a time
        data = str(rawdata.decode('utf-8'))     #decode the raw byte data into UTF-8
        if data.startswith("S"):                #make sure the read starts in the correct place
            dx = int(data[1])                   #X direction is second digit in data (data[0] is 'S')
            dy = int(data[3])                   #Y direction is fourth digit in data
            JSButton = int(data[5])             #JSButton is sixth digit in data
            #print(dx, dy, JSButton)            #remove '#' from print to test data stream
            handleJoyStickAsArrowKeys(dx, dy, JSButton)     #run body of code using dx, dy and JSButton as inputs
    
    root.destroy()

    show_alert()

    print("Oyun sonlandırıldı..")

    pygame.quit()

def time_counter():
    global ball_timer
    global timer
    global running
    
    while(ball_timer >= 0 and timer > 0):
        time.sleep(1)
        ball_timer = ball_timer - 1
        timer = timer - 1
        if ball_timer < 0:
            score_balltimer()
    
    running = False
    
    
def score_balltimer():
    global ball_timer        
    if score < 5:
        ball_timer = 7
    elif score < 10:
        ball_timer = 6 
    elif score < 15:
        ball_timer = 5
    elif score < 20:
        ball_timer = 4
    elif score < 25:
        ball_timer = 3

def show_alert():
    messagebox.showinfo("Oyun Bitti", f"Skorunuz: {score}")
    
if __name__ == "__main__":
    thread = threading.Thread(target=time_counter)
    thread.start()
    main()