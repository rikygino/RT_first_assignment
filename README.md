Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## Assignment
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

The aim of the program is to help the robot to do not crush on the walls going count-clockwise,
also it's going to pick every single silver token and put it behind itself while he is mapping
a way of the route, trying to stay in parallel with the walls

You can run the program with:

```bash
$ python run.py assignment.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/


----------------------------------------------------------------------

## Pseudocode

```
a_th = 2.0  #float: Threshold for the control of the linear distance

d_th = 0.4  #float: Threshold for the control of the orientation

R = Robot()  #instance of the class Robot

function drive(speed, seconds)
	turn on the motors with the speed received as a parameter
	then put in pause the motors after the time interval 'seconds'

function turn(speed, seconds)
	setting an angular velocity using "speed"

function findSilverToken()

    initialize distance at 100
    for each token that can seen by Robot()
        if the token have a value of the distance that is less than 100 
            && token is a silver token 
            && the angle between robot and token is less than 88 and more than -88

            than the distance is the distance between the found token and the robot

        the angle between token and robot is set equal to the angle of robot and token seen by Robot()
    
    if maximum distance is 100 
        return distance = -1 and angle found = -1
    else 
        return distance and angle

function findGoldenToken()

    initialize distance at 100
    for each token that can seen by Robot()
        if the token have a value of the distance that is less than 100 
            && token is a golden token 

            than the distance is the distance between the found token and the robot

        the angle between token and robot is set equal to the angle of robot and token seen by Robot()
    
    if maximum distance is 100 
        return distance = -1 and angle found = -1
    else 
        return distance and angle

function seeWalls()

    initialize distance at 100
    for each token that can seen by Robot()
        if the token have a value of the distance that is less than 100 
            && token is a silver token 
            && the angle between robot and token is less than 100 and more than 70
            && the angle between robot and token is less than -70 and more than -100

            than the distance is the distance between the found token and the robot

        the angle between token and robot is set equal to the angle of robot and token seen by Robot()
    
    if maximum distance is 100 
        return distance = -1 and angle found = -1
    else 
        return distance and angle


function keepMeInTrack(angle_golden)

    if there is a wall of golden tokens in front of the robot in the range 15 to -15 angle_golden
        see if near the robot there are other walls with seeWalls()

        if the angle_golden is positive 
            print "There is a wall at my right, I'm turning left"
            turn left with the function turn(speed, seconds)
        else
            print "There is a wall at my right, I'm turning rigth"
            turn right with the function turn(speed, seconds)           
    else if 
        the robot is not parallel to the walls it will left or right a bit
        with the function turn(speed, seconds)
    else 
        if none of the previous condition are satisfied the robot will go straight


function grabSilverToken(dist_golden, rot_y_golden, dist_silver, rot_y_silver):

    if the distance with the silver token is equal to -1
        print "I don't see any token, I'll continue with my route"
        and call the function to keep on moving the robot keepMeInTrack(angle_golden)
    if the distance with the silver token il less than d_th (0.4)
        print "Found the silver token!"
        if function grab() is true
            print "Grabbed!"
            turn right by 180 degrees the robot then drive forward
            with the function release(), the robot releases the token
            then drive backwards and turn left 180 degrees
        else
            print "Aww, I'm not close enough."
    else if angle_silver is between a_th(2.0) and -a_th(-2.0)
        print "Ah, that'll do."
        go straight with drive(speed, seconds)
    else if 
        the robot is not well aligned with the token, we move it on the left if angle_silver is less than -a_th or we move it on the right if the angle_silver is more than a_th

function main()
    while true
        set dist_golden, rot_y_golden equal to the values returned by findGoldenToken()
        set dist_silver, rot_y_silver equal to the values returned by findSilverToken()

        if distance of the golden token is less than the distance of the silver token with robot && the distance of the silver token is more than 0.75
            we call keepMeInTrack(angle_golden)
        else
            the robot is near a silver token so it will go to grab it with
            grabSilverToken(dist_golden, angle_golden, dist_silver, angle_silver)

```
----------------------------------------------------------------------

## Possible Improvements


 - Using golden tokens to align the robot with the silver token so that it turns perfectly a 180 degrees
 - The functions findGoldenToken() and findSilverToken() can be sticked togheter (It gave me some problems doing that, so I preferred to have a code that was working good, rather than having bugs)
