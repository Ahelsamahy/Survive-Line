import time
import os
import pygame
import pygame.gfxdraw
import numpy


from .defs import *

from .ballFunc import *
from .waveFunc import *

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.display.set_caption('Survive line')




class Game():
    localDir = os.path.dirname(__file__)
    fontPath = os.path.join(localDir, './usedMaterial/Nexa-Light.otf')
    NORMAL_FONT = pygame.font.Font(fontPath, 18)
    BIG_FONT = pygame.font.Font(fontPath, 30)
    SCORE_FONT = pygame.font.Font(fontPath, 35)

    def __init__(self, window, wDisplay, hDisplay):
        self.WDisplay = wDisplay
        self.HDisplay = hDisplay
        self.window = window
        self.Wave = Wave(wDisplay, hDisplay)
        self.Ball = Ball(self.Wave.WaveGap, window, self.Wave.PointsList)
        self.startTime = time.time()
        self.showedLines = []
        self.runTime = 0

    def updateLabel(self, data, font, x, y, GAME_DISPLAY, fontColour=DATA_FONT_COLOR):
        label = font.render('{}'.format(data), True, fontColour)
        GAME_DISPLAY.blit(label, (x, y))

    def displayScore(self):
        yPos = 0
        gap = 30
        xPos = self.WDisplay//2
        self.updateLabel(self.Wave.ScoreCount//200,Game.SCORE_FONT, xPos, yPos + gap, self.window)

    def displayAINum(self, genNum, genomeNum):
        yPos = 0
        gap = 70
        xPos = self.WDisplay//2
        # if(len(str(genNum)) or len(str(genomeNum))==1):xPos+=5
        if(len(str(genNum)) == 2 or len(str(genomeNum)) == 2):
            xPos -= 18
        self.updateLabel("{0}.{1}".format(genNum, genomeNum),Game.NORMAL_FONT, xPos, yPos + gap, self.window)

    def displayRuntime(self):
        y_pos = self.HDisplay-20
        x_pos = self.WDisplay-70
        colour = (100, 100, 100)
        self.runTime = round(time.time() - self.startTime)
        self.updateLabel("{0} S".format(self.runTime, 1), Game.NORMAL_FONT, x_pos, y_pos, self.window, colour)

    def collision(self, runLoop):
        ball = self.Ball.ballRect()
        Wave = self.Wave
        #                              226          ,             250
        for YCord in range(self.HDisplay-ball.bottom, self.HDisplay-ball.top):
            if (Wave.PointsList[YCord] != 0) and (ball.right >= Wave.PointsList[YCord]-50-Wave.WaveGap):
                return runLoop == False

            if (Wave.PointsList[YCord] != 0) and ball.left <= Wave.PointsList[YCord]-350+Wave.WaveGap:
                return runLoop == False

    def moveBall(self, dir):
        if (dir == "Right" and self.Ball.ballCordX + (Ball.BALL_RADIUS*2) < self.WDisplay):
            self.Ball.moveBall(right=True)
            return False
        elif (dir == "Left" and (self.Ball.ballCordX > 0 + Ball.BALL_RADIUS*2)):
            self.Ball.moveBall(right=False)
            return False
        elif dir == "Center":
            return False
        return True

    def notificationMusic(self):
        directory = os.path.join(Game.localDir,"./usedMaterial/Music/")
        backgroundMusicDir = "yoBaby.mp3"
        pygame.mixer.music.load(directory+backgroundMusicDir)
        pygame.mixer.music.play()

    def countDistance(self):
        """
        make a list for distance between the bottom edge of ballRect to the corresponding point on the wave 
        with the same x-axis, then one step up on wave and repeat, and make another loop to do the same with the ballRect
        """
        ball = self.Ball.ballRect()
        Wave = self.Wave
        rightList = []
        leftList = []
        self.showedLines.clear()
        # the starting point here is the bottom of ball and the end is the top + 20 px for prediction
        # increased the step size because there was lag for the whole process to be handled
        for YCord in range(self.HDisplay-ball.bottom, self.HDisplay-ball.top+20, 5):
            for YBall in range(0, ball.width, 5):
                dxR = pow(Wave.PointsList[YCord] - 50 - Wave.WaveGap - ball.bottomright[0] + YBall, 2)
                dxL = pow(Wave.PointsList[YCord] - 350 + Wave.WaveGap - ball.bottomleft[0] + YBall, 2)
                dy = pow(abs((800-YCord) - ball.bottomright[1]+YBall), 2)

                rightList.append(int(math.sqrt(dxR+dy)))
                leftList.append(int(math.sqrt(dxL+dy)))
                self.showedLines.append(YCord)
        return rightList, leftList

    def showVision(self):
        '''
        show the lines that are detected by the ball to the wave
        '''
        # PS: it is just visually, the actually line start from the bottom edge of the
        # ballRect to each point in the wave range, then go one up the ball rect and repeat the same step
        ball = self.Ball.ballRect()
        lineToWaveColour = (219, 199, 184)
        for disLine in range(len(self.showedLines)):
            xCord = self.showedLines[disLine]
            if(self.Wave.PointsList[xCord] != 0):
                pygame.draw.line(self.Ball.GameDisplay, lineToWaveColour, (ball.centerx, ball.centery),
                                 (self.Wave.PointsList[xCord]-50-self.Wave.WaveGap, 800-xCord), 2)
                pygame.draw.line(self.Ball.GameDisplay, lineToWaveColour, (ball.centerx, ball.centery),
                                 (self.Wave.PointsList[xCord]-350+self.Wave.WaveGap, 800-xCord), 2)

    def draw(self, vision, particles, drawBallRec):
        """
        Display the score, wave and the particles, make sure the screen will be filled with background
        """
        self.window.fill(BACKGROUND_COLOUR)
        self.displayScore()

        self.Wave.draw(self.window)
        self.Wave.generateWave()

        self.countDistance()

        if vision:
            self.showVision()
        if particles:
            self.Ball.generateParticles()
        self.Ball.drawBall(self.window , drawBallRec)
        self.Ball.moveBall()

    def loop(self):
        '''
        main functions that needs to be running always
        returns: score counter
        '''

        self.Wave.ScoreCount += 1
        self.Wave.changeSpeed()
        self.Wave.changeWave()
        return self.Wave.ScoreCount

    def reset(self):
        self.Ball.reset()
        self.Wave.reset()
