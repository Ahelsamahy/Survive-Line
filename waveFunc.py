import math
from tkinter import FALSE
from numpy import random
from defs import *

from mainL import *

import pygame

def generateWave():
    global WAVE_CORD_X, SCORE_COUNTER
    # checkGap()
    if len(POINTS_LIST) == DISPLAY_H-1:
        POINTS_LIST.pop(0)

    WAVE_CORD_X = int((DISPLAY_H/2) + WAVE_AMPLITUDE*math.sin(WAVE_FREQUENCY *
                      ((float(0)/-DISPLAY_W)*(2*math.pi) + (WAVE_SPEED*time.time()))))

    POINTS_LIST.append(WAVE_CORD_X)


def changeSpeed():
    global FPS, WAVE_GAP, GAME_SPEED
    if(SCORE_COUNTER % (100 * (GAME_SPEED//2)) == 0) and FPS < 60:
        FPS += 2
        GAME_SPEED *= GAME_SPEED
        print("incremented speed of game")

