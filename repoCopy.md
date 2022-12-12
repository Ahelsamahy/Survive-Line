The first step of developing the game was choosing a programming language that would be helpful in both showing graphics on screen and implement an AI algorithm, the only option that was convenient enough  was python as:

```
\begin{enumerate}
  \item The most famous programming langauge with AI libraries that have a good documentation.
  \item It is OOP, which means i can have a class for each component of the game easily to make an instance for the AI to train from.
  \item A library to draw graphic on screen while it won't need heavy CPU usage that won't throtle the process of AI learning 
\end{enumerate}
```

Going for a library for the game was the first step as it would define the characteristics, i went for **PyGame** because it was nearly the only one that is good enough with documentation to start with, and quit enough, the main focus isn't about making a game that will have that physics in it and 3d animation, for now, the imagined picture of the game is a rectangle as a screen that will have two main component of the game, wave that is on one side of the screen vertically and the one on the other side with the only difference is 350px (because the starting amplitude is 50px and the screen width is 400px) and a ball that the **only purpose for it is to survive the as much as it can, without hitting any of the sides of the wave**, the accent colour of the game will be between black as a background and white to show the elements, with an additional score counter on the top middle part of screen to keep record of points.

 the files layout of the game will be an `AI.py` file in the root folder, then subfolder named `SurviveLine` with 3 files in it `ballFunc.py` `waveFunc.py` and `game.py`, and to make it easy to make instance of the game, will create a file named `__init__.py` that will only have one line it it `from .game import Game` that means we will have a `Class Game():` in the `game.py` and it is used to call the `game` function as a library in the `AI.py` file (as it is in another folder) and make instance from it, but will get into this later in the AI section.



# Wave function

The starting point of the game, in the `waveFunc.py` to make a main class `Class Wave():` with  an equation that can generate a wave and at the same time I can change in the variables of the wave to make it harder for the player, these variable are 
wave amplitude\footnote{is the maximum or lowest height the wave can go in one point to up or down} or 
wave frequency \footnote{the number of waves that can go through a fixed distance in amount of time} with all of this in calculation, it means that I can make the game harder by making the behaviour unexpected for the next move, also to go extra step, there will be a decrease in the gap between the two waves to limit the player's movement.

```python
pointsList_XCord = int((self.HDisplay/2) + self.WaveAmplitude* math.sin(self.waveFreq * ((float(0)/-self.WDisplay)*(2*math.pi) + (time.time()))))
```

%add caption here

as you can see, there are some variables that have the `self.` before, that are defined as:

```python
def __init__(self, wDisplay, hDisplay):
        self.WDisplay = wDisplay
        self.HDisplay = hDisplay
        self.ScoreCount = 0  # will come back later for it, in the loop IMPORTANT
        self.waveFreq = 1  # will change later in difficulty part
        self.WaveGap = 0
        self.GameSpeed = 2  # to increment the difference in time to speed the FPS
        self.FPS = 60
        self.WaveAmplitude = 50
        self.PointsI = 0  # index to loop inside the points list
        self.PointsList = [0]*800
```

These are the variables that are only (and not specifically ) linked to the wave functions, and this is where an important functionality of OOP comes in ,that is encapsulation, to get all the related data to a class (which is wave class at this point), in it only and not others, if it is needed in other classes, then an instance of class wave can be made then the variable can be used from it.

The equation in figure #### is going to store the X axis coordinates in a list called `PointsList` for the sake of adding points to it once they are generated and show them on screen one by one as if it is loading, because if there isn't list, then the wave would be a steady visual sine wave (without changing amplitude or frequency yet), this part of code is placed in `def generateWave(self)` function.

there have to be more condition to make the points be generated without disorder, like one point won't be in the other half of screen, which means that when the 350px is added to it, it will be out of the borders of the display.

there would be a counter in the main game file `game.py` that is incremented by one each time the game takes a loop, so how the game display actually ?

### Display the game

there is a main while loop in the `AI.py` file that is controlled by a variable called `run=True`, the reason for it to be a variable not the Boolean `True` is to stop the game once there is a collision then start the next genome after. The functionality for it can be broken into several points.

- paint the background with black
- have a score counter (1 point each loop)
- go through all the points in `PointsList` and display all of them
- draw the ball
- draw a rectangle surrounding the ball (for collision detection)
- show particles

