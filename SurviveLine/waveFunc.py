import math
import time
from numpy import random
import numpy as np

# from defs import *
PointsI = 0


class Wave():
    def __init__(self, wDisplay, hDisplay):
        self.WDisplay = wDisplay
        self.HDisplay = hDisplay
        self.ScoreCount = 0  # will come back later for it, in the loop IMPORTANT
        self.waveFreq = 1  # will change later in difficulty part
        self.WaveGap = 0
        self.GameSpeed = 2  # to increment the difference in time to speed the FPS
        self.FPS = 30
        self.WaveAmplitude = 50
        self.PointsI = 0  # index to loop inside the points list
        self.PointsList = [0]*800

    def changeSpeed(self):
        if (self.ScoreCount % (100 * (self.GameSpeed//2)) == 0) and self.FPS < 100:
            self.FPS += 2
            self.GameSpeed *= self.GameSpeed
            print("incremented speed of game")
        return self.FPS, self.GameSpeed

    def changeWave(self):
        if (self.ScoreCount % 30 == 0) and self.WaveGap < 50:
            self.WaveGap += 1
            print("Incremented line gap")
        if (self.ScoreCount % 50 == 0):
            self.WaveAmplitude = random.randint(50, 51+self.WaveGap)
        return self.WaveGap, self.WaveAmplitude

    def generateWave(self):

        if self.PointsI % 800 == 0:
            self.PointsI = 0

        pointsList_XCord = int((self.HDisplay/2) + self.WaveAmplitude*math.sin(
            self.waveFreq * ((float(0)/-self.WDisplay)*(2*math.pi) + (time.time()))))

        # make the dot only to the right half of screen, elif for the left part
        if pointsList_XCord - self.WaveAmplitude - self.WaveGap > self.WDisplay:
            pointsList_XCord = self.WDisplay + 50 + self.WaveGap
        elif pointsList_XCord - 350 - self.WaveGap > self.WDisplay:
            pointsList_XCord = self.WDisplay + 350+self.WaveGap

        # not to generate dot that will overlap the left line
        if (pointsList_XCord < self.WDisplay//2):
            pointsList_XCord = self.WDisplay//2

        self.addPoint(self.PointsI, pointsList_XCord)
        self.checkGap()
        self.PointsI += 1
        return pointsList_XCord, self.PointsI

    def addPoint(self, index, point):
        if self.PointsList[-1] != 0:
            self.PointsList.pop(0)
            self.PointsList.append(point)
        else:
            self.PointsList[index] = point

    def checkGap(self):
        # gapDirection = True  # to right is true, left is false
        if (self.PointsI not in [0, 1, 799]) and (self.PointsList[self.PointsI-1]-self.PointsList[self.PointsI] > 1):
            gap = (self.PointsList[self.PointsI-1] -
                   self.PointsList[self.PointsI]) - 1
            self.fillGap(gap, False)
        elif (self.PointsI not in [0, 1, 799]) and (self.PointsList[self.PointsI] - self.PointsList[self.PointsI-1] > 1):
            gap = (self.PointsList[self.PointsI] -
                   self.PointsList[self.PointsI-1]) - 1
            self.fillGap(gap, True)

    def fillGap(self, gap, gapDirection):
        # gapDirection to right is true, left is false
        if self.PointsI + (gap) >= self.HDisplay-1:
            untilEnd = self.HDisplay-self.PointsI
            toAddFromStart = abs(gap-untilEnd)
            del self.PointsList[:toAddFromStart]
            toAdd = [0]*toAddFromStart
            self.PointsList.extend(toAdd)
            self.PointsI -= toAddFromStart
            gap -= 1
        if gap == 0:
            gap = 1
        insideY = self.PointsI
        if (gapDirection):
            # to move the point according to gap
            self.PointsList[self.PointsI +
                            gap] = self.PointsList[self.PointsI]
            self.PointsList[self.PointsI] = 0
        for x in range(self.PointsList[self.PointsI-1], self.PointsList[self.PointsI+gap]-1, (gap//gap)):
            self.PointsList[insideY] = x+1
            if insideY < 799:
                insideY += 1
        else:
            self.PointsList[self.PointsI +
                            gap] = self.PointsList[self.PointsI]
            self.PointsList[self.PointsI] = 0
        for x in range(self.PointsList[self.PointsI-1]-1, self.PointsList[self.PointsI+gap], -(gap//gap)):
            self.PointsList[insideY] = x
            if insideY < 799:
                insideY += 1
        self.PointsI = insideY-1

    def reset(self):
        self.ScoreCount = 0
        self.WaveGap = 0
        self.GameSpeed = 0
        self.FPS = 60
        self.WaveAmplitude = 50
        self.PointsI = 0
        self.PointsList = [0]*800
