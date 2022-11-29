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

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(Game.)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.game.moveBall(right=False)
            if keys[pygame.K_RIGHT]:
                self.game.moveBall(right=True)

            output = net.activate(
                (self.ball.ballCordX, self.Wave.pointsList[245:255]))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.moveBall(right=False)
            else:
                self.game.moveBall(right=True)

            game_info = self.game.loop()
            self.game.draw(True, False)
            pygame.display.update()

        pygame.quit()