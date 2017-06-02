import sys
import serial
import lib.utility as utility
import lib.variables as var

##############Motor Directions and Defaults #############
######## Turn Servos 0 - 180 __ Middle pos = 90  ########
######## Thrusters   1100 to 1900 Stopped = 1500 ########
##############Motor Directions and Defaults #############

#RFT = Right Front Thruster
#LFT = Left  Front Thruster
#RBT = Right Back  Thruster
#LBT = Left  Back  Thruster

#Stopped Value

RFT = 1500 
LFT = 1500
RBT = 1500
LBT = 1500

#RS = Right Servomotor
#LS = Left  Servomotor

#Middle Position
RS = 90
LS = 90

def open_communication():
	if(var.arduinoPort!= ''):
		ser = serial.Serial(var.arduinoPort)
	else:
		print("Please Call the get_serial_ports routine")

def print_motor_port():
	print(var.arduinoPort)

#Servo could be l = left , r = right or b = both
#value1 and value2 are the values of the servos from 0 to 180
def move_servos(servo,value1=90,value2=90):
	if(value1 < 0 or value1 > 180 or value2 < 0 or value2 > 180):
		print("Not a valid value")
		return None

	if(servo == 'l'):
		val = 'S,' + servo + ',' + str(value1)
		ser.write(val)
		ser.flush()
	elif(servo == 'r'):
		val = 'S,' + servo + ',' + str(value1)
		ser.write(val)
		ser.flush()
	elif(servo == 'b'):
		val = 'S,' + servo + ',' + str(value1) + ',' + str(value2)
		ser.wrtie(val)
		ser.flush()
	else:
		print("That isnt a recognize servo")
		return None

#Thruster could be l = left , r = right or b = both
#value1 and value2 are the values of the servos from 0 to 180
#Forward from 1501 to 1900
#Backward from 1100 to 1499
def move_thrusters(thruster,value1=1500, value2=1500, value3=1500, value4=1500):
	#utility.get_serial_ports()
	#ser = serial.Serial(var.arduinoPort)
	
	if(value1 < 1100 or value1 > 1900 or value2 < 1100 or value2 > 1900):
		print("Not a valid value")
		return None
	##Need to complete the functions
	#Move Left Thrusters
	if(thruster == 'l'):
		val = 'T,' + thruster + ',' + str(value1)
		ser.write(val)
		ser.flush()
	#Move Right Thrusters
	elif(thruster == 'r'):
		val = 'T,' + thruster + ',' + str(value1)
		ser.write(val)
		ser.flush()
	#Move Back Trhusters
	elif(thruster == 'b'):
		val = 'T,' + thruster + ',' + str(value1) + ',' + str(value2)
		ser.write(val)
		ser.flush()
	#Move Front Trhusters
	elif(thruster == 'f'):
		val = 'T,' + thruster + ',' + str(value1) + ',' + str(value2)
		ser.write(val)
		ser.flush()
	#Move all thrusters
	elif(thruster == 'a'):
		val = 'T,' + thruster + ',' + str(value1) + ',' + str(value2) + ',' + str(value3) + ',' + str(value4)
		ser.write(val)
		ser.flush()
	else:
		print("That isnt a recognize servo")
		return None

#def thruster_left():

def test_horizonal_displacement(distance):
	# + Distance = Right displacement
	# - Distance = Left displacement
	if(distance > 0 ):
		move_servos(var.bothServos, 180 , 180)
	else :
		move_servos(var.bothServos, 0 , 0)
	if(distance > 0):
		move_thrusters(var.allThrusters, 1700 , 1700, 1700, 1700)
	elif(distance < 0):
		move_thrusters(var.allThrusters, 1300 , 1300, 1300, 1300)

def horizonal_displacement(distance):
	# + Distance = Right displacement
	# - Distance = Left displacement
	if(distance > 0 ):
		move_servos(var.bothServos, 180 , 180)
	else :
		move_servos(var.bothServos, 0 , 0)
	if(distance > 0):
		move_thrusters(var.allThrusters, 1700 , 1700, 1700, 1700)
	elif(distance < 0):
		move_thrusters(var.allThrusters, 1300 , 1300, 1300, 1300)

#Function to test the motors with the prototyped car
def test_motors(thruster,value1=0, value2=0):
	ser = serial.Serial(var.arduinoPort)

	if(value1 < 0 or value1 > 255 or value2 < 0 or value2 > 255):
		print("Not a valid value")
		return None
	##Need to complete the functions
	#Move Left Thrusters
	if(thruster == 'l'):
		val = 'T,' + thruster + ',' + str(value1)
		data=val.encode()
		ser.write(data)
		ser.flush()
	#Move Right Thrusters
	elif(thruster == 'r'):
		val = 'T,' + thruster + ',' + str(value1)
		data=val.encode()
		ser.write(data)
		ser.flush()
	#Move Back Trhusters
	elif(thruster == 'b'):
		val = 'T,' + thruster + ',' + str(value1) + ',' + str(value2)
		data=val.encode()
		ser.write(data)
		ser.flush()

def test_horizontal(direction):
	#Turn Right
	if(direction > 0): 
		test_motors('l', 128)
	#Turn Left
	elif(direction < 0):
		test_motors('r', 128)


def get_thrust(numBatteries=2):
	if(numBatteries == 1):
		print(var.stForwardMaxThrust14V)
		print(var.stReverseMaxTrhust14V)	
	elif(numBatteries ==2):
		print(var.twoBatForwardMaxThrust14V)
		print(var.twoBatReverseMaxTrhust14V)	
	elif(numBatteries == 3):
		print(var.threeBatForwardMaxThrust14V)
		print(var.threeBatReverseMaxTrhust14V)	
	elif(numBatteries == 4):
		print(var.fourBatForwardMaxThrust14V)
		print(var.fourBatReverseMaxTrhust14V)	

def get_max_acc(numBatteries=2):
	if(numBatteries == 1):
		print(var.stTopForwardAcc)
		print(var.stTopReverseAcc)	
	elif(numBatteries ==2):
		print(var.twoBatTopForwardAcc)
		print(var.twoBatTopBackwardAcc)	
	elif(numBatteries == 3):
		print(var.threeBatTopForwardAcc)
		print(var.threeBatTopBackwardAcc)	
	elif(numBatteries == 4):
		print(var.fourBatTopForwardAcc)
		print(var.fourBatTopBackwardAcc)	

def get_max_speed():
	print(var.maxSpeed)
