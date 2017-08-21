'''
	@author Juan Carlos Aguilera
'''

import serial
import serial.tools.list_ports as ports

port = ''
pts = list(ports.comports())
if not pts:
	print ('Theres no connected sensors')
else:
	for p in pts :
		if (p[1].find('ACM') == 3):
			port = p[0]


ser = serial.Serial(port, baudrate = 9600, timeout = 1)

def getValues():
	val = b'S,b,180,180'
	ser.write(val)
	ser.flush()
	arduinoData = ser.read(len(val))
	return arduinoData

while(1):
	userInput = input('Get data point?')
	if userInput == 'y':
		print("Valores que entran a python :" , getValues())
