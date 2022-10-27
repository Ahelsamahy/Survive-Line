import sys
import os
import pygame
import pygame.gfxdraw

from ballFunc import *
from waveFunc import *

clock = pygame.time.Clock()
SCREEN = pygame.Surface((DISPLAY_W, DISPLAY_H))

songNum = 1

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


class ballParticles:
    def __init__(self, loc, vel, timer):
        # [loc, velocity, timer]
        PARTICLES.append([loc, vel, timer])

        for particle in PARTICLES:
            particle[0][0] -= particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1

            pygame.draw.circle(GAME_DISPLAY, (255, 255, 255), [int(
                particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                PARTICLES.remove(particle)


def debug(SCORE_COUNTER):
    print(SCORE_COUNTER)


def gameOver():
    global WAVE_GAP, SCORE_COUNTER, POINTS_LIST, pointsIndex
    pygame.init()

    while True:
        SCREEN.fill(background_color)
        windowX, windowY = 300, 200
        startBorderY = (DISPLAY_H-windowY)//2
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
                    WAVE_GAP, SCORE_COUNTER, POINTS_LIST, pointsIndex = reset()
                    WAVE_GAP = 0
                    run_game()


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

    while True:
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

        global SCORE_COUNTER, GAME_COUNTER, BALL_CORD_X, BALL_CORD_Y, WAVE_GAP, WAVE_AMPLITUDE, songNum, keepGenerating
        SCORE_COUNTER += 1
        keepGenerating = True
        if len(POINTS_LIST) > 260:
            keepGenerating = collision(WAVE_GAP)

        debug(SCORE_COUNTER)

        changeSpeed(SCORE_COUNTER)
        WAVE_GAP, WAVE_AMPLITUDE = changeWave(SCORE_COUNTER, WAVE_GAP)

        if keepGenerating == False:
            gameOver()
        else:
            generateWave()

        for Y_CORD in range(len(POINTS_LIST)):
            # pygame.gfxdraw.pixel(
            # GAME_DISPLAY, POINTS_LIST[Y_CORD]-55-WAVE_GAP-1, DISPLAY_H-Y_CORD, WAVE_COLOUR)
            pygame.gfxdraw.pixel(
                GAME_DISPLAY, POINTS_LIST[Y_CORD]-55-WAVE_GAP, DISPLAY_H-Y_CORD, WAVE_COLOUR)
            # pygame.gfxdraw.pixel(
            # GAME_DISPLAY, POINTS_LIST[Y_CORD]-55-WAVE_GAP+1, DISPLAY_H-Y_CORD, WAVE_COLOUR)

            # pygame.gfxdraw.pixel(
            # GAME_DISPLAY, POINTS_LIST[Y_CORD]-350+WAVE_GAP-1, DISPLAY_H-Y_CORD, WAVE_COLOUR)
            pygame.gfxdraw.pixel(
                GAME_DISPLAY, POINTS_LIST[Y_CORD]-350+WAVE_GAP, DISPLAY_H-Y_CORD, WAVE_COLOUR)
            # pygame.gfxdraw.pixel(
            # GAME_DISPLAY, POINTS_LIST[Y_CORD]-350+WAVE_GAP+1, DISPLAY_H-Y_CORD, WAVE_COLOUR)

        #[location(x,y), Velocity, Time]
        ballParticles([BALL_CORD_X, BALL_CORD_Y], [
                      random.randint(0, 20) / 10 - 1, -3], random.randint(4, 6))

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

        BALL_CORD_X = moveCircle()
        drawCircle(GAME_DISPLAY, BALL_CORD_X, BALL_CORD_Y, BALL_RADIUS, WHITE)

        pygame.display.flip()

        GAME_DISPLAY.blit(SCREEN, (0, 0))


if __name__ == "__main__":
    backgroundMusic()
    run_game()
