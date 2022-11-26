import pygame
from SurviveLine import Game
import neat
import os
import pickle


class SurviveLine:
  def __init__(self, window, width, height):
    self.game = Game(window, width, height)
    self.left_paddle = self.game.left_paddle
    self.right_paddle = self.game.right_paddle
    self.ball = self.game.ball