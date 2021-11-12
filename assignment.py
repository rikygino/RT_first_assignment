#
#
#
# Coded by Riky (Riccardo Gjini)
#
#
# The aim of the program is to help the robot to do not crush on the walls going count-clockwise,
# also it's going to pick every single silver token and put it behind itself while he is mapping
# a way of the route, trying to stay in parallel with the walls
#
#
#
#


from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0  # float: Threshold for the control of the linear distance

d_th = 0.4  # float: Threshold for the control of the orientation

R = Robot()  # instance of the class Robot



def drive(speed, seconds):
    #
    # Function for setting a linear velocity
    # 
    # Args: speed (int): the speed of the wheels
	# seconds (int): the time interval
    # 
    # 

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    #
    # Function for setting an angular velocity
    #
    # Args: speed (int): the speed of the wheels
	# seconds (int): the time interval
    #
    #

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def findSilverToken():
    #
    # Function to find the closest silver token
    #
    # Returns:
	# dist (float): distance of the closest silver token (-1 if no silver token is detected)
	# rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    #
    #

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.rot_y < 88 and token.rot_y > -88:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	    return -1, -1
    else:
   	    return dist, rot_y

def findGoldenToken():
    #
    # Function to find the closest golden token
    #
    # Returns:
	# dist (float): distance of the closest golden token (-1 if no golden token is detected)
	# rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    #
    #
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	    return -1, -1
    else:
   	    return dist, rot_y


def seeWalls():
    #
    # Function to find the closest golden token in two ranges
    #
    # Returns:
	# dist (float): distance of the closest golden token (-1 if no golden token is detected)
	# rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    #
    #

    dist=100
    for token in R.see(): 
        # Only the distances of the golden token that are found in this two ranges will be evaluated 
        # so that the robot will know where to go and do not crush on the walls
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and ((token.rot_y > -100 and token.rot_y < -70) or (token.rot_y < 100 and token.rot_y > 70)): 
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	    return -1, -1
    else:
   	    return dist, rot_y
           

def keepMeInTrack(rot_y_golden):

    # This function is used to mantain a certain distance from the walls 
    # when are seen by the robot in order to stay in track with the route

    if rot_y_golden < 15 and rot_y_golden > -15: 
        # If the robot sees walls in front of it, it will map the walls around itself and choose the opposite way
        dist_golden, rot_y_golden = seeWalls()
        if(rot_y_golden > 0):
            print("There is a wall at my right, I'm turning left")
            turn(-15, 1)
        else:
            print("There is a wall at my left, I'm turning right")
            turn(15, 1)
    elif rot_y_golden < 80 and rot_y_golden > 0: # if the robot is not parallel to the walls it will left or right a bit
        print("I should left a bit...")
        turn(-5, 0.2)
    elif rot_y_golden > -80 and rot_y_golden < 0:
        print("I should right a bit...")
        turn(5, 0.2)
    else:
        print("Going straight forward")
        drive(25,0.5)


def grabSilverToken(dist_golden, rot_y_golden, dist_silver, rot_y_silver):
    if dist_silver==-1: # if no token is detected, we make the robot analyze again the map so that it can manage to choose a way
        print("I don't see any token, I'll continue with my route")
        keepMeInTrack(rot_y_golden)
    if dist_silver<d_th: # if we are close to the token, we try grab it.
        print("Found the silver token!")
        if R.grab(): # if we grab the token, the robot put the token behind itself, and then we go back to the initial position
            print("Grabbed!")
            turn(29.5, 2)
            drive(8,2)
            R.release()
            drive(-10,2)
            turn(-29.5,2)
        else:
            print("Aww, I'm not close enough.")
    elif -a_th <= rot_y_silver <= a_th: # if the robot is well aligned with the token, we go forward
        print("Ah, that'll do.")
        drive(20, 0.5)
    elif rot_y_silver < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y_silver > a_th:
        print("Right a bit...")
        turn(+2, 0.5)


def main():
    while 1:
        # The robot is going to analyze how many golden and silver token are near it
        # and then decide where to go by using the distances and rotation angles returned
        # by this two functions
        dist_golden, rot_y_golden = findGoldenToken()
        dist_silver, rot_y_silver = findSilverToken()
        # IF: the distance between the robot and the golden token is lower than 
        # the distance with the silver token the robot will follow the route 
        if(dist_golden < dist_silver and dist_silver > 0.75): 
            keepMeInTrack(rot_y_golden)
        else:
            #ELSE: the robot is near a silver token so it will go to grab it
            grabSilverToken(dist_golden, rot_y_golden, dist_silver, rot_y_silver)


main()