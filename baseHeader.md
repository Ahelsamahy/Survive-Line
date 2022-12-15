# Timeline

The first step of developing the game was choosing a programming language that would be helpful in both showing graphics on screen and implement an AI algorithm, the only option that was convenient enough was python as:

```
\begin{enumerate}
  \item The most famous programming langauge with AI libraries that have a good documentation.
  \item It is OOP, which means i can have a class for each component of the game easily to make an instance for the AI to train from.
  \item A library to draw graphic on screen while it won't need heavy CPU usage that won't throtle the process of AI learning 
\end{enumerate}
```

Going for a library for the game was the first step as it would define the characteristics, i went for **PyGame** because it was nearly the only one that is good enough with documentation to start with, and quit enough, the main focus isn't about making a game that will have that physics in it and 3d animation, for now, the imagined picture of the game is a rectangle as a screen that will have two main component of the game, wave that is on one side of the screen vertically and the one on the other side with the only difference is 350px (because the starting amplitude is 50px and the screen width is 400px) and a ball that the **only purpose for it is to survive the as much as it can, without hitting any of the sides of the wave**, the accent colour of the game will be between black as a background and white to show the elements, with an additional score counter on the top middle part of screen to keep record of points.

## Develop the game

 the files layout of the game will be an `AI.py` file in the root folder, then subfolder named `SurviveLine` with 3 files in it `ballFunc.py` `waveFunc.py` and `game.py`, and to make it easy to make instance of the game, will create a file named `__init__.py` that will only have one line it it `from .game import Game` that means we will have a `Class Game():` in the `game.py` and it is used to call the `game` function as a library in the `AI.py` file (as it is in another folder) and make instance from it, but will get into this later in the AI section.

### Wave functionality

To get the base function of wave there would be a lot of functions to cover like:

```python
def draw(self, Display):
    #increase the FPS of game
def changeSpeed(self):
    #change the wave aplitude and increase the wave gap
def changeWave(self):
    #generate a new point on Y axis
def generateWave(self):
    #add point to the list of points
def addPoint(self, index, point):
    #check if there is a gap 
def checkGap(self):
    #function to fill it
def fillGap(self, gap, gapDirection):
    #reset all the self. variable that are made in __init__ class 
def reset(self):
```

most of them are self explanatory, but the ones that need more dive into details are the `generateWave`, `checkGap`and `fillGap`

#### Generate Wave

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

#### Check gap

after generating a point, with the change in amplitude, the next point that is added to list of points, doesn't have a difference of only 1px with the one before it, so that means that there will be a different line segments in the list and a gap between them, to overcome this, after a point is generated, there is a for loop that checks is there is only one pixel gap between it and the point before it, either it is minus or negative as the gap can be to left side or right side

![filledGap](./../../progressMedia/images/filledGap.jpg)

#### Fill Gap

if there is one part which took the most in the writing, i would say it is this part, because there were different approaches to solve the problem, first one is either to move the point on y axis by the gap then make a straight line from the old line segment to it, and the second one was to get the point just to be minus on the x axis then be linked to it. the first option was better for the sake of visibility and not effecting the next point respectively. There were lots of ways (or you can say conditions) that needs to be covered in the point list, for example what if the gap is at the end of list?  will throw "out of index error", one way to cover this is by removing amount of points from the start of the list, then add the same amount at the end where you need it,

Say that the gap is over the limit of list (800Px), dealing with it before was just to make the gap limited to the end of list, so if the point is at index 797 and the gap is 10 (that means there will be an out of index at extra index 6) so it was just to make it limited to  `gap = DISPLAY_H - POINTS_I - 1` but the problem is that it wouldn't work on high scale when the amplitude gets higher.
to deal with it is to remove the over-points in gap from the beginning of the list and add empty points of the same amount at the end then make the index go back to the new index, back to the same example,
It will remove 6 points from the beginning of list then add empty 6 points to the end, and shift the index to 6 points in the back so it stays with the new point.

```python
if self.PointsI + (gap) >= self.HDisplay-1:
	untilEnd = self.HDisplay-self.PointsI
	toAddFromStart = abs(gap-untilEnd)
	del self.PointsList[:toAddFromStart]
	toAdd = [0]*toAddFromStart
	self.PointsList.extend(toAdd)
	self.PointsI -= toAddFromStart
	gap -= 1
```

with every line here looks like a weird by itself, you would need some explanation:

- Line 2: calculate the difference between the ending point of list and the starting point of gap
- Line 3: get the difference in gap and the point
- Line 4: delete the amount of point from the beginning of list
- Line 5: create empty list with the amount of delete points from beginning of list

Now with the condition being fulfilled, it comes to fill the gap itself, there would be a two options (or ways you can say), but I will discuss one only and the other one have the same implementation with difference being the sign

```python
if (gapDirection):
	# to move the point according to gap
	self.PointsList[self.PointsI + gap] = self.PointsList[self.PointsI]
	self.PointsList[self.PointsI] = 0
    #the step is different for gap direction, as it would be -1 or +1
	for x in range(self.PointsList[self.PointsI-1], self.PointsList[self.PointsI+gap]-1, (gap//gap)):
		self.PointsList[insideY] = x+1
		if insideY < 799:
			insideY += 1
```

first it moves the point by the amount of gap then resets the old value of it to zero, secondly is a for loop to fill the points incrementally starting from the last point in the old line segment to the new point.

### Ball functionality

The main focus when working on the ball was to make it as simple as it can be so a new instance can be done from it without the need to store a self-genome variable, so every genome would have its own variables that can be changed with a new instance made.

#### Draw ball

As the game is based on a **ball** that survives a line, then I need to display a ball and not a circle, there isn't a function to draw a filled ball in one line, so i have to draw an empty circle then fill it, the function `pygame.gfxdraw.aacircle` will draw a  draw an anti-aliased circle and `pygame.gfxdraw.filled_circle` draw a filled circle inside of it, then draw a fake rectangle around them with `pygame.Rect` that will deal with the collision (will discuss it in the display game section)

#### Generate particles

This part is little on logic than the other because it was made for the visuality of the game, no output coming out of it to make the game faster or improve something, but it would add a little bit of a characteristic to the game and the vision I have for it.

The particles are made to hold the position of the ball and generate as a way to look like a combustion engine steam coming out ot it, so there are three things to notice here

- Location: where the particles will start and their ending point

- Velocity: the amount of particles that will be generated in a second

- Time: how long they will last on the screen


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

in the `Vel `variable deceleration part, it makes sure that the value we would get, would be a random number between {-1, 1} and the `Timer ` to give chaos to the particles so not all of them are released at the same time.

The code would add to list of particles a new one with these random starting values, then the for loop process each value on its own.

- line 7: it process the position on X-axis to the velocity also on the X-axis, same would happen to the Y-coordinates
- `particles[2]` is to reduce the particle radius by 0.1 in every frame (which is every loop then) 
- if condition at the end to remove the particle from the list so it wouldn't take much of space

this function is posible thanks to 

[^https://www.youtube.com/watch?v=F69-t33e8tk]: Particles - Pygame Tutorial by  DaFluffyPotato



########second section of header########

## Display the game



### Draw



#### Update label



#### Display score



#### Display AI number



### Collision



### Move ball



### Loop



### Reset



########third section of header########

## Create AI

### What is N.E.A.T ?

### Tweak AI

### Teach AI