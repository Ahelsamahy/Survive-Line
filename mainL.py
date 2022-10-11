from ast import Global
import sys
import os
import math
from pickle import FALSE, TRUE
import pygame
import pygame.gfxdraw
import time
from numpy import random
from defs import *
from itertools import cycle

clock = pygame.time.Clock()
SCREEN = pygame.Surface((DISPLAY_W, DISPLAY_H))

WHITE = (255, 255, 255)
WAVE_COLOUR = (178, 190, 181)
WAVE_GAP = 0
SCORE_COUNTER = 0
DELTA_TIME = 0
GAME_TIME = 0
GAME_COUNTER = 0
GAME_SPEED = 2
# [loc, velocity, timer]
PARTICLES = []
songNum = 1

WAVE_AMPLITUDE = 50
WAVE_FREQUENCY = 1
WAVE_SPEED = 1
WAVE_CORD_X = 0
POINTS_LIST = []
keepGenerating = TRUE

BALL_CORD_Y = 550
BALL_CORD_X = DISPLAY_W//2
BALL_MOVE_SPEED = 5
BALL_RADIUS = 12

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
# Make a window to show on [, pygame.NOFRAME]
GAME_DISPLAY = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption('Survive line')


NORMAL_FONT = pygame.font.Font("./usedMaterial/Nexa-Light.otf", 12)
BIG_FONT = pygame.font.Font("./usedMaterial/Nexa-Light.otf", 30)
SCORE_FONT = pygame.font.Font("./usedMaterial/Nexa-Light.otf", 35)


def update_label(data, font, x, y, GAME_DISPLAY):
    label = font.render('{}'.format(data), 1, DATA_FONT_COLOR)
    GAME_DISPLAY.blit(label, (x, y))
    return y


def update_data_labels(GAME_DISPLAY, font):
    y_pos = 10
    gap = 30
    x_pos = DISPLAY_W//2
    y_pos = update_label(SCORE_COUNTER//200, font,
                         x_pos, y_pos + gap, GAME_DISPLAY)


def generateWave():
    global WAVE_CORD_X, SCORE_COUNTER
    # checkGap()
    if len(POINTS_LIST) == DISPLAY_H-1:
        POINTS_LIST.pop(0)

    WAVE_CORD_X = int((DISPLAY_H/2) + WAVE_AMPLITUDE*math.sin(WAVE_FREQUENCY *
                      ((float(0)/-DISPLAY_W)*(2*math.pi) + (WAVE_SPEED*time.time()))))

    POINTS_LIST.append(WAVE_CORD_X)


