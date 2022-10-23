import math
import time
from numpy import random
import numpy as np

from defs import *
POINTS_I = 0


def changeSpeed(Counter):
    global FPS, GAME_SPEED
    if(Counter % (100 * (GAME_SPEED//2)) == 0) and FPS < 100:
        FPS += 2
        GAME_SPEED *= GAME_SPEED
        print("incremented speed of game")


def changeWave(Counter, waveGap):
    global WAVE_FREQUENCY, WAVE_AMPLITUDE, WAVE_SPEED
    if (Counter % 30 == 0) and waveGap < 80:
        waveGap += 1
        print("Incremented line gap")
    if (Counter % 50 == 0):
        WAVE_AMPLITUDE = random.randint(50, 51+waveGap)
    return waveGap, WAVE_AMPLITUDE


def generateWave():
    global WAVE_CORD_X, SCORE_COUNTER, POINTS_I

    if POINTS_I % 800 == 0:
        POINTS_I = 0

    WAVE_CORD_X = int((DISPLAY_H/2) + WAVE_AMPLITUDE*math.sin(WAVE_FREQUENCY *
                      ((float(0)/-DISPLAY_W)*(2*math.pi) + (WAVE_SPEED*time.time()))))

    # make the dot only to the right half of screen, elif for the left part
    if WAVE_CORD_X-WAVE_AMPLITUDE-WAVE_GAP > DISPLAY_W:
        WAVE_CORD_X = DISPLAY_W+50+WAVE_GAP
    elif WAVE_CORD_X-350-WAVE_GAP > DISPLAY_W:
        WAVE_CORD_X = DISPLAY_W+350+WAVE_GAP

    # not to generate dot that will overlap the left line
    if (WAVE_CORD_X < DISPLAY_W//2):
        WAVE_CORD_X = DISPLAY_W//2

    addPoint(POINTS_I, WAVE_CORD_X)
    checkGap()
    POINTS_I += 1


def addPoint(index, point):
    if POINTS_LIST[-1] != 0:
        POINTS_LIST.pop(0)
        POINTS_LIST.append(point)
    else:
        POINTS_LIST[index] = point


def checkGap():
    # gapDirection = True  # to right is true, left is false
    if (POINTS_I not in [0, 1]) and (POINTS_LIST[POINTS_I-1]-POINTS_LIST[POINTS_I] > 1):
        gap = (POINTS_LIST[POINTS_I-1] - POINTS_LIST[POINTS_I]) - 1
        fillGap(gap, False)
    elif (POINTS_I not in [0, 1]) and (POINTS_LIST[POINTS_I] - POINTS_LIST[POINTS_I-1] > 1):
        gap = (POINTS_LIST[POINTS_I] - POINTS_LIST[POINTS_I-1]) - 1
        fillGap(gap, True)


def fillGap(gap, gapDirection):
    # gapDirection to right is true, left is false
    global POINTS_I, POINTS_LIST
    if POINTS_I + (gap) >= DISPLAY_H-1:
        untilEnd = DISPLAY_H-POINTS_I
        toAddFromStart = gap-untilEnd
        del POINTS_LIST[:toAddFromStart]
        toAdd = [0]*toAddFromStart
        POINTS_LIST.extend(toAdd)
        # POINTS_I = toAddFromStart
    if gap == 0:
        gap = 1
    insideY = POINTS_I
    if(gapDirection):
        # to move the point according to gap
        POINTS_LIST[POINTS_I+gap] = POINTS_LIST[POINTS_I]
        POINTS_LIST[POINTS_I] = 0
        for x in range(POINTS_LIST[POINTS_I-1], POINTS_LIST[POINTS_I+gap]-1, (gap//gap)):
            POINTS_LIST[insideY] = x+1
            if insideY < 799:
                insideY += 1
    else:
        POINTS_LIST[POINTS_I+gap] = POINTS_LIST[POINTS_I]
        POINTS_LIST[POINTS_I] = 0
        for x in range(POINTS_LIST[POINTS_I-1]-1, POINTS_LIST[POINTS_I+gap], -(gap//gap)):
            POINTS_LIST[insideY] = x
            if insideY < 799:
                insideY += 1
    POINTS_I = insideY-1
