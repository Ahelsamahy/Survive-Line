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


# region old code

# if __name__ == "__main__":
#     backgroundMusic()
#     localDir = os.path.dirname(__file__)
#     configPath = os.path.join(localDir, 'config.txt')
#     runNeat(configPath)
# def run_game(self, genomes, config):
    #     global SCORE_COUNTER, GAME_COUNTER, BALL_CORD_X, BALL_CORD_Y, WAVE_GAP, GAME_SPEED, FPS, WAVE_AMPLITUDE, POINTS_I, WAVE_CORD_X, songNum, keepGenerating
    #     pygame.mixer.music.play(-1, 0.0)

    #     Balls = []
    #     ge = []
    #     nets = []

    #     # change difficulty of the game
    #     running = True

    #     while running:
    #         DELTA_TIME = clock.tick(FPS)
    #         SCREEN.fill(BACKGROUND_COLOUR)
    #         SCORE_COUNTER += 1
    #         ballIns = Ball(WAVE_GAP, [BALL_CORD_X, BALL_CORD_Y], [
    #             random.randint(0, 20) / 10 - 1, -3], random.randint(4, 6), GAME_DISPLAY,)
    #         CD = Wave.changeDifficulty(SCORE_COUNTER, WAVE_GAP,
    #                                    GAME_SPEED, FPS, WAVE_AMPLITUDE)
    #         e = Wave.generatePlusFilling(
    #             WAVE_CORD_X, POINTS_I, POINTS_LIST, WAVE_AMPLITUDE)
    #         keepGenerating = True
    #         # if len(POINTS_LIST) > 260:
    #         #     keepGenerating = ballIns.collision()

    #         debug(SCORE_COUNTER)
    #         FPS, GAME_SPEED = CD.changeSpeed()
    #         WAVE_GAP, WAVE_AMPLITUDE = CD.changeWave()
    #         if keepGenerating == False:
    #             gameOver()
    #         else:
    #             WAVE_CORD_X, POINTS_I = e.generateWave()

    #         for genome_id, genome in genomes:
    #             Balls.append(Ball(WAVE_GAP, [BALL_CORD_X, BALL_CORD_Y], [
    #                            random.randint(0, 20) / 10 - 1, -3], random.randint(4, 6), GAME_DISPLAY))
    #             ge.append(genome)
    #             net = neat.nn.FeedForwardNetwork.create(genome, config)
    #             nets.append(net)
    #             genome.fitness = 0

    #         for i, circle in enumerate(Balls):
    #             if ballIns.collision(circle):
    #                 ge[i].fitness -= 1
    #                 remove(i, Balls, ge, nets)

    #         for i, circle in enumerate(Balls):
    #             output = nets[i].activate((circle.rect.y, distance(circle),))
    #             if output[0] > 0.5:
    #                 circle.moveBall(True)

    #         for circle in Balls:
    #             circle.drawBall()
    #             circle.generatebartilces()
    #         for Y_CORD in range(len(POINTS_LIST)):
    #             pygame.gfxdraw.pixel(
    #                 GAME_DISPLAY, POINTS_LIST[Y_CORD]-55-WAVE_GAP, DISPLAY_H-Y_CORD, WAVE_COLOUR)
    #             pygame.gfxdraw.pixel(
    #                 GAME_DISPLAY, POINTS_LIST[Y_CORD]-350+WAVE_GAP, DISPLAY_H-Y_CORD, WAVE_COLOUR)

    #         #[location(x,y), Velocity, Time]
    #         ballIns.generateParticles()
    #         for event in pygame.event.get():
    #             if (event.type == pygame.QUIT):
    #                 pygame.quit()
    #             elif event.type == pygame.KEYDOWN:
    #                 if (event.key == pygame.K_ESCAPE):
    #                     print("ESC key is pressed, will stop now\n")
    #                     pygame.quit()
    #                     sys.exit()
    #                 elif event.key == pygame.K_o:
    #                     optionsMenu()
    #                 elif (event.key == pygame.K_n):
    #                     print("Next Song")
    #                     songNum += 1
    #         BALL_CORD_X = ballIns.moveBall()
    #         ballIns.drawBall(GAME_DISPLAY, BALL_CORD_X,
    #                            BALL_CORD_Y, BALL_RADIUS, WHITE)
    #         pygame.display.flip()
    #         GAME_DISPLAY.blit(SCREEN, (0, 0))

