import sys
import os
import math
from pickle import TRUE
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
songNum=1

WAVE_AMPLITUDE = 50
WAVE_FREQUENCY = 1
WAVE_SPEED = 1
WAVE_CORD_Y = 0
WAVE_CORD_X = 0
POINTS_MATRIX = [[0 for x in range(2)] for y in range(DISPLAY_H)]
posX = cycle(range(2))

BALL_CORD_Y = 550
BALL_CORD_X = DISPLAY_W//2
BALL_MOVE_SPEED = 5
BALL_RADIUS = 12

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
# Make a window to show on [, pygame.NOFRAME]
GAME_DISPLAY = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption('Survive line')

SCORE_FONT = pygame.font.Font("./usedMaterial/Nexa-Light.otf", DATA_FONT_SIZE)
NORMAL_FONT = pygame.font.Font("./usedMaterial/Nexa-Light.otf", 12)


def update_label(data, font, x, y, GAME_DISPLAY):
    label = font.render('{}'.format(data), 1, DATA_FONT_COLOR)
    GAME_DISPLAY.blit(label, (x, y))
    return y


def update_data_labels(GAME_DISPLAY, font):
    y_pos = 10
    gap = 30
    x_pos = DISPLAY_W//2
    y_pos = update_label(round(SCORE_COUNTER/100), font,
                         x_pos, y_pos + gap, GAME_DISPLAY)


