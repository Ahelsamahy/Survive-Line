import math
import time
from numpy import random

from defs import *


def generateWave():
    global WAVE_CORD_X, SCORE_COUNTER
    # checkGap()
    if len(POINTS_LIST) == DISPLAY_H-1:
        POINTS_LIST.pop(0)

    WAVE_CORD_X = int((DISPLAY_H/2) + WAVE_AMPLITUDE*math.sin(WAVE_FREQUENCY *
                      ((float(0)/-DISPLAY_W)*(2*math.pi) + (WAVE_SPEED*time.time()))))

    POINTS_LIST.append(WAVE_CORD_X)


def changeSpeed(Counter):
    global FPS, GAME_SPEED
    if(Counter % (100 * (GAME_SPEED//2)) == 0) and FPS < 100:
        FPS += 2
        GAME_SPEED *= GAME_SPEED
        print("incremented speed of game")


def changeWave(Counter):
    global WAVE_FREQUENCY, WAVE_AMPLITUDE, WAVE_SPEED, WAVE_GAP
    if (Counter % 10 == 0) and WAVE_GAP < 80:
        WAVE_GAP += 1
        print("Incremented line gap")
    if (Counter % 200 == 0):
        WAVE_AMPLITUDE = random.randint(50, WAVE_AMPLITUDE+WAVE_GAP)
    return WAVE_GAP, WAVE_AMPLITUDE


def fillGap(gap, gapDirection):
    # gapDirection to right is true, left is false
    global WAVE_CORD_Y
    if WAVE_CORD_Y % 799 == 0:
        WAVE_CORD_Y = 1
    if WAVE_CORD_Y + (gap) > DISPLAY_H-1:
        gap = DISPLAY_H - WAVE_CORD_Y - 1
    if gap == 0:
        gap = 1
    insideY = WAVE_CORD_Y

    if(gapDirection):
        POINTS_LIST[WAVE_CORD_Y + (gap)][0] = POINTS_LIST[WAVE_CORD_Y][0]
        POINTS_LIST[WAVE_CORD_Y + (gap)][1] = POINTS_LIST[WAVE_CORD_Y][1]
        POINTS_LIST[WAVE_CORD_Y][0] = POINTS_LIST[WAVE_CORD_Y][1] = 0
        # print(POINTS_LIST[WAVE_CORD_Y-1][0],
        #   POINTS_LIST[WAVE_CORD_Y+gap][0])
        for x in range(POINTS_LIST[WAVE_CORD_Y-1][0]+1, POINTS_LIST[WAVE_CORD_Y+gap][0], (gap//gap)):
            POINTS_LIST[insideY][next(posX)] = x
            POINTS_LIST[insideY][next(posX)] = -SCORE_COUNTER+1
            if insideY < 799:
                insideY += 1
    else:
        POINTS_LIST[WAVE_CORD_Y + (gap)][0] = POINTS_LIST[WAVE_CORD_Y][0]
        POINTS_LIST[WAVE_CORD_Y + (gap)][1] = POINTS_LIST[WAVE_CORD_Y][1]
        POINTS_LIST[WAVE_CORD_Y][0] = POINTS_LIST[WAVE_CORD_Y][1] = 0
        # print(POINTS_LIST[WAVE_CORD_Y-1][0],
        #       POINTS_LIST[WAVE_CORD_Y+gap][0])
        for x in range(POINTS_LIST[WAVE_CORD_Y-1][0]-1, POINTS_LIST[WAVE_CORD_Y+gap][0], -(gap//gap)):
            POINTS_LIST[insideY][next(posX)] = x
            POINTS_LIST[insideY][next(posX)] = -SCORE_COUNTER
            if insideY < 799:
                insideY += 1


def checkGap():
    # gapDirection = True  # to right is true, left is false
    if (POINTS_LIST[WAVE_CORD_Y-1]-POINTS_LIST[WAVE_CORD_Y] > 1):
        gap = (POINTS_LIST[WAVE_CORD_Y-1]-POINTS_LIST[WAVE_CORD_Y])-1
        fillGap(gap, False)
    elif(POINTS_LIST[WAVE_CORD_Y] - POINTS_LIST[WAVE_CORD_Y-1] > 1) and (WAVE_CORD_Y not in {1, 2, 3}):
        gap = (POINTS_LIST[WAVE_CORD_Y] - POINTS_LIST[WAVE_CORD_Y-1]) - 1
        fillGap(gap, True)
