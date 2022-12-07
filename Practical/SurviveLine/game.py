import time
import os
import pygame
import pygame.gfxdraw


from .defs import *

from .ballFunc import *
from .waveFunc import *

songNum = 1

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
# [, pygame.NOFRAME]
# GAME_DISPLAY = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption('Survive line')

localDir = os.path.dirname(__file__)
fontPath = os.path.join(localDir, './usedMaterial/Nexa-Light.otf')


class Game():
    DISPLAY_W = 400
    DISPLAY_H = 800
    NORMAL_FONT = pygame.font.Font(fontPath, 18)
    BIG_FONT = pygame.font.Font(fontPath, 30)
    SCORE_FONT = pygame.font.Font(fontPath, 35)

    def __init__(self, window, wDisplay, hDisplay):
        self.WDisplay = wDisplay
        self.HDisplay = hDisplay
        self.Wave = Wave(wDisplay, hDisplay)
        self.Ball = Ball(self.Wave.WaveGap, window, self.Wave.PointsList)
        self.window = window
        self.startTime = time.time()

    def updateLabel(self, data, font, x, y, GAME_DISPLAY, fontColour=DATA_FONT_COLOR):
        label = font.render('{}'.format(data), True, fontColour)
        GAME_DISPLAY.blit(label, (x, y))

    def displayScore(self):
        yPos = 0
        gap = 30
        xPos = self.WDisplay//2
        self.updateLabel(self.Wave.ScoreCount//200,
                         Game.SCORE_FONT, xPos, yPos + gap, self.window)

    def displayAINum(self, genNum, genomeNum):
        yPos = 0
        gap = 70 
        xPos = self.WDisplay//2
        # if(len(str(genNum)) or len(str(genomeNum))==1):xPos+=5
        if(len(str(genNum))==2 or len(str(genomeNum))==2):xPos-=18
        self.updateLabel("{0}.{1}".format(genNum, genomeNum),Game.NORMAL_FONT, xPos, yPos + gap, self.window)

    def displayRuntime(self):

        y_pos = self.HDisplay-20
        x_pos = self.WDisplay-70
        colour = (100, 100, 100)
        self.updateLabel("{0} S".format(round(
            time.time() - self.startTime, 1)), Game.NORMAL_FONT, x_pos, y_pos, self.window, colour)

    def collision(self, runLoop):
        ball = self.Ball.drawBall(self.window)
        Wave = self.Wave
        for x in range(240, 250):
            if (Wave.PointsList[x] != 0) and (ball.right >= Wave.PointsList[x]-55-Wave.WaveGap+9):
                # print("hit from " + str(x) + " right")
                return runLoop == False

            if (Wave.PointsList[x] != 0) and ball.left <= Wave.PointsList[x]-338+Wave.WaveGap:
                # print("hit from " + str(x) + " left")
                return runLoop == False

    def draw(self):
        """
        Display the score, wave and the particles, make sure the screen will be filled with background
        """
        self.window.fill(BACKGROUND_COLOUR)
        self.displayScore()

        self.Wave.draw(self.window)
        self.Wave.generateWave()

        self.Ball.drawBall(self.window)
        self.Ball.generateParticles()

    def moveBall(self, dir):
        if (dir =="Right" and self.Ball.ballCordX + (Ball.BALL_RADIUS*2) < Game.DISPLAY_W):
            self.Ball.moveBall(right=True)
            return False
        elif (dir =="Left" and (self.Ball.ballCordX > 0 + Ball.BALL_RADIUS*2)):
            self.Ball.moveBall(right=False)
            return False
        elif  dir == "Center":
            return False
        return True

    def loop(self):
        '''
        main functions that needs to be running always
        returns: score counter
        '''
        self.Ball.moveBall()
        self.Wave.ScoreCount += 1
        self.Wave.changeSpeed()
        self.Wave.changeWave()
        if self.Ball.ballCordX < 0:
            self.Ball.reset()
        elif self.Ball.ballCordX > self.WDisplay:
            self.Ball.reset()
        return self.Wave.ScoreCount

    def reset(self):
        self.Ball.reset()
        self.Wave.reset()