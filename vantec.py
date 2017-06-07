import os
import sys
import tty
import time
import termios
import lib.imu as imu
import lib.lidar as lidar
import lib.variables as var
import lib.utility as utility
import lib.motors as motors
import lib.navigation as navigation

'''
A = 65
W = 87
S = 83
D = 68
'''

orig_settings = termios.tcgetattr(sys.stdin)

tty.setraw(sys.stdin)
x = 0

while x != chr(27): # ESC

	x = sys.stdin.read(1)#[0]
	y = 'a'
	if(x == 'A' or x == 'a'):
		print("Turn Left")
	if(x == 'D' or x == 'd'):
		print("Turn Right")
	if(x == 'W' or x == 'w'):
		print("Forward")
	if(x == 'S' or x == 's'):
		print("Backward")

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    

#motors.test_motors(var.servoBoth, 128 , 128)

<<<<<<< HEAD
=======
utility.get_serial_ports()
#motors.open_communication()
#motors.test_motors('b', 128 , 128)
imu.test_function()
#motors.open_communication()
#motors.move_thrusters(var.rightThruster, 1400)
#motors.move_servo(var.leftServo, 120)
>>>>>>> 0eba302e11f69993342d906be6c2e71977201b5b
