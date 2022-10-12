from numpy import random
from defs import *

import pygame

PARTICLES = []
BALL_CORD_Y = 550
BALL_CORD_X = DISPLAY_W//2
BALL_MOVE_SPEED = 5
BALL_RADIUS = 12


def collision(waveGap):
    global keepGenerating
    ball = pygame.Rect(BALL_CORD_X, BALL_CORD_Y, BALL_RADIUS, BALL_RADIUS)
    for x in range(245, 255):
        if ball.right >= POINTS_LIST[x]-55-waveGap:
            print("hit from " + str(x))
            return keepGenerating == False

        if ball.left <= POINTS_LIST[x]-340+waveGap:
            print("hit from " + str(x))
            return keepGenerating == False


def drawCircle(SCREEN, x, y, radius, color):
    pygame.gfxdraw.aacircle(SCREEN, x, y, radius, color)
    pygame.gfxdraw.filled_circle(SCREEN, x, y, radius, color)


def moveCircle():
    global BALL_CORD_X
    PRESSED_KEYS = pygame.key.get_pressed()
    if PRESSED_KEYS[pygame.K_RIGHT] and BALL_CORD_X + (BALL_RADIUS) < DISPLAY_W-4:
        BALL_CORD_X += BALL_MOVE_SPEED
    if PRESSED_KEYS[pygame.K_LEFT] and BALL_CORD_X > 0 + BALL_RADIUS+4:
        BALL_CORD_X -= BALL_MOVE_SPEED
    return BALL_CORD_X


def reset():
    global BALL_CORD_Y, BALL_CORD_X, POINTS_LIST, keepGenerating, PARTICLES, SCORE_COUNTER
    BALL_CORD_Y = 550
    BALL_CORD_X = DISPLAY_W//2
    POINTS_LIST.clear()
    keepGenerating = True
    PARTICLES.clear()
    return SCORE_COUNTER == 0
