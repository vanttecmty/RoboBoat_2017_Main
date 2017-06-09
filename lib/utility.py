import sys
import os
import lib.variables as var
import serial.tools.list_ports as ports

#Function that find which por has every component
#Store them on the global variables file located on lib
def get_serial_ports():
	pts = list(ports.comports())
	if not pts:
		print ('Theres no connected sensors')
	else:
		for p in pts :
			if (p[1].find('CP2102') == 6) :
				var.lidarPort = p[0] 
			elif (p[1].find('USB-RS232') == 0) :
				var.imuPort = p[0] 
			elif (p[1].find('ACM') == 3):
				var.arduinoUnoPort = p[0]
			elif (p[1].find('Serial') == 7):
				var.arduinoPort = p[0]


def print_serial_ports():
	pts = list(ports.comports())
	if not pts:
		print ('Theres no connected sensors')
	else:
		for p in pts :
			print(p)
			print(p[1].find('Serial') == 7)


def check_value_size(val):
	if(len(val) == 3):
		return val
	elif(len(val) == 2):
		return '0'+val
	elif(len(val) == 1):
		return '00'+val
	