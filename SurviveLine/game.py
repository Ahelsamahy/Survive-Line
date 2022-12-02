import sys
import os
import pygame
import pygame.gfxdraw
import neat
import math

from .defs import *

from .ballFunc import *
from .waveFunc import *

# Make a SCREEN to draw on
# SCREEN = pygame.Surface((DISPLAY_W, DISPLAY_H))

songNum = 1

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
# [, pygame.NOFRAME]
# GAME_DISPLAY = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption('Survive line')

localDir = os.path.dirname(__file__)
fontPath = os.path.join(localDir, './usedMaterial/Nexa-Light.otf')


class Game():
    NORMAL_FONT = pygame.font.Font(fontPath, 12)
    BIG_FONT = pygame.font.Font(fontPath, 30)
    SCORE_FONT = pygame.font.Font(fontPath, 35)

    def __init__(self, window, wDisplay, hDisplay):
        self.WDisplay = wDisplay
        self.HDisplay = hDisplay
        self.Wave = Wave(wDisplay, hDisplay)
        self.Ball = Ball(self.Wave.WaveGap, window, self.Wave.PointsList)
        self.window = window

    def updateLabel(self, data, font, x, y, GAME_DISPLAY):
        label = font.render('{}'.format(data), 1, DATA_FONT_COLOR)
        GAME_DISPLAY.blit(label, (x, y))
        return y

    def displayScore(self):
        y_pos = 10
        gap = 30
        x_pos = self.WDisplay//2
        y_pos = self.updateLabel(
            self.Wave.ScoreCount//200, Game.SCORE_FONT, x_pos, y_pos + gap, self.window)

    def collision(self,runLoop):
        ball = self.Ball.drawBall(self.window)
        Wave = self.Wave
        for x in range(240, 255):
            if (Wave.PointsList[x] != 0) and (ball.right >= Wave.PointsList[x]-55-Wave.WaveGap+9):
                print("hit from " + str(x) + " right")
                # return runLoop == False

            if (Wave.PointsList[x] != 0) and ball.left <= Wave.PointsList[x]-338+Wave.WaveGap:
                print("hit from " + str(x) + " left")
                # return runLoop == False

    def draw(self):
        self.window.fill(BACKGROUND_COLOUR)
        self.displayScore()

        self.Wave.draw(self.window)
        self.Wave.generateWave()

        self.Ball.drawBall(self.window)
        self.Ball.generateParticles()

    def moveBall(self, right=True):
        if (right and self.Ball.ballCordX + (Ball.BALL_RADIUS*2) < DISPLAY_W):
            self.Ball.moveBall(right)
            return False
        if (right == False and (self.Ball.ballCordX > 0 + Ball.BALL_RADIUS*2)):
            self.Ball.moveBall(right=False)
            return False
        return True

    def loop(self):
        self.Ball.moveBall()
        self.Wave.ScoreCount += 1
        self.Wave.changeSpeed()
        self.Wave.changeWave()
        if self.Ball.ballCordX < 0:
            self.Ball.reset()
        elif self.Ball.ballCordX > self.WDisplay:
            self.Ball.reset()

    def reset(self):
        self.Ball.reset()
        self.Wave.reset()

