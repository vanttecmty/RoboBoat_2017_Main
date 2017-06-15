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

def move_thrusters_both(power=1500):
	if(power < 1100 or power > 1900):
		print("Thruster power must be between 1100 - 1900");
	else:
		p = str(power);
		p = utility.check_value_size(p);
		val = 'B,' + p + '%';
		var.ser.write(val.encode())
		var.ser.flush()

def move_thrusters_right(power=1500):
	if(power < 1100 or power > 1900):
		print("Thruster power must be between 1100 - 1900");
	else:
		p = str(power);
		p = utility.check_value_size(p);
		val = 'R,' + p + '%';
		var.ser.write(val.encode())
		var.ser.flush()
		
def move_thrusters_left(power=1500):
	if(power < 1100 or power > 1900):
		print("Thruster power must be between 1100 - 1900");
	else:
		p = str(power);
		p = utility.check_value_size(p);
		val = 'L,' + p + '%';
		var.ser.write(val.encode())
		var.ser.flush()

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

def move_both(power=0):
	if(power < -400 or power > 400):
		print("The power is not on the correct range");
	else:
		realPowerValue = round(power + 1500);
		move_thrusters_both(realPowerValue);


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

def move_left(power=0):
	if(power < -400 or power > 400):
		print("The power is not on the correct range");
	else:
		realPowerValue = power + 1500;
		move_thrusters(realPowerValue , thrustersBack);


def move_right(power=0):
	if(power < -400 or power > 400):
		print("The power is not on the correct range");
	elif(angle < -90 or angle > 90):
		print("The angle is not on the correct range");
	else:
		realPowerValue = round(power) + 1500;
		move_thrusters_left(realPowerValue , thrustersBack);



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

def move_servos(angle=servoInitPosition):
	if(angle < 0 or angle > 180):
		print("Not a correct angle");
	else:
		an = str(angle);
		an = utility.check_value_size(an);
		val = "S,x," + an + "%";
		print("Servo angle = ", val);
		var.ser.write(val.encode())
		var.ser.flush();
		print( var.ser.read( var.ser.inWaiting()).decode() );

#Possible thruster values b = back , f = front
def move_thrusters(power=thrusterInitPosition, thrusters='b'):
	if(power < 1100 or power > 1900):
		print("Thruster power must be between 1100 - 1900");
	else:
		if(thrusters == thrustersBack):
			p = str(power)
			p = utility.check_value_size(p)
			val = 'T,' + thrustersBack + ',' + p + '%' ;
			var.ser.write(val.encode())
			var.ser.flush()
			#print( var.ser.read( var.ser.inWaiting()).decode() );
		elif(thrusters == thrustersFront):
			p = str(power)
			p = utility.check_value_size(p)
			val = 'T,' + thrustersFront + ',' + p + '%' ;
			var.ser.write(val.encode())
			var.ser.flush()
			var.ser.read(var.ser.inWaiting())
			#print( var.ser.read( var.ser.inWaiting()).decode() );
			
	
def move_thrusters_2(power=thrusterInitPosition, thruster='b'):
	if(power < 1100 or power > 1900):
		print("Thruster power must be between 1100 - 1900");
	else:
		if(thruster == 'b'):
			p = str(power)
			p = utility.check_value_size(p)
			val = 'T,' + thruster + ',' + p + '%' ;
			var.ser.write(val.encode())
			var.ser.flush()
			#print( var.ser.read( var.ser.inWaiting()).decode() );
		elif(thruster == 'r'):
			p = str(power)
			p = utility.check_value_size(p)
			val = 'T,' + thruster + ',' + p + '%' ;
			var.ser.write(val.encode())
			var.ser.flush()
			#print( var.ser.read( var.ser.inWaiting()).decode() );
		elif(thruster == 'l'):
			p = str(power)
			p = utility.check_value_size(p)
			val = 'T,' + thruster + ',' + p + '%' ;
			var.ser.write(val.encode())
			var.ser.flush()
			#print( var.ser.read( var.ser.inWaiting()).decode() );


def turn_right():
	move_thrusters_2(1600,'r');
	move_thrusters_2(1400,'l');

def turn_left():
	move_thrusters_2(1600,'l');
	move_thrusters_2(1400,'r');

def thrusters_back(power=0):
	if(power < -400 or power > 400):
		print("The power is not on the correct range");
	else:
		realPowerValue = power + 1500;
		move_thrusters(realPowerValue , thrustersBack);


def thrusters_front(angle=0, power=0):
	if(power < -400 or power > 400):
		print("The power is not on the correct range");
	elif(angle < -90 or angle > 90):
		print("The angle is not on the correct range");
	else:
		realServoValue = 90 + round(angle)
		realPowerValue = round(power) + 1500;
		move_servos(realServoValue);
		move_thrusters(realPowerValue , thrustersBack);

'''