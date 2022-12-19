import pygame
from SurviveLine import Game
import neat
import os
import pickle
from collections import Counter

class SurviveLineGame:
    def __init__(self, window, width, height):
        self.localDir = os.path.dirname(__file__)
        self.game = Game(window, width, height)
        self.Wave = self.game.Wave
        self.ball = self.game.Ball
        self.clock = pygame.time.Clock()


    def normalRun(self):
        run = True
        vision = False
        particles = False
        while run:
            self.clock.tick(self.Wave.FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        vision = not vision
                    if event.key == pygame.K_p:
                        particles = not particles
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
            self.game.draw(vision,particles)

            keepRunning = self.game.collision(run)
            # if keepRunning == False:
            #     run = False
            pygame.display.update()

        pygame.quit()

    def trainAI(self, genome1, config, genomeNum, genNum):
        net = neat.nn.FeedForwardNetwork.create(genome1, config)
        run = True
        vision = False
        particles = False
        self.Wave.waveSpeed = 4
        while run:
            self.clock.tick(self.Wave.FPS*self.Wave.waveSpeed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        vision = not vision
                    if event.key == pygame.K_p:
                        particles = not particles

            fitness = self.game.loop()
            ball = self.game.Ball.ballRect()
            leftWave, rightWave = self.game.countDistance()
            decisions = []
            for leftIn, rightIn in zip (leftWave,rightWave):

                output = net.activate((leftIn, ball.centerx, rightIn))
                decisions.append(output.index(max(output)))
                # layout for the NN of the winner genome
                # input for each instance of the list 10 digits
                # reward if the distance for both left and right is the same
                if((len(str(output[0])) and len(str(output[0]))) > 3 ):
                    if round(output[0], -1) == round(output[2], -1):
                        fitness += 2
    
            # if (all(i in decisions for i in [1,2])):
            #     print("there is intersection") # Checks if all items are in the list
            c =  max(set(decisions), key=decisions.count)
            if c == 0:
                    self.game.moveBall("Left")
            elif c == 1:
                    self.game.moveBall("Center")
            elif c == 2:
                elif decision == 2:
                    self.game.moveBall("Right")

                # reward if the distance for both left and right is the same
                if round(output[0], -1) == round(output[2], -1):
                    fitness += 2

                self.game.draw(vision,particles)
                self.game.displayAINum(genNum, genomeNum)
                self.game.displayRuntime()
                keepRunning = self.game.collision(run)
    
            if(fitness in range(3000, 3003)):
                print("something good happened here")
                outputRuntime = True
                self.game.notificationMusic()
    
                if keepRunning == False:
                    # if it dies early then punishment would be higher
                    if(fitness < 300):
                        fitness -= 50
                    self.calcFitness(genome1, fitness)
                    run = False
                if outputRuntime ==True:
                    print("total runtime is", self.game.runTime)
    
                pygame.display.update()

    def calcFitness(self, genome1, scoreCounter):
        genome1.fitness += scoreCounter

genNum = -1

def evalGenomes(genomes, config):
    global genNum
    width, height = 400, 800
    # , pygame.NOFRAME
    window = pygame.display.set_mode((width, height))
    genNum += 1
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
    # save a checkpoint after each 1 generation
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(evalGenomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    width, height = 400, 800
    # , pygame.NOFRAME
    window = pygame.display.set_mode((width, height))
    e = SurviveLineGame(window, width, height)

    configPath = os.path.join(e.localDir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configPath)

    # e.normalRun()  # run the game without AI
    runNEAT(config)  # train AI
