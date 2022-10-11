
from tkinter import FALSE
from numpy import random
from defs import *

from mainL import *

import pygame

PARTICLES = []
BALL_CORD_Y = 550
BALL_CORD_X = DISPLAY_W//2
BALL_MOVE_SPEED = 5
BALL_RADIUS = 12

def collision():
    global keepGenerating
    ball = pygame.Rect(BALL_CORD_X, BALL_CORD_Y, BALL_RADIUS, BALL_RADIUS)
    for x in range(245, 255):
        if ball.right >= POINTS_LIST[x]-55:
            print("hit from " + str(x))
            return keepGenerating == FALSE

        if ball.left <= POINTS_LIST[x]-340:
            print("hit from " + str(x))
            return keepGenerating == FALSE

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

def ballParticles():
    # [loc, velocity, timer]
    PARTICLES.append([[BALL_CORD_X, BALL_CORD_Y], [
                     random.randint(0, 20) / 10 - 1, -3], random.randint(4, 6)])

    for particle in PARTICLES:
        particle[0][0] -= particle[1][0]
        particle[0][1] -= particle[1][1]
        particle[2] -= 0.1

        pygame.draw.circle(GAME_DISPLAY, (255, 255, 255), [int(
            particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            PARTICLES.remove(particle)

def reset():
    global BALL_CORD_Y, BALL_CORD_X, POINTS_LIST, keepGenerating, PARTICLES,SCORE_COUNTER
    BALL_CORD_Y = 550
    BALL_CORD_X = DISPLAY_W//2
    SCORE_COUNTER = 0
    POINTS_LIST.clear()
    keepGenerating = TRUE
    PARTICLES.clear()