# def remove(index, Balls, Genomes, Nets):
#     Balls.pop(index)
#     Genomes.pop(index)
#     Nets.pop(index)

# def debug(SCORE_COUNTER):
#     print(SCORE_COUNTER)

# def gameOver():
#     global WAVE_GAP, SCORE_COUNTER, POINTS_LIST, POINTS_I
#     pygame.init()

#     while True:
#         SCREEN.fill(BACKGROUND_COLOUR)
#         windowX, windowY = 300, 200
#         startBorderY = (DISPLAY_H-windowY)//2
#         updateLabel("SCORE", BIG_FONT,
#                      windowX//2, DISPLAY_H//2 - startBorderY//4, GAME_DISPLAY)
#         keepCenter = (len(str((abs(round(SCORE_COUNTER//300))))))
#         updateLabel(round(SCORE_COUNTER//200), SCORE_FONT,
#                      DISPLAY_W//2-8 * keepCenter - keepCenter*0.3, DISPLAY_H//2 - startBorderY//8, GAME_DISPLAY)
#         updateLabel("press anykey to play again", NORMAL_FONT,
#                      DISPLAY_W//2 - 75, DISPLAY_H//2 + startBorderY//3, GAME_DISPLAY)
#         pygame.display.update()

#         GAME_DISPLAY.blit(SCREEN, (0, 0))
#         for event in pygame.event.get():
#             if (event.type == pygame.QUIT):
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if (event.key == pygame.K_ESCAPE):
#                     print("ESC key is pressed, will stop now\n")
#                     pygame.quit()
#                     sys.exit()
#                 else:
#                     WAVE_GAP, SCORE_COUNTER, POINTS_LIST, POINTS_I = reset()
#                     WAVE_GAP = 0
#                     game.run_game()

# def backgroundMusic():
#     directory = "./usedMaterial/Music/"
#     playList = {}

#     for file in os.listdir(directory):
#         filename = os.fsdecode(file)
#         if filename.endswith(".mp3"):
#             playList[os.path.join(directory, filename)] = filename[:-4]
#             continue
#         else:
#             continue

#     backgroundMusicDir = (list(playList.keys())[songNum])[1:]
#     pygame.mixer.music.load(os.path.abspath(os.getcwd())+backgroundMusicDir)

# def optionsMenu():

#     pygame.init()

#     while True:
#         SCREEN.fill(BACKGROUND_COLOUR)
#         windowX, windowY = 300, 200
#         startBorderX, startBorderY = DISPLAY_W//2-windowX//2, DISPLAY_H//2-windowY//2
#         pygame.draw.rect(SCREEN, "white", pygame.Rect(
#             startBorderX, startBorderY, windowX, windowY),  2)
#         updateLabel("I don't own the copyright for the songs", NORMAL_FONT,
#                      startBorderX+windowX//10, startBorderY+windowY-30, GAME_DISPLAY)
#         pygame.display.update()

#         GAME_DISPLAY.blit(SCREEN, (0, 0))
#         for event in pygame.event.get():
#             if (event.type == pygame.QUIT):
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if (event.key == pygame.K_ESCAPE):
#                     print("ESC key is pressed, will stop now\n")
#                     pygame.quit()
#                     sys.exit()
#                 elif event.key == pygame.K_BACKSPACE:

#                     run_game()

# def runNeat(configPath):
#     config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          configPath)
#     pop = neat.Population(config)
#     pop.run(game.run_game, 50)

# endregion