from that you would need a function to take care of the repetitve tasks that nees to be checked during the time of running the game, like collision, show particles and change wave, all of this is being done in the `def loop(self)` at the `game.def` and it basically take care of the functions that are related to the ball and wave, like collision, draw, move ball and display some info while teaching the AI, that was a lot without explaining, will go throguh each one a little

#### Collision

it gets an instance of the ball as there is a function in PyGame to have a fake (invisible) rectangle around a spirit (that is how players are called) and from that you have a direction points without defining them as a coordinates, for example, the ball starts at the middle of screen( point 200px) and goes 12px as radius, that means 188px for left edge of ball and 212px for the right edge and all of this would need to be stored, imagine doing the same for bottom left, bottom right, top left top right. it would need to store extra variables that aren't needed, so there are `spirit.right` to deal with the right side of the spirit and detect if it **overlaps** another object, it would be usefull in the case of collision as the points are stored in a list, so i don't have to check all of it, just for the radius of the ball, but to make it go further, i reduced the range so it wouldn't make more effort on the CPU during the training.

```python
def collision(self, runLoop):
        ball = self.Ball.drawBall(self.window)
        Wave = self.Wave
        for x in range(240, 250):
            if (Wave.PointsList[x] != 0) and (ball.right >= Wave.PointsList[x]-55-Wave.WaveGap+9):
                # print("hit from " + str(x) + " right")
                return runLoop == False

            if (Wave.PointsList[x] != 0) and ball.left <= Wave.PointsList[x]-338+Wave.WaveGap:
                # print("hit from " + str(x) + " left")
                return runLoop == False
```

You would notice that there is a return variable from the function, it is linked to the call in `main.py` just to stop the main while loop and start he next genome.

```python
			keepRunning = self.game.collision(run)
            if keepRunning == False:
                run = False
                #which would by then terminate the main while loop of game
```

#### Move ball

As I'm still explaning about the borders of game and ball movememnet, it would be a good chance to talk about the ball movement mechanisem, it is controlled by the function `def moveBall()` in the `game.py` as it is the one in control of the main functions of the game, in case there is an output of the neural network to move the ball right then the function would check if the ball is still in the space of screen and the right side of the ball isn't over the screen width, also the left side of ball isn't lower than the screen width

```python
def moveBall(self, dir):
        if (dir =="Right" and self.Ball.ballCordX + (Ball.BALL_RADIUS*2) < Game.DISPLAY_W):
            self.Ball.moveBall(right=True)
            return False
        elif (dir =="Left" and (self.Ball.ballCordX > 0 + Ball.BALL_RADIUS*2)):
            self.Ball.moveBall(right=False)
            return False
        elif  dir == "Center":
            return False
        return True
```

the point of having an if statement for centre is that during the learning period of AI, there neural network would always seek a change in its input to get a different output, in case of centre output, that would mean that output is the same, there had to be an extra reward in case of centre output to encourage the neural network to choose it (will discuss it into more details in the AI part)



####  Particles

this part is a little logic than the other because it was made for the visuallty of the game, no output coming out of it to make the gmae faster or improve something, but it would add a little bit of a characteristic to the game and the vision i have for it.

The particles are made to hold the position of the ball and generate as a way to look like a combustion engine steam coming out ot it, so there are three things to notice her

Location: where the particles will start and ending point

Velocity: the amount of particles that will be generated in a second

Time: how long they will last on the screen

With this in consideration, we can start writing a function for it 

```python
def generateParticles(self):
        Loc =[self.ballCordX, self.ballCordY] 
        Vel = [random.randint(0, 20) / 10 - 1, -3]
        Timer = random.randint(4, 6)
        self.Particles.append([Loc, Vel, Timer])
        for particle in self.Particles:
            particle[0][0] -= particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1

            pygame.draw.circle(self.GameDisplay, (255, 255, 255), [int(
                particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.Particles.remove(particle)
```

in the vel variable deceleration part, it makes sure that the value we would get, would be a random number between {-1,1} and timer to give chaos to the particles so not all of them are released at the same time.

The code would add to list of particles a new one with these random starting values, then the for loop process each value on its own.

- line 7: it process the position on X-axis to the velocity also on the X-axis, same would happen to the Y-coordinates
- `particles[2]` is to reduce the particle radius by 0.1 in every frame (which is every loop then) 
- if condition at the end to remove the particle from the list so it wouldn't take much of space

this function is posible thanks to 

[^https://www.youtube.com/watch?v=F69-t33e8tk]:Particles - Pygame Tutorial by  DaFluffyPotato



\begin{equation}



\end{equation}