import math
import pygame
import pygame.gfxdraw
import time
from numpy import random
from defs import *
from itertools import cycle
from apscheduler.schedulers.background import BackgroundScheduler


clock = pygame.time.Clock()
LINE_GAP = 0
SCORE_COUNTER = 0
DELTA_TIME = 0
GAME_TIME = 0
GAME_COUNTER = 0  # COUNTER
CORD_Y= 0
CORD_X= 0
POINTS_MATRIX = [[0 for x in range(2)] for y in range(DISPLAY_H)]
posX = cycle(range(2))
pygame.init()
# Make a window to show on
GAME_DISPLAY = pygame.display.set_mode((DISPLAY_W, DISPLAY_H), pygame.NOFRAME)
pygame.display.set_caption('Survive line')

label_font = pygame.font.Font("./usedMaterial/Nexa-Light.otf", DATA_FONT_SIZE)



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


def debug(SCORE_COUNTER, LINE_GAP, GAME_COUNTER):
    global CORD_Y
    print(SCORE_COUNTER)
    if (SCORE_COUNTER % 20 == 0):
        LINE_GAP += 1
        print("Incremented line gap")
    if (SCORE_COUNTER % 1 == 0) and GAME_COUNTER < 799:
        GAME_COUNTER += 1
        CORD_Y+=1

    pygame.init()
    # Make a window to show on
    gameDisplay = pygame.display.set_mode(
        (DISPLAY_W, DISPLAY_H), pygame.NOFRAME)
    pygame.display.set_caption('Survive line')

    # Make a surface to draw on
    surface = pygame.Surface((DISPLAY_W, DISPLAY_H))
    surface.fill(background_color)
    running = True

    label_font = pygame.font.Font(
        "./usedMaterial/Nexa-Light.otf", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
    lineGap = 0
    scoreCounter = 0
    dt = 0
    gameTime = 0
    CC = 0
    y = 0
    x=0
    while running:

        dt = clock.tick(30)
        gameTime += dt

        # Redraw the background
        surface.fill(background_color)

        amplitude = 50  # in px

        overallY = 300
        # Update sine wave

        # if (scoreCounter % 5 == 0):
        #     frequency = random.randint(1, 6)

        frequency = 1
        speed = 1
        scoreCounter += 1
        w, h = 2, DISPLAY_H
        matrix = [[0 for x in range(w)] for y in range(h)]
        posX = cycle(range(2))

        print(scoreCounter)
        if (scoreCounter % 20 == 0):
            lineGap += 1
            print("inside inside")
        if (scoreCounter % 1 == 0) and CC < 799:
            CC += 1
            y += 1
        # if (scoreCounter%30 ==0):
        x = int((DISPLAY_H/2) + amplitude*math.sin(frequency *
                                                   ((float(y)/-DISPLAY_W+50)*(2*math.pi) + (speed*time.time()))))
        matrix[y][next(posX)] = x
        matrix[y][next(posX)] = y
        pygame.gfxdraw.pixel(gameDisplay, matrix[y][next(posX)]-55, matrix[y][next(posX)], (255, 255, 255))
            
        # for show in range(0,DISPLAY_H):
        #     pygame.gfxdraw.pixel(gameDisplay, matrix[y][next(posX)]-55, matrix[y][next(posX)]+show, (255, 255, 255))
            
        pygame.display.flip()
        # for y in range(0,DISPLAY_H):
        #     matrix[y,posX.next()]
        #     pygame.gfxdraw.pixel(gameDisplay, cordX-50, cordY, (255, 255, 255))

        #     pygame.display.flip()

        if (scoreCounter % 1 == 0):
            gameDisplay.blit(surface, (0, 0))
            # surface.set_at((x-50-lineGap, y), (255,255,255))
            # surface.set_at((x-350+lineGap, y), (255, 255, 255))

        # for cordX,cordY in matrix.items():
        #     pygame.gfxdraw.pixel(gameDisplay,cordX-50, cordY, (255, 255, 255))
        # for x in range(0, DISPLAY_H):

        # Put the surface we draw on, onto the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
                print("A key is pressed, will stop now\n")

        # update_data_labels(gameDisplay, dt, gameTime, label_font)


if __name__ == "__main__":
    run_game()
