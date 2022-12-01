import pygame
from SurviveLine import Game
import neat
import os
import pickle


class SurviveLineGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.Wave = self.game.Wave
        self.ball = self.game.Ball

    def test_ai(self):
        #, genome, config
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

            # output = net.activate(
            #     (self.ball.ballCordX, self.Wave.pointsList[245:255]))
            # decision = output.index(max(output))

            # if decision == 0:
            #     pass
            # elif decision == 1:
            #     self.game.moveBall(right=False)
            # else:
            #     self.game.moveBall(right=True)

            game_info = self.game.loop()
            self.game.draw()
            self.game.collision()
            pygame.display.update()

        pygame.quit()

    # def train_ai(self, genome1, genome2, config):
    #     net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    #     net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    #     run = True
    #     while run:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 quit()

    #         output1 = net1.activate(
    #             (self.ball.ballCordX, self.Wave.pointsList[245:255]))
    #         decision1 = output1.index(max(output1))

    #         if decision1 == 0:
    #             pass
    #         elif decision1 == 1:
    #             self.game.moveBall(right=False)
    #         else:
    #             self.game.moveBall(right=False)

    #         output2 = net2.activate(
    #             (self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
    #         decision2 = output2.index(max(output2))

    #         if decision2 == 0:
    #             pass
    #         elif decision2 == 1:
    #             self.game.move_paddle(left=False, up=True)
    #         else:
    #             self.game.move_paddle(left=False, up=False)

    #         game_info = Game.loop()

    #         Game.draw(draw_score=False, draw_hits=True)
    #         pygame.display.update()

    #         if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > 50:
    #             self.calculate_fitness(genome1, genome2, game_info)
    #             break

def eval_genomes(genomes, config):
    pass

def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-7')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    width, height = 400, 800
    win = pygame.display.set_mode((width, height))
    e = SurviveLineGame(win,width, height )

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    e.test_ai()
    # run_neat(config)
    # test_ai(config)

