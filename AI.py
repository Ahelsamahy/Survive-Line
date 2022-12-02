import pygame
from SurviveLine import Game
import neat
import os
import pickle


DISPLAY_W = 400
DISPLAY_H = 800


class SurviveLineGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.Wave = self.game.Wave
        self.ball = self.game.Ball


    def testAI(self):
        # , genome, config
        # net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.game.moveBall(right=False)
            if keys[pygame.K_RIGHT]:
                self.game.moveBall(right=True)
            if keys[pygame.K_ESCAPE]:
                run = False

            # leftWave = self.Wave.PointsList[245:255] - 338 + self.Wave.WaveGap
            # rightWave = self.Wave.PointsList[245:255] - 55 - self.Wave.WaveGap+9
            # ballCord = self.ball.ballCordX
            # output = net.activate(
            #     (ballCord - leftWave, ballCord, rightWave - ballCord))
            # decision = output.index(max(output))

            # if decision == 0:
            #     pass
            # elif decision == 1:
            #     self.game.moveBall(right=False)
            # else:
            #     self.game.moveBall(right=True)

            self.game.loop()
            self.game.draw()
            keepRunning = self.game.collision(run)
            if  keepRunning==False:
                run = False
            pygame.display.update()

        pygame.quit()

    def trainAI(self, genome1, config):
        net = neat.nn.FeedForwardNetwork.create(genome1, config)

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(self.Wave.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    quit()

            leftWave = self.Wave.PointsList[245] - 338 + self.Wave.WaveGap
            rightWave = self.Wave.PointsList[245] - 55 - self.Wave.WaveGap+9
            ballCord = self.ball.ballCordX
            output = net.activate(
                (ballCord - leftWave, ballCord, rightWave - ballCord))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.moveBall(right=False)
            else:
                self.game.moveBall(right=True)

            self.game.loop()    
            self.game.draw()
            keepRunning = self.game.collision(run)
            if  keepRunning==False:
                run = False
            pygame.display.update()

            if self.Wave.ScoreCount >= 2000:
                self.calcFitness(genome1, self.Wave.ScoreCount)
                break

    def calcFitness(self, genome1, scoreCounter):
        genome1.fitness += scoreCounter


def evalGenomes(genomes, config):
    width, height = DISPLAY_W, DISPLAY_H
    window = pygame.display.set_mode((width, height))
    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
        # print(round(i/len(genomes) * 100), end=" ")
        game = SurviveLineGame(window, width, height)
        game.trainAI(genome1, config)


def runNEAT(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-7')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(evalGenomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def testAI(config):
    width, height = DISPLAY_W, DISPLAY_H
    window = pygame.display.set_mode((width, height))

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = SurviveLineGame(window, width, height)
    # game.testAI(winner, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    configPath = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configPath)
    width, height = DISPLAY_W, DISPLAY_H
    window = pygame.display.set_mode((width, height))
    e = SurviveLineGame(window, width, height)
    # e.testAI()
    runNEAT(config)
    # testAI(config)
