import math
import pygame
import time
from numpy import random
from defs import *




def update_label(data, title, font, x, y, gameDisplay):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y


def update_data_labels(gameDisplay, dt, gameTime, font):
    y_pos = 10
    gap = 30
    x_pos = 10
    y_pos = update_label(round(1000/dt, 2), 'FPS', font,
                         x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(gameTime/1000, 2), 'Game time',
                         font, x_pos, y_pos + gap, gameDisplay)


def run_game():

    pygame.init()
    # Make a window to show on
    gameDisplay = pygame.display.set_mode(
        (DISPLAY_W, DISPLAY_H), pygame.NOFRAME)
    pygame.display.set_caption('Survive line')

    # Make a surface to draw on
    surface = pygame.Surface((DISPLAY_W, DISPLAY_H))
    surface.fill(background_color)
    running = True

    label_font = pygame.font.Font("../Nexa-Light.otf", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
    lineGap=0
    scoreCounter=0
    dt = 0
    gameTime = 0

    while running:

        dt = clock.tick(FPS)
        gameTime += dt

        # Redraw the background
        surface.fill(background_color)

        # Update sine wave
        frequency = 1
        
        speed = 2
        scoreCounter+=1
        print(scoreCounter)
        if  (scoreCounter%20==0):
            lineGap+=1
            print("inside inside")

        for x in range(0, DISPLAY_H):
            y = int((DISPLAY_H/2) + amplitude*math.sin(frequency *
                    ((float(x)/-DISPLAY_W+50)*(2*math.pi) + (speed*time.time()))))
            # amplitude = random.randint(100)
            surface.set_at((y-55-lineGap, x), (255,255,255))
            surface.set_at((y-345+lineGap, x), (255,255,255))


        # Put the surface we draw on, onto the screen
        gameDisplay.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
                print("A key is pressed, will stop now\n")

        update_data_labels(gameDisplay, dt, gameTime, label_font)

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
