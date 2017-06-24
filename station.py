#Estación

#Comunicación del Serial independiende a la de Variable
#Esta comunicación es únicamente para la estación.

#Comunicación con el Bote a través de XBEE
#Establecer Comunicación con el Servidor de AUVSI
#Comunicarse con BT a la aplicación
#Leer Kill Switch del Bote
#Sí se puede saber del Kill Switch del Drone

import os
import io
import sys
import xbee 
import time
#import serial
import threading
from PIL import Image
from bluetooth import *
from array import array
import lib.bluetoothServer as bt
import lib.auvsiServerCommunication as auvsi

xb = xbee('/dev/ttyUSB0')

status = True
data = []
teamCode = "Tecnológico de Monterrey"
course = "courseA"
file = "image.jpg"

class readKillSwitches(threading.Thread):
	def __init__(self, threadID,name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;

	def run(self): 
		kill = x.read_kill_switch()
		if kill == "emergency":
			print("Abort Everything");

#Manage Drone Communication
class BTtransmission(threading.Thread):
	def __init__(self, threadID,name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;

	def run(self): 
		timestamp = data[0]

#Manage Drone Kill Switch
#Manage Boat Remote Kill Switch
class XBeeThread(threading.Thread):
	def __init__(self, threadID,name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		global data
		x = xbee.xbee('/dev/ttyUSB0');
		data = x.receive_from_boat().split('-');
		if(status):
			x.send2boat(str(status));

#Get XBee info and send it to AUVSI server
class AUVSICommunication(threading.Thread):
	def __init__(self, threadID,name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):		
		timestamp = data 

def send_heart_beat():
	timestamp = data[0];
	challenge = data[1];
	latitude  = data[2];
	longitude = data[3];
	stat = data[4];
	if(len(timestamp) > 14 or len(challenge) != 0 or len(latitude) < 11 or len(longitude) < 11):
		send_heart_beat();
	else:
		auvsi.send_heart_beat(course,timestamp,challenge,latitude,longitude);


def send_follow():
	if(	len(course > 4) ):
		gate = auvsi.send_follow_leader(course);
	else:
		send_follow();
		

def send_docking():
	if(len(course) > 4):
		imgID = auvsi.send_docking(course,file);
	else:
		send_docking()

def init():
	#Start sequence
	#Call XBee and read info
	
	'''
	while(status):
		if(challenge == 'docking'):
			send_docking();
		elif(challenge == 'follow'):
			gate = sendFollow();
		elif(challenge == 'return'):
			print("Return")
		sendHeartBeat();
	'''


'''
' Inicio del Programa
'''
xbThread 	 = XBeeThread(1,"XBeeThread");
#btTranThread = BTtransmission(2,"BTtransmission");
#AUVSIThread  = AUVSICommunication(3,"AUVSICommunication");  

#Start Threads
xbThread.start();
#btTranThread.start();
#AUVSIThread.start();

xbThread.join();
#btTranThread.join();
#AUVSIThread.join();


if __name__ == '__main__':
	init()

print("Exiting Main Thread");


