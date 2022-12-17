## 2022.10.22:

 the problem that was found is that list when it is predefined will add elements to it when it is needed, but will make a problem when trying to move the point when a gap is found to move the points forward, as it throw error "out of index" so to make it right, I had to make a predefined list with 800 element inside of it that they are all zero's then before adding element, it will remove the specific zero at its place

Ended with problem in trying to figure out a way to fill the gap after the first wave (8ooPx) are generated as filling the gaps doesn't wok after it, problem with adding it to the function addPoint(), is that it will make it a recursive function calling when it ends up in filling the gap with for loop

## 2022.10.23:

Gap problem, say that the gap is over the limit of list (800Px), dealing with it before was just to make the gap limited to the end of list, so if the point is at index 797 and the gap is 10 (that means there will be an out of index at extra index 6) so it was just to make it limited to  (gap = DISPLAY_H - POINTS_I - 1) but the problem is that it wouldn't work on high scale when the amplitude gets higher.
to deal with it is to remove the over-points in gap from the beginning of the list and add empty points of the same amount at the end then make the index go back to the new index, back to the same example,
 it will remove 6 points from the beginning of list then add empty 6 points to the end, and shift the index to 6 points in the back so it stays with the new point

## 2022.10.27: 

filling the gap after the first wave
the function does on the first time because the whole list is defined with 0 so there is a gap to go through it and fill, but after the first wave is over, whoever there is a point generated, the addPoint() removes one point from the start to add the new point to the end, so gap can't work at this point and can only keep going after it generates enough points to be extended at, so lets say taht the gap is 20, the wave will generate more than 20 points while the gap is still visible, then run the fillGap() for it

now it is needed to work on the reset function and left collision

make generate wave in a class, that would make pass points_i as a var to the class and deal with the related functions [generateWav(), addPoint(), checkGap(), fillGap()] all with the same var

## 2022.11.5:

the wave not showing when the game reset

I don't know what happened to the code, but when the reset function is called after the collision, it resets all the vars in the game, and it is working, but if i see Points_list in generate wave, it shows that there are points inside of it and they are filled in the right index (which is ok even though all elements should be 0) but on the other hand, in the for loop to draw the lines, it doesn't see the added numbers in the list and just sees a list (Points_list) with zero elements.
what i did is the same with points_i, made a new var for the list in the class constructor of the generatePlusFilling() for the list and changed the usage of it in the whole class.

## 2022.11.25: changing the layout:

so, before, i was making the classes based on the the object, anything that is related to the ball, would be in the ball class, and the same for wave, turns out it is better to have only the basics for the object to instantiate it then the functions such as collision should be inn the game so they can have a return value. so far what i have been doing is implementing the AI in the game, but made another version of the game working by itself without the AI

implemented the game file from the pong game to the class in survivalline

something i had before is the problem of having one file that does the functionality for all components of the game, for instance, the reset function that exsisted in ball func, it is responsible for resetting the whole game including wave related vars, it is better to have a class for the wave then in it have function to reset the related vars for it, then you can call it whenever you want, as for my opinion, this is better because i would get confusing with the vars to call

## 2022.12.1: first working after AI

the whole time between commit `f981680ab8adb38deb7b2e6edc63446752727835` and today, was just making the code more ... OOP you would say, as it was before just leaning on the idea of having the three files for the game (ballFunc, waveFunc and mainL) with the defentions being in one folder defs.py, that made it hard a little bit to make the working game readable, so the new approach that is used now is having function in each component to make only on thing and split them into files,here is the structure.

there is ballFun.py and the waveFunc.py files, all the defs that are related to each of them, is moved to its own ones, then there is function **only** for the basics of it, for example, there was only one reset function to make the whole game reset, but in the new approach, there is reset function in each component class like the Wave and Ball, and in the main game file, there is one reset function that calls the other reset function in wave and ball class.

There is the main game.py that is responsible of making instance of the game and control the functionality in subClasses like moving the ball or generate wave and move ball. The reason for having it is each genome is an instance of the game with its own vars and classes, and each one of them would be separated in the class.

# 2020.12.05: centre is bad