def fillGap(gap, gapDirection):
    # gapDirection to right is true, left is false
    global WAVE_CORD_Y
    if WAVE_CORD_Y % 799 == 0:
        WAVE_CORD_Y = 1
    if WAVE_CORD_Y + (gap) > DISPLAY_H-1:
        gap = DISPLAY_H - WAVE_CORD_Y - 1
    if gap == 0:
        gap = 1
    insideY = WAVE_CORD_Y

    if(gapDirection):
        POINTS_MATRIX[WAVE_CORD_Y + (gap)][0] = POINTS_MATRIX[WAVE_CORD_Y][0]
        POINTS_MATRIX[WAVE_CORD_Y + (gap)][1] = POINTS_MATRIX[WAVE_CORD_Y][1]
        POINTS_MATRIX[WAVE_CORD_Y][0] = POINTS_MATRIX[WAVE_CORD_Y][1] = 0
        # print(POINTS_MATRIX[WAVE_CORD_Y-1][0],
        #   POINTS_MATRIX[WAVE_CORD_Y+gap][0])
        for x in range(POINTS_MATRIX[WAVE_CORD_Y-1][0]+1, POINTS_MATRIX[WAVE_CORD_Y+gap][0], (gap//gap)):
            POINTS_MATRIX[insideY][next(posX)] = x
            POINTS_MATRIX[insideY][next(posX)] = -SCORE_COUNTER+1
            if insideY < 799:
                insideY += 1
    else:
        POINTS_MATRIX[WAVE_CORD_Y + (gap)][0] = POINTS_MATRIX[WAVE_CORD_Y][0]
        POINTS_MATRIX[WAVE_CORD_Y + (gap)][1] = POINTS_MATRIX[WAVE_CORD_Y][1]
        POINTS_MATRIX[WAVE_CORD_Y][0] = POINTS_MATRIX[WAVE_CORD_Y][1] = 0
        # print(POINTS_MATRIX[WAVE_CORD_Y-1][0],
        #       POINTS_MATRIX[WAVE_CORD_Y+gap][0])
        for x in range(POINTS_MATRIX[WAVE_CORD_Y-1][0]-1, POINTS_MATRIX[WAVE_CORD_Y+gap][0], -(gap//gap)):
            POINTS_MATRIX[insideY][next(posX)] = x
            POINTS_MATRIX[insideY][next(posX)] = -SCORE_COUNTER
            if insideY < 799:
                insideY += 1
    # print("Moved a point")


def checkGap():
    # gapDirection = True  # to right is true, left is false
    if (POINTS_MATRIX[WAVE_CORD_Y-1][0]-POINTS_MATRIX[WAVE_CORD_Y][0] > 1):
        gap = (POINTS_MATRIX[WAVE_CORD_Y-1][0]-POINTS_MATRIX[WAVE_CORD_Y][0])-1
        fillGap(gap, False)
    elif(POINTS_MATRIX[WAVE_CORD_Y][0] - POINTS_MATRIX[WAVE_CORD_Y-1][0] > 1) and (WAVE_CORD_Y not in {1, 2, 3}):
        gap = (POINTS_MATRIX[WAVE_CORD_Y][0] -
               POINTS_MATRIX[WAVE_CORD_Y-1][0]) - 1
        fillGap(gap, True)


def generateWave():
    global WAVE_CORD_Y, WAVE_CORD_X, SCORE_COUNTER
    checkGap()
    if WAVE_CORD_Y < DISPLAY_H-1:
        WAVE_CORD_Y += 1
    else:
        WAVE_CORD_Y = 0

    WAVE_CORD_X = int((DISPLAY_H/2) + WAVE_AMPLITUDE*math.sin(WAVE_FREQUENCY *
                      ((float(WAVE_CORD_Y)/-DISPLAY_W)*(2*math.pi) + (WAVE_SPEED*time.time()))))
    #make the dot only to the right half of screen, elif for the left part
    if WAVE_CORD_X-WAVE_AMPLITUDE-WAVE_GAP > DISPLAY_W:
        WAVE_CORD_X = DISPLAY_W+50+WAVE_GAP
    elif WAVE_CORD_X-350-WAVE_GAP > DISPLAY_W:
        WAVE_CORD_X = DISPLAY_W+350+WAVE_GAP

    #not to generate dot that will overlap the left line
    if (WAVE_CORD_X < DISPLAY_W//2):
        WAVE_CORD_X = DISPLAY_W//2

    POINTS_MATRIX[WAVE_CORD_Y][next(posX)] = WAVE_CORD_X
    POINTS_MATRIX[WAVE_CORD_Y][next(posX)] = -SCORE_COUNTER


def changeSpeed():
    global FPS, WAVE_GAP, GAME_SPEED
    if(SCORE_COUNTER % (100 * (GAME_SPEED//2)) == 0) and FPS < 60:
        FPS += 2
        GAME_SPEED *= GAME_SPEED
        print("incremented speed of game")


def changeWave():
    global WAVE_FREQUENCY, WAVE_AMPLITUDE, WAVE_SPEED, WAVE_GAP
    if (SCORE_COUNTER % 10 == 0) and WAVE_GAP < 80:
        WAVE_GAP += 1
        print("Incremented line gap")
    if (SCORE_COUNTER % 200 == 0):
        # WAVE_FREQUENCY = random.randint(1, 6)
        WAVE_AMPLITUDE = random.randint(50, WAVE_AMPLITUDE+WAVE_GAP)


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


def collision():
    ball = pygame.Rect(BALL_CORD_X, BALL_CORD_Y, BALL_RADIUS, BALL_RADIUS)
    for x in range(540, 560):
        afterCalculations = POINTS_MATRIX[x][0]-55-WAVE_GAP
        if 0 < (ball.right - afterCalculations) < 10:
            print("hit from " + str(afterCalculations))


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

        global SCORE_COUNTER, GAME_COUNTER, BALL_CORD_X, BALL_CORD_Y,songNum
        SCORE_COUNTER += 1
        # debug(SCORE_COUNTER)

        changeSpeed()
        changeWave()
        generateWave()

        color = WAVE_COLOUR
        for inside in range(800):
            if inside in range(500, 570):
                color = (255, 0, 0)
            pygame.gfxdraw.pixel(
                GAME_DISPLAY, POINTS_MATRIX[inside][0]-55-WAVE_GAP, POINTS_MATRIX[inside][1]+SCORE_COUNTER, color)

        # so i want to reach a fixed point in the screen that will be the collision area.

        for Y_CORD in range(800):
            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(
                posX)]-55-WAVE_GAP+1, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WAVE_COLOUR)
            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(
                posX)]-55-WAVE_GAP, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WAVE_COLOUR)
            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(
                posX)]-55-WAVE_GAP-1, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WAVE_COLOUR)

            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(
                posX)]-350+WAVE_GAP+1, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WAVE_COLOUR)
            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(
                posX)]-350+WAVE_GAP, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WAVE_COLOUR)
            pygame.gfxdraw.pixel(GAME_DISPLAY, POINTS_MATRIX[Y_CORD][next(
                posX)]-350+WAVE_GAP-1, POINTS_MATRIX[Y_CORD][next(posX)]+SCORE_COUNTER, WAVE_COLOUR)

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
                    songNum +=1


        moveCircle()
        drawCircle(GAME_DISPLAY, BALL_CORD_X, BALL_CORD_Y, BALL_RADIUS, WHITE)
        # collision()

        pygame.display.flip()

        GAME_DISPLAY.blit(SCREEN, (0, 0))

        # update_data_labels(GAME_DISPLAY, SCORE_FONT)


if __name__ == "__main__":
    backgroundMusic()
    run_game()
