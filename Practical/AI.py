import pygame
from SurviveLine import Game
import neat
import os
import pickle


DISPLAY_W = 400
DISPLAY_H = 800


class SurviveLineGame:
    def __init__(self, window, width, height):
        self.localDir = os.path.dirname(__file__)
        self.game = Game(window, width, height)
        self.Wave = self.game.Wave
        self.ball = self.game.Ball

    def normalRun(self):
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
                self.game.moveBall("Left")
            if keys[pygame.K_RIGHT]:
                self.game.moveBall("Right")
            if keys[pygame.K_ESCAPE]:
                run = False

            self.game.loop()        
            self.game.draw()
            keepRunning = self.game.collision(run)
            if keepRunning == False:
                run = False
            pygame.display.update()

        pygame.quit()

    def trainAI(self, genome1, config, genomeNum,genNum):
        net = neat.nn.FeedForwardNetwork.create(genome1, config)
        g=neat.StdOutReporter(True)
        g.start_generation
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
            fitness = self.game.loop()

            leftWave = self.Wave.PointsList[245] - 338 + self.Wave.WaveGap
            rightWave = self.Wave.PointsList[245] - 55 - self.Wave.WaveGap+9
            ballCord = self.ball.ballCordX
            output = net.activate(
                (ballCord - leftWave, ballCord, rightWave - ballCord))
            decision = output.index(max(output))
            # layout for the NN of the winner genome
            # input for each instance of the list 10 digits

            if decision == 0:
                self.game.moveBall("Left")
            elif decision == 1:
                self.game.moveBall("Center")
                fitness += 1
            elif decision == 2:
                self.game.moveBall("Right")

            self.game.draw()
                        #"", "" genNum, genomeNum
            self.game.displayAINum(genNum, genomeNum)
            self.game.displayRuntime()
            keepRunning = self.game.collision(run)

            #reward if the distance for both left and right is the same 
            if round(output[0], -1) == round(output[2], -1):
                fitness += 2
            if keepRunning == False:
                #if it dies early then punishment would be higher
                if(fitness<300):
                    fitness-=50
                self.calcFitness(genome1, fitness)
                run = False
                
            pygame.display.update()


    def calcFitness(self, genome1, scoreCounter):
        genome1.fitness += scoreCounter

genNum = -1
def evalGenomes(genomes, config):
    global genNum
    width, height = DISPLAY_W, DISPLAY_H
    window = pygame.display.set_mode((width, height))
    genNum+=1
    for i, (genome_id1, genome1) in enumerate(genomes):

        # print the genome number
        genomeNum = round(i/len(genomes)*60)//2 + 1  # double of pop size
        print(genomeNum, end=" ")
        # print(round(i/len(genomes) * 60)//2, end=" ")

        genome1.fitness = 0
        game = SurviveLineGame(window, width, height)
        game.trainAI(genome1, config, genomeNum, genNum)

def runNEAT(config):
    # p = neat.Checkpointer.restore_checkpoint(
    #     e.localDir+"/2022.12.3/"+'neat-checkpoint-7')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #save a checkpoint after each 1 generation
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(evalGenomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    width, height = DISPLAY_W, DISPLAY_H
    window = pygame.display.set_mode((width, height))
    e = SurviveLineGame(window, width, height)

    configPath = os.path.join(e.localDir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configPath)

    # e.normalRun()               #run the game without AI
    runNEAT(config)             #train AI
    # testAI(config)