Just committing and adding a centre move, the AI wouldn't choose it because there isn't a change in the statues, so i had to increase the fitness for it.

# 2020.12.14: what's up gap?

so, the old problem I had is that there would be a need for a check gap function to check with the point that is newly made with the one before it and them referee to fillGap to shift the first point in the new line segment by the amount of gap then make a line between the old line segment and the new one, then an idea came to me, what if instead of shifting the point on y axis, I can then shift it on x-axis?

hear me out, in the old way you would need to shift and make a line to keep the ball going on the x-axis without having a gap, but if I can know the gap (which I already know) then decrease the new point by the amount of gap + 1 (if it is a positive gap) and will be -1 if it is a negative gap , you may ask, "why didn't you use absolute value for amount of gap as left is the same as right?" because then this would mean that the wave would increment in one way which depends if it is +1 or -1

the newly implemented function is called `def shiftOnXAxis(self, newPoint)` in `waveFunc.py`

# 2020.12.15: distance (leftWave, ball, rightWave)

As of the early implementation of the AI, the input was (from left to right) the:

- distance between the centre of ball to the point in wave with the same x cord both left and right
- ball x cord

but the problem is the collison covers the whole ballRect (that is 24 pixel) and the NN can only have input of the centre, to solve it you would need to pass a list of the distance between the points on ballRect and the wave on the side, here is a big dive

to work on the right distance, so right now there is ballRect that covers the whole ball and responsible for the collision detection, and there are points with the corresponding x axis on the wave that if any point on the ballRect overlap one of the points (with same x axis) on the wave, the collison will be triggered and this genome will be over, to think more into details, i need to check first with the point on the bottom right side of the ballRect with the one same as x axis on the wave, then move one point up one wave and calculate it (using Pythagoras) when the points on list are over, then move one pixel up the ballRect and repeat the same on the wave.

![ball vision](./../../../progressMedia/images/vision 576 line.png)

<p style="text-align:center;font-size:13px">keep in mind that the starting point is in the middle of the ball in the image, but it is just a simple way to say that there is a vision</p>

Sounds good, but the problem is that the for loop was CPU consuming, imagine there are 24 pixel then repeat it again for the wave ones (a two inner for loops) $24^2 = 576$ and another one for the left side $576*2 = 1152$,  and to process them again on the AI input , that is $1152*2 = 2304$ times, all is made in one second, not to add the particles that are being made behind the ball, all of this was a lot. To make a little better, I reduced the step size to be 5 for each loop, made it to 45 in each list

|                  576 lines on each side                  |                     45 on each side                     |
| :------------------------------------------------------: | :-----------------------------------------------------: |
| ![](./../../../progressMedia/images/vision 576 line.png) | ![](./../../../progressMedia/images/vision 45 line.png) |

you might ask "will this reduce the vision of the AI ?", quite frankly, I think if it could handle itself with only one point, then  it can do better with 45 line on each side, it even gave more space to add extra point, so it can see the future now (an extra 20 points on wave)

# 2020.12.17: give NN list as input ?!!

A NN would need you to define the amount of input that it will work on, also the output, you can't try to find a way around by using a list and feed it more input that you have defined, which is the problem I ran into after the last log (12.15) is after getting list of distance between the ballRect and the point in wave, i was trying to feed all of it in the NN, and this wouldn't work because you can't multiply a whole list (as all) by an int `TypeError: can't multiply sequence by non-int of type 'float` even when i tried to overcome it by transfering the list to array or a full string so it can be used just as a place holder.

Then i thought about having each point to have its own output decision, the secret key is `zip()` which allows me to loop through two lists parallel, which makes sense in my case (right and left distance), let's count the input again using the old way (distance from ball **left** side to the **left** wave, ball x coordinates, distance from ball **right** side to the **right** wave) so it is the same x coordinates that i would need when going up the wave.
Turns out that it would work with some tweaks to the wave speed, because the `zip()` made the loop go through extra itirations that made xpoints be generated more than (amount of points in right or left list) usual you can say, that effected the counter that is used to change the wave amplitude and fps of game.

