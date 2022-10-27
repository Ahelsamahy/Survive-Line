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
    if (Counter % 30 == 0) and waveGap < 50:
        waveGap += 1
        print("Incremented line gap")
    if (Counter % 50 == 0):
        WAVE_AMPLITUDE = random.randint(50, 51+waveGap)
    return waveGap, WAVE_AMPLITUDE


class generatePlusFilling(object):

    def __init__(self, points):
        self.points_i = points

    def generateWave(self):
        global WAVE_CORD_X, SCORE_COUNTER,points_i

        if self.points_i % 800 == 0:
            self.points_i = 0

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

        self.addPoint(self.points_i, WAVE_CORD_X)
        self.checkGap()
        self.points_i += 1

    def addPoint(self, index, point):
        if POINTS_LIST[-1] != 0:
            POINTS_LIST.pop(0)
            POINTS_LIST.append(point)
        else:
            POINTS_LIST[index] = point

    def checkGap(self):
        # gapDirection = True  # to right is true, left is false
        if (self.points_i not in [0, 1, 799]) and (POINTS_LIST[self.points_i-1]-POINTS_LIST[self.points_i] > 1):
            gap = (POINTS_LIST[self.points_i-1] - POINTS_LIST[self.points_i]) - 1
            self.fillGap(gap, False)
        elif (self.points_i not in [0, 1, 799]) and (POINTS_LIST[self.points_i] - POINTS_LIST[self.points_i-1] > 1):
            gap = (POINTS_LIST[self.points_i] - POINTS_LIST[self.points_i-1]) - 1
            self.fillGap(gap, True)

    def fillGap(self, gap, gapDirection):
        # gapDirection to right is true, left is false
        global  POINTS_LIST
        if self.points_i + (gap) >= DISPLAY_H-1:
            untilEnd = DISPLAY_H-self.points_i
            toAddFromStart = abs(gap-untilEnd)
            del POINTS_LIST[:toAddFromStart]
            toAdd = [0]*toAddFromStart
            POINTS_LIST.extend(toAdd)
            self.points_i -= toAddFromStart
            gap -= 1
        if gap == 0:
            gap = 1
        insideY = self.points_i
        if(gapDirection):
            # to move the point according to gap
            POINTS_LIST[self.points_i+gap] = POINTS_LIST[self.points_i]
            POINTS_LIST[self.points_i] = 0
            for x in range(POINTS_LIST[self.points_i-1], POINTS_LIST[self.points_i+gap]-1, (gap//gap)):
                POINTS_LIST[insideY] = x+1
                if insideY < 799:
                    insideY += 1
        else:
            POINTS_LIST[self.points_i+gap] = POINTS_LIST[self.points_i]
            POINTS_LIST[self.points_i] = 0
            for x in range(POINTS_LIST[self.points_i-1]-1, POINTS_LIST[self.points_i+gap], -(gap//gap)):
                POINTS_LIST[insideY] = x
                if insideY < 799:
                    insideY += 1
        self.points_i = insideY-1
