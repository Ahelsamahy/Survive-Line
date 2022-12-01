from numpy import random
from .defs import *

import pygame


class Ball(object):
    BALL_MOVE_SPEED = 5
    BALL_RADIUS = 12
    BALL_CORD_Y = 550       # fixed as the ball doesn't go up or down
    BALL_CORD_X = 0         # changes as the ball moves on this axes

    def __init__(self, waveGap, gameDisplay, X_POS, pointsList):
        self.ballCordX = X_POS
        self.ballCordY = 550
        self.WaveGap = waveGap

        self.Particles = []
        self.GameDisplay = gameDisplay
        self.PointsList = pointsList

    def drawBall(self, SCREEN):
        pygame.Rect(self.X_POS, self.ballCordY, self.radius*2, self.radius*2)
        pygame.gfxdraw.aacircle(SCREEN, self.ballCordX,
                                self.ballCordY, self.radius*2, WHITE)
        pygame.gfxdraw.filled_circle(
            SCREEN, self.ballCordX, self.ballCordY, self.radius*2, WHITE)

    def moveBall(self, right=True):
        # if moveBall= true then move to right
        if right == True:
            self.ballCordX += self.moveSpeed
        else:
            self.ballCordX -= self.moveSpeed

    def collision(self, ball):
        global keepGenerating
        ball = pygame.Rect(self.ballCordX, self.ballCordY,
                           Ball.BALL_RADIUS*2, Ball.BALL_RADIUS*2)
        for x in range(245, 255):
            if (self.PointsList[x] != 0) and (ball.right >= self.PointsList[x]-55-self.WaveGap):
                print("hit from " + str(x) + " right")
                return keepGenerating == False

            if (self.PointsList[x] != 0) and ball.left <= self.PointsList[x]-338+self.WaveGap:
                print("hit from " + str(x) + " left")
                return keepGenerating == False

    def generateParticles(self):
        Loc =[self.ballCordX, self.ballCordY] 
        Vel = [random.randint(0, 20) / 10 - 1, -3]
        Timer = random.randint(4, 6)
        self.Particles.append([Loc, Vel, Timer])
        for particle in self.Particles:
            particle[0][0] -= particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1

            pygame.draw.circle(self.GameDisplay, (255, 255, 255), [int(
                particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.Particles.remove(particle)

    def reset(self):
        self.ballCordY = 550
        self.ballCordX = DISPLAY_W//2
        self.Particles = []

# def reset():
#     global BALL_CORD_Y, BALL_CORD_X, POINTS_LIST, keepGenerating, PARTICLES, SCORE_COUNTER, WAVE_GAP, POINTS_I
#     BALL_CORD_Y = 550
#     BALL_CORD_X = DISPLAY_W//2
#     POINTS_LIST = [0]*800
#     POINTS_I = 0
#     keepGenerating = True
#     PARTICLES.clear()
#     SCORE_COUNTER = 0
#     WAVE_GAP = 0
#     return WAVE_GAP, SCORE_COUNTER, POINTS_LIST, POINTS_I
