w, h = 2, 800
Matrix = [[0 for x in range(w)] for y in range(h)]

Matrix[0][0] = 1
Matrix[0][1]=359
Matrix[0][2]=359

print(Matrix[0][0])  
print(Matrix[0][1])  


# from array import *

# t = [ [0]*2 for i in range(800)]
# t[1][1]="tt"
# for i in t:
#     print(i)


# print("Initialize dictionary multiple key-value : " + str(to_dict))


# print(matrix)

# for x in matrix:
#     for x in range(10):
#         for y in range(3):
#             x.update({x:y})

# print(matrix)

# from pickle import TRUE
# import pygame
# import pygame.gfxdraw
# import math
# import time
# from defs import *


# clock = pygame.time.Clock()
# dt = 0
# game_time = 0

# pygame.init()
# # Make a window to show on
# gameDisplay = pygame.display.set_mode(
#     (DISPLAY_W, DISPLAY_H))
# pygame.display.set_caption('Survive line')
# # Make a surface to draw on
# surface = pygame.Surface((DISPLAY_W, DISPLAY_H))
# surface.fill(background_color)
# running = True
# x=100
# while running:
#     dt = clock.tick(30)
#     game_time += dt
#     pygame.gfxdraw.line(gameDisplay, 60, 80, 130, 100, (255, 255, 255))
#     pygame.draw.aaline(gameDisplay, (255, 255, 255), (60, 100), (130, 120), blend=0)
#     pygame.draw.line(gameDisplay, (255, 255, 255), (60, 120), (130, 140), width=6)
#     no_pts = gameDisplay.get_width()

#     x=100
#     for x in range(50):
#         pygame.gfxdraw.pixel(gameDisplay,60+x+1, 170+x, (255, 255, 255))
#         pygame.gfxdraw.pixel(gameDisplay,60+x, 170+x, (255, 255, 255))
#         pygame.gfxdraw.pixel(gameDisplay,60+x-1, 170+x, (255, 255, 255))

#     pygame.display.update()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             running = TRUE
#             print("A key is pressed, will stop now\n")
