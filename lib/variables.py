import os
import sys
import serial
import serial.tools.list_ports as ports

baudRateArduino = 9600
baudRateIMU = 115200
baudRateRPLidar = 115200

lidarPort   = ''
imuPort     = ''
arduinoPort = ''
arduinoUnoPort = ''

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

pts = list(ports.comports())
if not pts:
	print ('Theres no connected sensors')
else:
	for p in pts :
		print(p)
		if (p[1].find('CP2102') == 6) :
			imuPort = p[0] 
		elif (p[1].find('RS232') == 5) :
			lidarPort = p[0] 
		elif (p[1].find('ACM') == 3):
			arduinoUnoPort = p[0]
		elif (p[1].find('Serial') == 7):
			arduinoPort = p[0]
			
#Declared the communication variable of arduino serial
ser = serial.Serial(arduinoUnoPort, baudRateArduino)
