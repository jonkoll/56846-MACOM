from __future__ import print_function

import time
from sr.robot import *


def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):  #positive clockwise
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_silver_token():
	dist = 100
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
			dist = token.dist
			rot_y = token.rot_y
	if dist == 100:
		return -1, -1
	else:
		return dist, rot_y

def find_gold_token():
	dist = 100
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
			dist = token.dist
			rot_y = token.rot_y
	if dist == 100:
		return -1, -1
	else:
		return dist, rot_y

def move_towards_silver_token(dist, rot_y, a_th, d_th):
	if dist == -1: 			#if no token has been found
		turn(+10, 1)
		return(False)
	elif dist < d_th:
		if R.grab():
			print("Grab successfull")
			return(True)	
		else:
			print("Grab disaster!!!")
			return(False)
	elif rot_y < -a_th: 
		turn(-2, 0.5)
		return(False)
	elif rot_y > a_th:
		turn(+2, 0.5)
		return(False)	
	else:
		drive(20, 0.2)
		return(False)

def move_towards_gold_token(dist, rot_y, a_th, d_th):
	if dist == -1: 		#if no token has been found
		turn(-10, 1)
		return(False)
	elif dist < d_th:
		if R.release():
			print("Release successfull")
			return(True)
		else:
			print("Release disaster!!!")
			return(False)
	elif rot_y < -a_th: 
		turn(-2, 0.5)
		return(False)
	elif rot_y > a_th:
		turn(+2, 0.5)
		return(False)	
	else:
		drive(20, 0.2)
		return(False)

def goto_silver():
	grabbed = False
	while grabbed == False:
		dist, rot_y = find_silver_token()
		grabbed = move_towards_silver_token(dist, rot_y, a_th_grab, d_th_grab)
	print("Silver token has been reached and grabbed")

def goto_gold():
	turn(-20, 1.5)		#initial turn to move towards correct gold token
	released = False
	while released == False:
		dist, rot_y = find_gold_token()
		released = move_towards_gold_token(dist, rot_y, a_th_release, d_th_release)
	print("Gold token has been reached, silver token released")
	turn(20, 1)			#turn away from released token to prevent repeated grabs
	drive(10, 0.5)


#------_______MAIN_______------#
#grab requirements
a_th_grab = 2.0
d_th_grab = 0.4

#release requirements
a_th_release = 2.0		
d_th_release = 0.6		


R = Robot()
tokens_sorted = 0

#due to starting position, first token requires special treatment
goto_silver()
turn(-20, 1)		
goto_gold()
tokens_sorted += 1

#loop through remaining five pairs of tokens
while tokens_sorted < 6:	
	goto_silver()
	goto_gold()
	tokens_sorted += 1
	print("Tokens sorted: ", tokens_sorted)
print("Mission accomplished")

#post-mission loop
while True:		    
	turn(30, 1.2)
	turn(-30, 1)
	print("WOOP WOOP")
#-------------------------------#
    
    
    
    
