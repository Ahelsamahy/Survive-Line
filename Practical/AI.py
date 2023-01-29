import pygame
from SurviveLine import Game
import neat
import os
import pickle

class SurviveLineGame:
    def __init__(self, window, width, height):
        self.window = window
        self.localDir = os.path.dirname(__file__)
        self.game = Game(window, width, height)
        self.Wave = self.game.Wave
        self.ball = self.game.Ball
        self.clock = pygame.time.Clock()
        self.outputRuntime = False
        self.threshold = 200*101


    def normalRun(self):
        run = True
        vision = False
        showParticles = False
        drawBallRec = False
        self.Wave.waveSpeed = 1
        while run:
            self.clock.tick(self.Wave.FPS*self.Wave.waveSpeed)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        vision = not vision
                    if event.key == pygame.K_p:
                        showParticles = not showParticles
                    if event.key == pygame.K_b:
                        drawBallRec = not drawBallRec
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
            self.game.draw(vision, showParticles , drawBallRec)

            keepRunning = self.game.collision(run)
            # if keepRunning == False:
            #     run = False
            pygame.display.update()

        pygame.quit()

    def trainAI(self, genome1, config, genomeNum, genNum):
        net = neat.nn.FeedForwardNetwork.create(genome1, config)
        run = True
        vision = True
        showParticles = False
        drawBallRec = False
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
                        showParticles = not showParticles
                    if event.key == pygame.K_b:
                        drawBallRec = not drawBallRec
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        quit()

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
                leftDis = int(output[0])
                rightDis = int (output[2])
                if(len(str(leftDis)) and len(str(rightDis)) > 2 ):
                    if round(leftDis, -1) == round(rightDis, -1):
                        fitness += 2
            
            # if (all(i in decisions for i in [1,2])):
            #     print("there is intersection") # Checks if all items are in the list
            c =  max(set(decisions), key=decisions.count)
            if c == 0:
                self.game.moveBall("Left")
            elif c == 1:
                self.game.moveBall("Center")
            elif c == 2:
                self.game.moveBall("Right")

            self.game.draw(vision, showParticles, drawBallRec)
            self.game.displayAINum(genNum, genomeNum)
            self.game.displayRuntime()
            keepRunning = self.game.collision(run)

            # when it reaches 50 = 10000/200 
            if(fitness in range(10000, 10004)):
                # print("something good happened here")
                self.outputRuntime = True
                drawBallRec = True
                # self.game.notificationMusic()

            #stop the genome at this point, as it already reached a high score of 200
            if fitness>self.threshold:
                keepRunning = False

            if keepRunning == False:
                # if it dies early then punishment would be higher
                if(fitness < 300):
                    fitness -= 20
                self.calcFitness(genome1, fitness)
                run = False

            pygame.display.update()

    def calcFitness(self, genome1, scoreCounter):
        genome1.fitness = scoreCounter

genNum = -1
highestFitness = 0
highestGenerationFitness = 0
highestGenomeFitness = 0
def evalGenomes(genomes, config):

    global genNum, highestFitness,highestGenerationFitness,highestGenomeFitness
    width, height = 400, 800
    # , pygame.NOFRAME
    window = pygame.display.set_mode((width, height))
    genNum += 1

    for i, (genome_id, genome) in enumerate(genomes):

        genomeNum = round(i/len(genomes)*60)//2 + 1  # double of pop size
        # print(genomeNum, end=" ")

        genome.fitness = 0
        game = SurviveLineGame(window, width, height)
        game.trainAI(genome, config, genomeNum, genNum)
        if game.outputRuntime == True:
            if game.threshold < genome.fitness:
                print("{0} reached the threshold".format(genomeNum))
            else:
                print("genome number {0} = {1}S with fitness {2}".format(genomeNum, game.game.runTime, genome.fitness//200))
        if genome.fitness > highestFitness:
            highestFitness = genome.fitness
            highestGenerationFitness = genNum
            highestGenomeFitness = genomeNum

    print("highest fitness now is {0} generation {1} genome {2}".format(highestFitness,highestGenerationFitness, highestGenomeFitness))

def runNEAT(config):
    # p = neat.Checkpointer.restore_checkpoint(e.localDir+"/2022.12.19.1/"+'neat-checkpoint-89')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # save a checkpoint after each 1 generation
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(evalGenomes, 200)
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
