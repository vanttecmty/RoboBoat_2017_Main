import os
import sys
import serial
import serial.tools.list_ports as ports

previousRightMotorValue = 0;
previousLeftMotorValue = 0;

baudRateArduino = 115200
baudRateIMU 	= 115200
baudRateRPLidar = 115200

lidarPort   = ''
imuPort     = ''
arduinoPort = ''
arduinoUnoPort = ''
arduinoMega = ''

servoLeft = 'l'
servoRight = 'r'
servoBoth = 'b'
servoMoveLeft = 180
servoMoveRight = 0
servoMoveInitP = 90

thrusterLeft = 'l'
thrusterRight = 'r'
thrustersBack = 'b'
thrustersFront = 'f'
thrustersAll = 'a'
thrusterMoveFront = 1650 #Min 1500 Max 1900
thrusterMoveBack  = 1350 #Min 1499 Max 1100
thrusterMoveInitP = 1500 

##Motors Information
numberOfMotors    = 2
numberOfBatteries = 2

maxSpeed = 9.8

boatWeight = 25 #Kg

currChallenge = 'N'

pts = list(ports.comports());

if not pts:
	print ('Theres no connected sensors')
else:
	for p in pts :
		print(p, p[1])
		if (p[1].find('ACM') == 3):
			arduinoUnoPort = p[0]
		elif (p[1].find('Serial') == 7):
			arduinoPort = p[0]
		elif (p[1].find('3-3') == 0 or p[1].find('3-4') == 0 or p[1].find('Silicon Labs CP2102 USB to UART') == 0 or p[1].find('CP2102') == 0 ):
			lidarPort = p[0]; 
		elif (p[1].find('USB-RS232') == 0) :
			imuPort = p[0];
		elif (p[1].find('USB2.0-Serial') == 0) :
			ardionoMega = p[0];


#ser = serial.Serial('/dev/ttyACM1', baudRateArduino);

#ser = serial.Serial('/dev/ttyACM0', baudRateArduino);
 
'''
if(arduinoMega != ''):
	ser = serial.Serial(arduinoMega, baudRateArduino )	

elif(arduinoPort != ''):
	ser = serial.Serial(arduinoUnoPort, baudRateArduino)

elif(arduinoUnoPort != ''):
	ser = serial.Serial(arduinoPort, baudRateArduino)
'''
