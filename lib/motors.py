'''
	@author Juan
'''
import sys
import time
import serial
import lib.variables as var
import lib.utility as utility
##############Motor Directions and Defaults #############
######## Turn Servos 0 - 180 __ Middle pos = 90  ########
######## Thrusters   1100 to 1900 Stopped = 1500 ########
##############Motor Directions and Defaults #############

minRotationS = 300 #rev/min
maxRotationS = 300 #rev/min

maxPowerValue = 1900;
minPowerValue = 1100;

powerR = 0 ; 
powerL = 0 ;

thrusterInitPosition = 1500
thrustersBack  = 'b'
thrustersFront = 'f'
servoInitPosition = 90

def move_thrusters(powerR=1500,powerL=1500):
	if(powerR < 1100 or powerR > 1900 or powerL < 1100 or powerL > 1900):
		print("Thruster power must be between 1100 - 1900");
	else:
		pR = str(powerR);
		pR = utility.check_value_size(pR);
		pL = str(powerL);
		pL = utility.check_value_size(pL);
		val = '%' + 'B,' + pR + ',' + pL + '%';
		var.ser.write(val.encode())
		var.ser.flush()
		print(var.ser.read(var.ser.inWaiting()).decode())

def move(powerR=0,powerL=0):
	if(powerR < -400 or powerR > 400 or powerL < -400 or powerL > 400):
		print("The power is not on the correct range");
	else:
		realPowerValueR = round(powerR + 1500);
		realPowerValueL = round(powerL + 1500);
		
		move_thrusters(realPowerValueR,realPowerValueL);
		#while(var.previousLeftMotorValue != powerL or var.previousRightMotorValue != powerR):
		#	checkDifference(powerR, powerL);
		
'''
def powerControl(power):
	for i in range(63,0):
		
	return 0;

def turnControl(power):
	
	return 0;
'''

def checkDifference(currPowerR,currPowerL):
	threshold = 0.025 * (maxPowerValue - minPowerValue );

	#Get the difference between the current power and the last one
	diffL = abs(currPowerL - var.previousLeftMotorValue);
	diffR = abs(currPowerR - var.previousRightMotorValue);

	#Check were the direction is going
	# 1 = Increase Power
	#-1 = Decrease Power
	if(diffL != 0): 
		directionL = (currPowerL - var.previousLeftMotorValue)  / diffL ;
	else:
		directionL = 0;
	if(diffR != 0): 
		directionR = (currPowerR - var.previousRightMotorValue) / diffR ;
	else:
		directionR = 0;

	if(diffR > threshold and diffL > threshold ):
		#Increase Right Motor Power
		if(directionR > 0):
			var.previousRightMotorValue += threshold;
		#Decrease Right Motor Power
		elif(directionR < 0):
			var.previousRightMotorValue -= threshold;
		
		#Increase Left Motor Power
		if(directionL > 0):
			var.previousLeftMotorValue += threshold;
		#Decrease Left Motor Power
		elif(directionL < 0):
			var.previousLeftMotorValue -= threshold;

		realPR = int(var.previousRightMotorValue)+int(thrusterInitPosition);
		realPL = int(var.previousLeftMotorValue) +int(thrusterInitPosition);
		
		#print(realPR,realPL);
		move_thrusters(realPR,realPL);
		time.sleep(0.125);
			
	elif(diffR > threshold and diffL < threshold):
		if(directionR > 0):
			var.previousRightMotorValue += threshold;
		#Increase
		elif(directionR < 0):
			var.previousRightMotorValue -= threshold;

		var.previousLeftMotorValue = currPowerL;

		realPR = int(var.previousRightMotorValue)+int(thrusterInitPosition);
		realPL = int(var.previousLeftMotorValue) +int(thrusterInitPosition);
		
		#print(realPR,realPL);
		move_thrusters(realPR,realPL);
		time.sleep(0.125);
		
	elif(diffR < threshold and diffL > threshold):
		#Increase
		if(directionL > 0):
			var.previousLeftMotorValue += threshold;
		#Decrease
		elif(directionL < 0):
			var.previousLeftMotorValue -= threshold;

		realPR = int(var.previousRightMotorValue)+int(thrusterInitPosition);
		realPL = int(var.previousLeftMotorValue) +int(thrusterInitPosition);
		
		#print(realPR,realPL);
		move_thrusters(realPR,realPL);
		time.sleep(0.125);
	else:
		var.previousLeftMotorValue  = currPowerL;
		var.previousRightMotorValue = currPowerR;
		
		realPR = int(var.previousRightMotorValue)+int(thrusterInitPosition);
		realPL = int(var.previousLeftMotorValue) +int(thrusterInitPosition);

		#print(realPR,realPL);
		move_thrusters(realPR,realPL);
		time.sleep(0.125);


'''
def move_thrusters_right(power=1500):
	if(power < 1100 or power > 1900):
		print("Thruster power must be between 1100 - 1900");
	else:
		p = str(power);
		p = utility.check_value_size(p);
		val = '%' + 'R,' + p + '%';
		var.ser.write(val.encode())
		var.ser.flush()
		print(var.ser.read(var.ser.inWaiting()).decode())
		
def move_thrusters_left(power=1500):
	if(power < 1100 or power > 1900):
		print("Thruster power must be between 1100 - 1900");
	else:
		p = str(power);
		p = utility.check_value_size(p);
		val = '%' + 'L,' + p + '%';
		var.ser.write(val.encode())
		var.ser.flush()
		print(var.ser.read(var.ser.inWaiting()).decode())

def move_left(power=0):
	if(power < -400 or power > 400):
		print("The power is not on the correct range");
	else:
		realPowerValue = round(power + 1500);
		move_thrusters_left(realPowerValue);

def move_right(power=0):
	if(power < -400 or power > 400):
		print("The power is not on the correct range");
	else:
		realPowerValue = round(power + 1500);
		move_thrusters_right(realPowerValue);


#All these functions if side = 1 left if side = 0 right
def turn_90(side):
	if(side):
		move_thrusters_left(0);
	else:
		move_thrusters_right(0);

def turn_60(side):
	if(side):
		move_thrusters_left(0);
	else:
		move_thrusters_right(0);

def turn_45(side):
	if(side):
		move_thrusters_left(0);
	else:
		move_thrusters_right(0);

def turn_30(side):
	if(side):
		move_thrusters_left(0);
	else:
		move_thrusters_right(0);
'''