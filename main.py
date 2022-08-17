import math
import pygame
import pygame.gfxdraw
import time
from numpy import random
from defs import *
from itertools import cycle

clock = pygame.time.Clock()
WHITE = (255, 255, 255)
LINE_GAP = 0
SCORE_COUNTER = 0
DELTA_TIME = 0
GAME_TIME = 0
GAME_COUNTER = 0
CORD_Y = 0
CORD_X = 0
Y_AXIS_INCREMENT = 0
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


def generateWave():
    global CORD_Y
    if CORD_Y < DISPLAY_H-1:
        CORD_Y += 1
    else:
        CORD_Y = 0
    amplitude = 50
    frequency = 1
    speed = int(FPS/30)
    x = int((DISPLAY_H/2) + amplitude*math.sin(frequency *
            ((float(CORD_Y)/-DISPLAY_W)*(2*math.pi) + (speed*time.time()))))
    POINTS_MATRIX[CORD_Y][next(posX)] = x
    POINTS_MATRIX[CORD_Y][next(posX)] = -SCORE_COUNTER


def debug(SCORE_COUNTER, LINE_GAP):
    global CORD_Y
    print(SCORE_COUNTER)
    if (SCORE_COUNTER % 20 == 0):
        LINE_GAP += 1
        print("Incremented line gap")


def run_game():
    # Make a surface to draw on
    surface = pygame.Surface((DISPLAY_W, DISPLAY_H))
    surface.fill(background_color)
    running = True

    while running:
        DELTA_TIME = clock.tick(FPS)
        # GAME_TIME += DELTA_TIME
        surface.fill(background_color)

        # if (scoreCounter % 5 == 0):
        #     frequency = random.randint(1, 6)

        global SCORE_COUNTER, GAME_COUNTER
        SCORE_COUNTER += 1
        debug(SCORE_COUNTER, LINE_GAP)

        generateWave()

        for Y_CORD in range(800):
            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(posX)]-55, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WHITE)
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
