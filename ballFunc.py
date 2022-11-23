from numpy import random
from defs import *

import pygame



PARTICLES = []
BALL_CORD_Y = 550
BALL_CORD_X = DISPLAY_W//2
BALL_MOVE_SPEED = 5
BALL_RADIUS = 12

class Ball(object):
    def __init__(self, waveGap,loc, vel, timer,gameDisplay):
        self.WaveGap = waveGap
        self.Loc = loc
        self.Vel = vel
        self.Timer = timer
        self.GameDisplay = gameDisplay

    def collision(self,ball):
        global keepGenerating
        ball = pygame.Rect(BALL_CORD_X, BALL_CORD_Y, BALL_RADIUS, BALL_RADIUS)
        for x in range(245, 255):
            if (POINTS_LIST[x] != 0) and (ball.right >= POINTS_LIST[x]-55-self.WaveGap):
                print("hit from " + str(x) + " right")
                return keepGenerating == False

            if (POINTS_LIST[x] != 0) and ball.left <= POINTS_LIST[x]-338+self.WaveGap:
                print("hit from " + str(x) + " left")
                return keepGenerating == False

    def drawCircle(self,SCREEN, x, y, radius, color):
        pygame.gfxdraw.aacircle(SCREEN, x, y, radius, color)
        pygame.gfxdraw.filled_circle(SCREEN, x, y, radius, color)

    def moveCircle(self,moveBall):
        # if moveBall= true then move to right
        global BALL_CORD_X

        if moveBall==True and BALL_CORD_X + (BALL_RADIUS) < DISPLAY_W-4:
            BALL_CORD_X += BALL_MOVE_SPEED
        if (moveBall==False) and BALL_CORD_X > 0 + BALL_RADIUS+4:
            BALL_CORD_X -= BALL_MOVE_SPEED
        return BALL_CORD_X

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


def reset():
    global BALL_CORD_Y, BALL_CORD_X, POINTS_LIST, keepGenerating, PARTICLES, SCORE_COUNTER, WAVE_GAP, POINTS_I
    BALL_CORD_Y = 550
    BALL_CORD_X = DISPLAY_W//2
    POINTS_LIST = [0]*800
    POINTS_I = 0
    keepGenerating = True
    PARTICLES.clear()
    SCORE_COUNTER == 0
    WAVE_GAP == 0
    return WAVE_GAP, SCORE_COUNTER, POINTS_LIST,POINTS_I
