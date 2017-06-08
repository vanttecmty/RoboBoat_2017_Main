import sys
import time
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


thrusterMinRotationalSpeed = 300  #rev/min
thrusterMaxRotationalSpeed = 3800 #rev/min

thrusterOperatingVoltage = 14.8 #V

thrusterLength 		= 113 #mm
thrusterDiameter 	= 100 #mm
propellerDiameter 	= 76 #mm
thrusterWeightWater = 156 #g
thrusterWeightAir 	= 344 #g

#Single Thruster calculations
#st = Single Thruster
stFowardMaxThrust16V  = 5.1  #kgf
stReverseMaxThrust16V = 4.1  #kgf

stForwardMaxThrust12V  = 3.55 #kgf
stReverseMaxThrust12V = 3.0  #kgf

thrusterBatteryVoltage = 14.8

#Voltage of the battery = 14.8
stForwardMaxThrust14V = (thrusterBatteryVoltage * stFowardMaxThrust16V)  / 16  #kgf
stReverseMaxThrust14V = (thrusterBatteryVoltage * stReverseMaxThrust16V) / 16 #kgf

stTopForwardAcc  = (stForwardMaxThrust14V * 9.8 ) / var.boatWeight #m/s²
stTopBackwardAcc = (stReverseMaxThrust14V * 9.8) / var.boatWeight #m/s²

#Full Boat Calculations
##4 Batteries 1 each Motor
fourBatForwardMaxThrust = stForwardMaxThrust14V * 4 #kgf
fourBatBackwardMaxThrust= stReverseMaxThrust14V * 4 #kgf
fourBatTopForwardAcc	= (fourBatForwardMaxThrust * 9.8 ) / var.boatWeight 		#m/s²
fourBatTopBackwardAcc	= (fourBatBackwardMaxThrust * 9.8 ) / var.boatWeight     #m/s²

##2 Batteries
twoBatForwardMaxThrust  = (thrusterBatteryVoltage/2 * stFowardMaxThrust16V)  / 16 #kgf
twoBatBackwardMaxThrust = (thrusterBatteryVoltage/2 * stReverseMaxThrust16V) / 16 #kgf
twoBatTopForwardAcc		= (twoBatForwardMaxThrust  * 9.8 ) / var.boatWeight 		#m/s²
twoBatTopBackwardAcc 	= (twoBatBackwardMaxThrust * 9.8 ) / var.boatWeight 		#m/s²

##3 Batteries 1 For each rear thruster 1 for the two front thrusters
threeBatForwardMaxThrust = (stForwardMaxThrust14V  * 2) + twoBatForwardMaxThrust  	#kgf
threeBatBackwardMaxThrust= (stForwardMaxThrust14V * 2) + twoBatBackwardMaxThrust 	#kgf
threeBatTopForwardAcc	 = (threeBatForwardMaxThrust  * 9.8 ) / var.boatWeight 		#m/s²
threeBatTopBackwardAcc	 = (threeBatBackwardMaxThrust * 9.8 ) / var.boatWeight 		#m/s²

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
		var.ser.write(val.encode());
		var.ser.flush();
	elif(servo == 'r'):
		val = 'S,' + servo + ',' + str(value1)
		var.ser.write(val.encode());
		var.ser.flush();
	elif(servo == 'b'):
		val = 'S,' + servo + ',' + str(value1) + ',' + str(value2)
		var.ser.write(val.encode());
		var.ser.flush();
		#print(var.ser.read(len(val.encode())));
		#print(var.ser.read(1));


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
		var.ser.write(val.encode())
		var.ser.flush()
	#Move Right Thrusters
	elif(thruster == 'r'):
		val = 'T,' + thruster + ',' + str(value1)
		var.ser.write(val.encode())
		var.ser.flush()
	#Move Back Trhusters
	elif(thruster == 'b'):
		val = 'T,' + thruster + ',' + str(value1) + ',' + str(value2)
		var.ser.write(val.encode())
		var.ser.flush()
	#Move Front Trhusters
	elif(thruster == 'f'):
		val = 'T,' + thruster + ',' + str(value1) + ',' + str(value2)
		var.ser.write(val.encode())
		var.ser.flush()
	#Move all thrusters
	elif(thruster == 'a'):
		val = 'T,' + thruster + ',' + str(value1) + ',' + str(value2) + ',' + str(value3) + ',' + str(value4)
		var.ser.write(val.encode())
		var.ser.flush()
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
	if(value1 < 0 or value1 > 255 or value2 < 0 or value2 > 255):
		print("Not a valid value")
		return None
	##Need to complete the functions
	#Move Left Thrusters
	if(thruster == 'l'):
		val = 't,' + thruster + ',' + str(value1)
		var.var.ser.write(val.encode())
		var.var.ser.flush()
	#Move Right Thrusters
	elif(thruster == 'r'):
		val = 't,' + thruster + ',' + str(value1)
		var.var.ser.write(val.encode())
		var.var.ser.flush()
	#Move Back Trhusters
	elif(thruster == 'b'):
		val = 't,' + thruster + ',' + str(value1) + ',' + str(value2)
		var.var.ser.write(val.encode())
		var.var.ser.flush()
		readSize = len(val.encode())
		#print("Expecting Message of size " , len(val.encode()) , val.encode())
		print(var.var.ser.read(readSize))
		

def send_value(val):
	var.ser.write(val.encode())
	var.ser.flush()
	arduinoData = var.ser.read(len(val))
	return arduinoData


def test_horizontal(direction):
	#Turn Right
	if(direction > 0): 
		test_motors('l', 128)
	#Turn Left
	elif(direction < 0):
		test_motors('r', 128)


def get_thrust(numBatteries=2):
	if(numBatteries == 1):
		print(stForwardMaxThrust14V)
		print(stReverseMaxTrhust14V)	
	elif(numBatteries ==2):
		print(twoBatForwardMaxThrust14V)
		print(twoBatReverseMaxTrhust14V)	
	elif(numBatteries == 3):
		print(threeBatForwardMaxThrust14V)
		print(threeBatReverseMaxTrhust14V)	
	elif(numBatteries == 4):
		print(fourBatForwardMaxThrust14V)
		print(fourBatReverseMaxTrhust14V)	

def get_max_acc(numBatteries=2):
	if(numBatteries == 1):
		print(stTopForwardAcc)
		print(stTopReverseAcc)	
	elif(numBatteries ==2):
		print(twoBatTopForwardAcc)
		print(twoBatTopBackwardAcc)	
	elif(numBatteries == 3):
		print(threeBatTopForwardAcc)
		print(threeBatTopBackwardAcc)	
	elif(numBatteries == 4):
		print(fourBatTopForwardAcc)
		print(fourBatTopBackwardAcc)	

def get_max_speed():
	print(var.maxSpeed)
