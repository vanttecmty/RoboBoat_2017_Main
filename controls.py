import os
import sys
import tty
import time
import termios
import lib.variables as var
import lib.utility as utility
import lib.motors as motors
import lib.navigation as nav


'''
A = 65
W = 87
S = 83
D = 68 

Up = 38
Down = 40
Left = 37
Right = 39
'''

orig_settings = termios.tcgetattr(sys.stdin)

tty.setraw(sys.stdin)
x = 0
endProgram = False
manualMode = False
autonomousMode = False
testServosMode = False

while  x != chr(27) :
	x = sys.stdin.read(1)#[0]
	if(x == 'm' or x == 'M'):
		print("Manual Mode");
		autonomousMode = False;
		manualMode = True;
		testServosMode = False;
	if(x == 'x' or x == 'X'):
		print("Autonomous Mode");
		autonomousMode = True;
		manualMode = False;
		testServosMode = False;
	if(x == 'v' or x == 'V'):
		print("Test Servo Mode");
		autonomousMode = False;
		manualMode = False;
		testServosMode = True;

	if(manualMode):
		# 0 Izquierda 
		if(x == 'a' or x == 'A'):
			print("Turn Left");
			nav.move_left();
		# 180 Derecha
		if(x == 'd' or x == 'D'):
			print("Turn Right");
			nav.move_right();
		# 1900 Adelante
		if(x == 'w' or x == 'W'):
			print("Forward");
			nav.move_forward();
		# 1100 Reversa
		if(x == 's' or x == 'S'):
			print("Backward");
			nav.move_backward();
		#
		if(x == 'q' or x == 'Q'):
			print("Horizontal Movement Left");
			nav.move_horizontal_left();
		if(x == 'e' or x == 'E'):
			print("Horizontal Movement Right");
			nav.move_horizontal_right();


	elif(autonomousMode):
		if(x == 'P'):
			print("Autonomous Mode");

	elif(testServosMode):
		if(x == 'l'  or x == 'L'):
			print("Left");
			nav.move_left();
		if(x == 'j'  or x == 'J'):
			print("Right");
			nav.move_right();
		if(x == 'k'  or x == 'K'):
			print("Init Pos");
			nav.move_init_pos()
		

nav.move_init_pos()
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    


