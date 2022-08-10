import pygame
import time
import math
from numpy import random



# Some config width height settings
canvas_width = 400
canvas_height = 700
lineGap=0
scoreCounter=0

# Just define some colors we can use
color = pygame.Color(255, 255, 255, 0)
background_color = pygame.Color(0, 0, 0, 0)


pygame.init()
# Set the window title
pygame.display.set_caption("Sine Wave")

# Make a screen to see
screen = pygame.display.set_mode((canvas_width, canvas_height))
screen.fill(background_color)

# Make a surface to draw on
surface = pygame.Surface((canvas_width, canvas_height))
surface.fill(background_color)


# Simple main loop
running = True
while running:

    clock = pygame.time.Clock()
    dt = clock.tick(30)
    # x = random.randint(100)
    # print(x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Redraw the background
    surface.fill(background_color)

    # Update sine wave
    frequency = 1
    amplitude = 50  # in px
    speed = 2
    scoreCounter+=1
    print(scoreCounter)
    if  (scoreCounter%20==0):
        lineGap+=1
    
    for x in range(0, canvas_height):
        y = int((canvas_height/2) + amplitude*math.sin(frequency *
                ((float(x)/canvas_width)*(2*math.pi) + (speed*time.time()))))
        # amplitude = random.randint(100)
        surface.set_at((y-lineGap, x), color)
        surface.set_at((y-300+lineGap, x), color)

    # Put the surface we draw on, onto the screen
    screen.blit(surface, (0, 0))

    # Show it.
    pygame.display.flip()

# import pygame
# import sys
# import math
# pygame.init()
# screen = pygame.display.set_mode([640, 480])
# screen.fill([0, 0, 0])
# plotPoints = []
# for x in range(0, 640):
#     y = int(math.sin(x/640.0 * 4 * math.pi) * 200 + 240)
#     plotPoints.append([x, y])
# pygame.draw.lines(screen, [255, 255, 255], False, plotPoints, 2)
# pygame.display.flip()
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()

# import math
# import pygame

# pygame.init()
# screen = pygame.display.set_mode((400,400))
# clock = pygame.time.Clock()
# FPS =30
# while True:
#     dt = clock.tick(FPS)
#     t = pygame.time.get_ticks() / 2  % 400 # scale and loop time
#     x = t
#     y = math.sin(t/50.0) * 100 + 200       # scale sine wave
#     y = int(y)                             # needs to be int

#     screen.fill((0,0,0))
#     pygame.draw.line(screen, (255,255,255), (x, y), 30)

#     pygame.display.flip()

# import pygame
# import math
# import time


# frequency = 5
# amplitude = 50
# overallY = 300

# clock = pygame.time.Clock()
# dt = 0
# game_time = 0

# while True:
#   dt = clock.tick(30)
#   game_time += dt
#   gameDisplay = pygame.display.set_mode((600, 600))
#   gameDisplay.fill((0,0,0))


#   no_pts = gameDisplay.get_width()
#   for i in range(no_pts):
#       x = i/no_pts * 2 * math.pi
#       y = (amplitude * math.cos(x * frequency)) + overallY
#       if i > 0:
#           pygame.draw.line(gameDisplay, (0, 0, 0),  prev_pt, (i, y))
#       prev_pt = (i, y)
#       pygame.display.update()
