import sys
import time
import serial
import lib.variables as var
import lib.utility as utility
##############Motor Directions and Defaults #############
######## Turn Servos 0 - 180 __ Middle pos = 90  ########
######## Thrusters   1100 to 1900 Stopped = 1500 ########
##############Motor Directions and Defaults #############

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

def move(powerR=0,powerL=0):
	if(powerR < -400 or powerR > 400 or powerL < -400 or powerL > 400):
		print("The power is not on the correct range");
	else:
		realPowerValueR = round(powerR + 1500);
		realPowerValueL = round(powerL + 1500);
		move_thrusters(realPowerValueR, realPowerValueL);


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