def changeSpeed():
    global FPS, WAVE_GAP, GAME_SPEED
    if(SCORE_COUNTER % (100 * (GAME_SPEED//2)) == 0) and FPS < 60:
        FPS += 2
        GAME_SPEED *= GAME_SPEED
        print("incremented speed of game")


def collision():
    global keepGenerating
    ball = pygame.Rect(BALL_CORD_X, BALL_CORD_Y, BALL_RADIUS, BALL_RADIUS)
    for x in range(245, 255):
        if ball.right >= POINTS_LIST[x]-55:
            print("hit from " + str(x))
            keepGenerating = FALSE

        if ball.left <= POINTS_LIST[x]-340:
            print("hit from " + str(x))
            keepGenerating = FALSE


def debug(SCORE_COUNTER):
    print(SCORE_COUNTER)


def drawCircle(SCREEN, x, y, radius, color):
    pygame.gfxdraw.aacircle(SCREEN, x, y, radius, color)
    pygame.gfxdraw.filled_circle(SCREEN, x, y, radius, color)


def moveCircle():
    global BALL_CORD_X
    PRESSED_KEYS = pygame.key.get_pressed()
    if PRESSED_KEYS[pygame.K_RIGHT] and BALL_CORD_X + (BALL_RADIUS) < DISPLAY_W-4:
        BALL_CORD_X += BALL_MOVE_SPEED
    if PRESSED_KEYS[pygame.K_LEFT] and BALL_CORD_X > 0 + BALL_RADIUS+4:
        BALL_CORD_X -= BALL_MOVE_SPEED


def reset():
    global BALL_CORD_Y, BALL_CORD_X, POINTS_LIST, keepGenerating, PARTICLES
    BALL_CORD_Y = 550
    BALL_CORD_X = DISPLAY_W//2
    POINTS_LIST.clear()
    keepGenerating = TRUE
    PARTICLES.clear()


def gameOver():

    pygame.init()

    while TRUE:
        SCREEN.fill(background_color)
        windowX, windowY = 300, 200
        startBorderX, startBorderY = (
            DISPLAY_W-windowX)//2, (DISPLAY_H-windowY)//2
        # pygame.draw.rect(SCREEN, "white", pygame.Rect(
        #     startBorderX, startBorderY, windowX, windowY),  2)
        update_label("SCORE", BIG_FONT,
                     windowX//2, DISPLAY_H//2 - startBorderY//4, GAME_DISPLAY)
        keepCenter = (len(str((abs(round(SCORE_COUNTER//300))))))
        update_label(round(SCORE_COUNTER//200), SCORE_FONT,
                     DISPLAY_W//2-8 * keepCenter - keepCenter*0.3, DISPLAY_H//2 - startBorderY//8, GAME_DISPLAY)
        update_label("press anykey to play again", NORMAL_FONT,
                     DISPLAY_W//2 - 75, DISPLAY_H//2 + startBorderY//3, GAME_DISPLAY)
        pygame.display.update()

        GAME_DISPLAY.blit(SCREEN, (0, 0))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_ESCAPE):
                    print("ESC key is pressed, will stop now\n")
                    pygame.quit()
                    sys.exit()
                else:
                    reset()
                    run_game()


def ballParticles():
    # [loc, velocity, timer]
    PARTICLES.append([[BALL_CORD_X, BALL_CORD_Y], [
                     random.randint(0, 20) / 10 - 1, -3], random.randint(4, 6)])

    for particle in PARTICLES:
        particle[0][0] -= particle[1][0]
        particle[0][1] -= particle[1][1]
        particle[2] -= 0.1

        pygame.draw.circle(GAME_DISPLAY, (255, 255, 255), [int(
            particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            PARTICLES.remove(particle)


def backgroundMusic():
    directory = "./usedMaterial/Music/"
    playList = {}

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"):
            playList[os.path.join(directory, filename)] = filename[:-4]
            continue
        else:
            continue

    backgroundMusicDir = (list(playList.keys())[songNum])[1:]
    pygame.mixer.music.load(os.path.abspath(os.getcwd())+backgroundMusicDir)


def optionsMenu():

    pygame.init()

    while TRUE:
        SCREEN.fill(background_color)
        windowX, windowY = 300, 200
        startBorderX, startBorderY = DISPLAY_W//2-windowX//2, DISPLAY_H//2-windowY//2
        pygame.draw.rect(SCREEN, "white", pygame.Rect(
            startBorderX, startBorderY, windowX, windowY),  2)
        update_label("I don't own the copyright for the songs", NORMAL_FONT,
                     startBorderX+windowX//10, startBorderY+windowY-30, GAME_DISPLAY)
        pygame.display.update()

        GAME_DISPLAY.blit(SCREEN, (0, 0))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_ESCAPE):
                    print("ESC key is pressed, will stop now\n")
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:

                    run_game()


def run_game():
    # Make a SCREEN to draw on
    pygame.mixer.music.play(-1, 0.0)
    running = True
    while running:
        DELTA_TIME = clock.tick(FPS)
        # GAME_TIME += DELTA_TIME
        SCREEN.fill(background_color)

        global SCORE_COUNTER, GAME_COUNTER, BALL_CORD_X, BALL_CORD_Y, songNum
        SCORE_COUNTER += 1

        if len(POINTS_LIST) > 260:
            collision()

        # debug(SCORE_COUNTER)

        # changeSpeed()
        # changeWave()
        if keepGenerating == TRUE:
            generateWave()
        else:
            gameOver()

        color = WAVE_COLOUR
        # so i want to reach a fixed point in the screen that will be the collision area.

        for Y_CORD in range(len(POINTS_LIST)):

            pygame.gfxdraw.pixel(
                GAME_DISPLAY, POINTS_LIST[Y_CORD]-55-WAVE_GAP, DISPLAY_H-Y_CORD, WAVE_COLOUR)
            pygame.gfxdraw.pixel(
                GAME_DISPLAY, POINTS_LIST[Y_CORD]-350-WAVE_GAP, DISPLAY_H-Y_CORD, WAVE_COLOUR)

        ballParticles()

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_ESCAPE):
                    print("ESC key is pressed, will stop now\n")
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_o:
                    optionsMenu()
                elif(event.key == pygame.K_n):
                    print("Next Song")
                    songNum += 1

        moveCircle()
        drawCircle(GAME_DISPLAY, BALL_CORD_X, BALL_CORD_Y, BALL_RADIUS, WHITE)

        pygame.display.flip()

        GAME_DISPLAY.blit(SCREEN, (0, 0))

        # update_data_labels(GAME_DISPLAY, SCORE_FONT)


if __name__ == "__main__":
    backgroundMusic()
    run_game()
