import math
import time
from numpy import random
import numpy as np

# from defs import *
POINTS_I = 0


class Wave():
    WAVE_AMPLITUDE = 50
    WAVE_FREQUENCY = 1
    WAVE_SPEED = 1
    def __init__(self, counter, waveGap, gameSpeed, fps, waveAmplitude, xCord, points, pointslist):
        self.Counter = counter
        self.WaveGap = waveGap
        self.GameSpeed = gameSpeed
        self.FPS = fps
        self.WaveAmplitude = waveAmplitude
        self.points_i = points
        self.pointsList = pointslist
        self.XCord = xCord
        self.pointsList = [0]*800

    def reset(self):
        self.Counter = 0
        self.WaveGap = 0
        self.GameSpeed = 0
        self.FPS = 60
        self.WaveAmplitude = 50
        self.points_i = 0
        self.pointsList = [0]*800
        self.XCord = 0

    class changeDifficulty(object):

        def changeSpeed(self):
            if (self.Counter % (100 * (self.GameSpeed//2)) == 0) and self.FPS < 100:
                self.FPS += 2
                self.GameSpeed *= self.GameSpeed
                print("incremented speed of game")
            return self.FPS, self.GameSpeed

        def changeWave(self):
            if (self.Counter % 30 == 0) and self.WaveGap < 50:
                self.WaveGap += 1
                print("Incremented line gap")
            if (self.Counter % 50 == 0):
                self.WaveAmplitude = random.randint(50, 51+self.WaveGap)
            return self.WaveGap, self.WaveAmplitude

    class generatePlusFilling(object):
        def generateWave(self):
            global SCORE_COUNTER
            if self.points_i % 800 == 0:
                self.points_i = 0

            self.XCord = int((DISPLAY_H/2) + self.WaveAmplitude*math.sin(
                WAVE_FREQUENCY * ((float(0)/-DISPLAY_W)*(2*math.pi) + (WAVE_SPEED*time.time()))))

            # make the dot only to the right half of screen, elif for the left part
            if self.XCord-self.WaveAmplitude-WAVE_GAP > DISPLAY_W:
                self.XCord = DISPLAY_W+50+WAVE_GAP
            elif self.XCord-350-WAVE_GAP > DISPLAY_W:
                self.XCord = DISPLAY_W+350+WAVE_GAP

            # not to generate dot that will overlap the left line
            if (self.XCord < DISPLAY_W//2):
                self.XCord = DISPLAY_W//2

            self.addPoint(self.points_i, self.XCord)
            self.checkGap()
            self.points_i += 1
            return self.XCord, self.points_i

        def addPoint(self, index, point):
            if self.pointsList[-1] != 0:
                self.pointsList.pop(0)
                self.pointsList.append(point)
            else:
                self.pointsList[index] = point

        def checkGap(self):
            # gapDirection = True  # to right is true, left is false
            if (self.points_i not in [0, 1, 799]) and (self.pointsList[self.points_i-1]-self.pointsList[self.points_i] > 1):
                gap = (self.pointsList[self.points_i-1] -
                       self.pointsList[self.points_i]) - 1
                self.fillGap(gap, False)
            elif (self.points_i not in [0, 1, 799]) and (self.pointsList[self.points_i] - self.pointsList[self.points_i-1] > 1):
                gap = (self.pointsList[self.points_i] -
                       self.pointsList[self.points_i-1]) - 1
                self.fillGap(gap, True)

        def fillGap(self, gap, gapDirection):
            # gapDirection to right is true, left is false
            if self.points_i + (gap) >= DISPLAY_H-1:
                untilEnd = DISPLAY_H-self.points_i
                toAddFromStart = abs(gap-untilEnd)
                del self.pointsList[:toAddFromStart]
                toAdd = [0]*toAddFromStart
                self.pointsList.extend(toAdd)
                self.points_i -= toAddFromStart
                gap -= 1
            if gap == 0:
                gap = 1
            insideY = self.points_i
            if (gapDirection):
                # to move the point according to gap
                self.pointsList[self.points_i +
                                gap] = self.pointsList[self.points_i]
                self.pointsList[self.points_i] = 0
            for x in range(self.pointsList[self.points_i-1], self.pointsList[self.points_i+gap]-1, (gap//gap)):
                self.pointsList[insideY] = x+1
                if insideY < 799:
                    insideY += 1
            else:
                self.pointsList[self.points_i +
                                gap] = self.pointsList[self.points_i]
                self.pointsList[self.points_i] = 0
            for x in range(self.pointsList[self.points_i-1]-1, self.pointsList[self.points_i+gap], -(gap//gap)):
                self.pointsList[insideY] = x
                if insideY < 799:
                    insideY += 1
            self.points_i = insideY-1
