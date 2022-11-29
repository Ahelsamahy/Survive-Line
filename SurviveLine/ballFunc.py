from numpy import random
from .defs import *

import pygame


class Ball(object):
    PARTICLES = []
    BALL_MOVE_SPEED = 5
    BALL_RADIUS = 12

    def __init__(self, waveGap, loc, vel, timer, gameDisplay, X_POS):
        self.ballCordY = 550  # fixed as the ball doesn't go up or down
        self.ballCordX = X_POS  # changes as the ball moves on this axes
        self.moveSpeed = 5
        self.radius = 12
        self.WaveGap = waveGap
        self.Loc = loc
        self.Vel = vel
        self.Timer = timer
        self.GameDisplay = gameDisplay
        self.rect = pygame.Rect(
            self.X_POS, self.ballCordY, self.radius*2, self.radius*2)

    def drawBall(self, SCREEN):
        pygame.gfxdraw.aacircle(SCREEN, self.rect.x,BALL_CORD_Y, self.radius*2, WHITE)
        pygame.gfxdraw.filled_circle(SCREEN, self.rect.x, BALL_CORD_Y, self.radius*2, WHITE)

    def moveBall(self, right=True):
        # if moveBall= true then move to right
        if right == True:
            self.ballCordX += self.moveSpeed
        else:
            self.ballCordX -= self.moveSpeed

    def reset(self):
        self.ballCordY = 550
        self.ballCordX = DISPLAY_W//2

    def collision(self, ball):
        global keepGenerating
        ball = pygame.Rect(self.ballCordX, self.ballCordY,
                           self.radius*2, self.radius*2)
        for x in range(245, 255):
            if (POINTS_LIST[x] != 0) and (ball.right >= POINTS_LIST[x]-55-self.WaveGap):
                print("hit from " + str(x) + " right")
                return keepGenerating == False

            if (POINTS_LIST[x] != 0) and ball.left <= POINTS_LIST[x]-338+self.WaveGap:
                print("hit from " + str(x) + " left")
                return keepGenerating == False

    def generateParticles(self):
        PARTICLES.append([self.Loc, self.Vel, self.Timer])
        for particle in PARTICLES:
            particle[0][0] -= particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1

            pygame.draw.circle(self.GameDisplay, (255, 255, 255), [int(
                particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                PARTICLES.remove(particle)

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
