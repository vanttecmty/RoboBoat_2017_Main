import os
import sys
import tty
import time
import termios
import lib.variables as var
import lib.utility as utility
import lib.motors as motors

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
testServosMode2 = False

while  x != chr(27) :
	x = sys.stdin.read(1)#[0]
	if(x == 'm' or x == 'M'):
		print("Manual Mode");
		autonomousMode = False;
		manualMode = True;
		testServosMode = False;
		testServosMode2 = False;
	if(x == 'x' or x == 'X'):
		print("Autonomous Mode");
		autonomousMode = True;
		manualMode = False;
		testServosMode = False;
		testServosMode2 = False;
	if(x == 'v' or x == 'V'):
		print("Test Servo Mode");
		autonomousMode = False;
		manualMode = False;
		testServosMode = True;
		testServosMode2 = False;
	if(x == 'z' or x == 'Z'):
		autonomousMode = False;
		manualMode = False;
		testServosMode = False;
		testServosMode2 = True;

	if(manualMode):
		# 0 Izquierda 
		if(x == 'a' or x == 'A'):
			#print("Turn Left");
			motors.move_left(50);
		# 180 Derecha
		if(x == 'd' or x == 'D'):
			#print("Turn Right");
			motors.move_right(50);
		# 1900 Adelante
		if(x == 'w' or x == 'W'):
			#print("Forward");
			motors.move_both(50)
		# 1100 Reversa
		if(x == 's' or x == 'S'):
			#print("Backward");
			motors.move_both(-50);
		if(x == 'q' or x == 'Q'):
			#print("Stop Motors")
			motors.move_both(0);

	elif(autonomousMode):
		if(x == 'P'):
			print("Autonomous Mode");

	elif(testServosMode):
		if(x == 'l'  or x == 'L'):
			print("Left");
			motors.move_servos(0);
		if(x == 'j'  or x == 'J'):
			print("Right");
			motors.move_servos(180);
		if(x == 'k'  or x == 'K'):
			print("Init Pos");
			motors.move_servos(90);

	elif(testServosMode2):
		#motors.move_servos(90);		
		motors.move_servos(30);

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    


