import os
import io
import sys
import xbee
import time
import threading
#import lib.bluetoothServer as bt
#import lib.auvsiServerCommunication as auvsi

#Manage Drone Kill Switch
#Manage Boat Remote Kill Switch
class XBeeThread(threading.Thread):
	def __init__(self, threadID,name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		while True:
			print("XBEE")
			global data
			x = xbee.xbee('/dev/ttyUSB0');
			data = x.receive_from_boat().split(',');
			x.send2boat('000000000'.encode());
			print(data[0]);
			

'''
' Inicio del Programa
'''
xbThread 	 = XBeeThread(1,"XBeeThread");
xbThread.start();
xbThread.join();
print("Thread Joined")

if __name__ == '__main__':
	init()