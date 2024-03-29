from numpy import random
from .defs import *
import pygame


class Ball(object):
    BALL_MOVE_SPEED = 2
    BALL_RADIUS = 12
    BALL_CORD_Y = 550  # fixed as the ball doesn't go up or down
    BALL_CORD_X = 0  # changes as the ball moves on this axes

    def __init__(self, waveGap, gameDisplay, pointsList):
        self.ballCordX = 400 // 2
        self.ballCordY = Ball.BALL_CORD_Y
        self.WaveGap = waveGap
        self.Particles = []
        self.GameDisplay = gameDisplay
        self.PointsList = pointsList

    def drawBall(self, SCREEN, drawRect):
        if drawRect:
            ballRect = self.ballRect()
            pygame.draw.rect(SCREEN, (125, 125, 125), ballRect)
        pygame.gfxdraw.aacircle(
            SCREEN, self.ballCordX, self.ballCordY, Ball.BALL_RADIUS, WHITE
        )
        pygame.gfxdraw.filled_circle(
            SCREEN, self.ballCordX, self.ballCordY, Ball.BALL_RADIUS, WHITE
        )

    def ballRect(self):
        ballRect = pygame.Rect(
            self.ballCordX - Ball.BALL_RADIUS,
            self.ballCordY - Ball.BALL_RADIUS,
            Ball.BALL_RADIUS * 2,
            Ball.BALL_RADIUS * 2,
        )
        return ballRect

    def moveBall(self, right=None):
        # if moveBall = true then move to right
        if right == True:
            self.ballCordX += Ball.BALL_MOVE_SPEED
        elif right == False:
            self.ballCordX -= Ball.BALL_MOVE_SPEED

    def generateParticles(self):
        Loc = [self.ballCordX, self.ballCordY]
        Vel = [random.randint(0, 20) / 10 - 1, -3]
        Timer = random.randint(4, 6)
        self.Particles.append([Loc, Vel, Timer])
        for particle in self.Particles:
            particle[0][0] -= particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1

            pygame.draw.circle(
                self.GameDisplay,
                (255, 255, 255),
                [int(particle[0][0]), int(particle[0][1])],
                int(particle[2]),
            )
            if particle[2] <= 0:
                self.Particles.remove(particle)

    def reset(self):
        self.ballCordY = Ball.BALL_CORD_Y
        self.ballCordX = 400 // 2
        self.Particles = []
