import math
from textwrap import fill
import pygame
import pygame.gfxdraw
import time
from numpy import random
from defs import *
from itertools import cycle

clock = pygame.time.Clock()
WHITE = (255, 255, 255)
WAVE_GAP = 0
SCORE_COUNTER = 0
DELTA_TIME = 0
GAME_TIME = 0
GAME_COUNTER = 0
GAME_SPEED = 2

WAVE_AMPLITUDE = 50
WAVE_FREQUENCY = 1
WAVE_SPEED = 1
CORD_Y = 0
CORD_X = 0
POINTS_MATRIX = [[0 for x in range(2)] for y in range(DISPLAY_H)]
posX = cycle(range(2))
pygame.init()
GAME_DISPLAY = pygame.display.set_mode(
    (DISPLAY_W, DISPLAY_H), pygame.NOFRAME)  # Make a window to show on
pygame.display.set_caption('Survive line')
label_font = pygame.font.Font("./usedMaterial/Nexa-Light.otf", DATA_FONT_SIZE)


def update_label(data, title, font, x, y, GAME_DISPLAY):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    GAME_DISPLAY.blit(label, (x, y))
    return y


def update_data_labels(GAME_DISPLAY, DELTA_TIME, GAME_TIME, font):
    y_pos = 10
    gap = 30
    x_pos = 10
    y_pos = update_label(round(1000/DELTA_TIME, 2), 'FPS', font,
                         x_pos, y_pos + gap, GAME_DISPLAY)
    y_pos = update_label(round(GAME_TIME/1000, 2), 'Game time',
                         font, x_pos, y_pos + gap, GAME_DISPLAY)


def fillGap(gap, gapDirection):
    # gapDirection to right is true, left is false
    insideY = CORD_Y
    if gap == 0:
        gap == 1
    if(gapDirection):
        if CORD_Y + (gap) > DISPLAY_H-1:
            gap = DISPLAY_H - CORD_Y - 1
        POINTS_MATRIX[CORD_Y + (gap)][0] = POINTS_MATRIX[CORD_Y][0]
        POINTS_MATRIX[CORD_Y + (gap)][1] = POINTS_MATRIX[CORD_Y][1]
        POINTS_MATRIX[CORD_Y][0] = POINTS_MATRIX[CORD_Y][1] = 0
        print(POINTS_MATRIX[CORD_Y-1][0], POINTS_MATRIX[CORD_Y+gap][0])
        for x in range(POINTS_MATRIX[CORD_Y-1][0]+1, POINTS_MATRIX[CORD_Y+gap][0], (gap//gap)):
            POINTS_MATRIX[insideY][next(posX)] = x
            POINTS_MATRIX[insideY][next(posX)] = -SCORE_COUNTER+1
            if insideY < 799:
                insideY += 1
    else:
        if CORD_Y + (gap) > DISPLAY_H-1:
            gap = DISPLAY_H - CORD_Y - 1
        POINTS_MATRIX[CORD_Y + (gap)][0] = POINTS_MATRIX[CORD_Y][0]
        POINTS_MATRIX[CORD_Y + (gap)][1] = POINTS_MATRIX[CORD_Y][1]
        POINTS_MATRIX[CORD_Y][0] = POINTS_MATRIX[CORD_Y][1] = 0
        print(POINTS_MATRIX[CORD_Y-1][0], POINTS_MATRIX[CORD_Y+gap][0])
        for x in range(POINTS_MATRIX[CORD_Y-1][0]-1, POINTS_MATRIX[CORD_Y+gap][0], -(gap//gap)):
            POINTS_MATRIX[insideY][next(posX)] = x
            POINTS_MATRIX[insideY][next(posX)] = -SCORE_COUNTER
            if insideY < 799:
                insideY += 1
    print("Moved a point")


def checkGap():
    # gapDirection = True  # to right is true, left is false
    if (POINTS_MATRIX[CORD_Y-1][0]-POINTS_MATRIX[CORD_Y][0] > 2):
        gap = (POINTS_MATRIX[CORD_Y-1][0]-POINTS_MATRIX[CORD_Y][0])-1
        fillGap(gap, False)
    elif(POINTS_MATRIX[CORD_Y][0] - POINTS_MATRIX[CORD_Y-1][0] > 1) and (CORD_Y not in {1, 2, 3}):
        gap = (POINTS_MATRIX[CORD_Y][0] - POINTS_MATRIX[CORD_Y-1][0]) - 1
        fillGap(gap, True)
        print("Gap between the left point and next right point is: " +str( gap))


def generateWave():
    global CORD_Y, CORD_X, SCORE_COUNTER
    checkGap()
    if CORD_Y < DISPLAY_H-1:
        CORD_Y += 1
    else:
        CORD_Y = 0

    CORD_X = int((DISPLAY_H/2) + WAVE_AMPLITUDE*math.sin(WAVE_FREQUENCY *
                 ((float(CORD_Y)/-DISPLAY_W)*(2*math.pi) + (WAVE_SPEED*time.time()))))
    if CORD_X-50-WAVE_GAP > DISPLAY_W:
        CORD_X = DISPLAY_W+50+WAVE_GAP
    elif (CORD_X < DISPLAY_W//2):
        CORD_X = DISPLAY_W//2

    POINTS_MATRIX[CORD_Y][next(posX)] = CORD_X
    POINTS_MATRIX[CORD_Y][next(posX)] = -SCORE_COUNTER


def changeSpeed():
    global FPS, WAVE_GAP, GAME_SPEED
    if(SCORE_COUNTER % (100 * (GAME_SPEED//2)) == 0) and FPS < 120:
        FPS += 2
        GAME_SPEED *= GAME_SPEED
        print("incremented speed of game")


def changeWave():
    global WAVE_FREQUENCY, WAVE_AMPLITUDE, WAVE_SPEED, WAVE_GAP
    if (SCORE_COUNTER % 10 == 0) and WAVE_GAP < 60:
        WAVE_GAP += 1
        print("Incremented line gap")
    if (SCORE_COUNTER % 100 == 0):
        # WAVE_FREQUENCY = random.randint(1, 6)
        WAVE_AMPLITUDE = random.randint(50, WAVE_AMPLITUDE+WAVE_GAP)


def debug(SCORE_COUNTER, WAVE_GAP):
    global CORD_Y
    print(SCORE_COUNTER)


def run_game():
    # Make a surface to draw on
    surface = pygame.Surface((DISPLAY_W, DISPLAY_H))
    surface.fill(background_color)
    running = True

    while running:
        DELTA_TIME = clock.tick(FPS)
        # GAME_TIME += DELTA_TIME
        surface.fill(background_color)

        global SCORE_COUNTER, GAME_COUNTER
        SCORE_COUNTER += 1
        debug(SCORE_COUNTER, WAVE_GAP)

        changeSpeed()
        changeWave()
        generateWave()

        for Y_CORD in range(800):
            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(
                posX)]-55-WAVE_GAP, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WHITE)
            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(
                posX)]-350+WAVE_GAP, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WHITE)
        pygame.display.flip()

        if (SCORE_COUNTER % 1 == 0):
            GAME_DISPLAY.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
                print("A key is pressed, will stop now\n")

        # update_data_labels(GAME_DISPLAY, DELTA_TIME, GAME_TIME, label_font)


if __name__ == "__main__":
    run_game()
