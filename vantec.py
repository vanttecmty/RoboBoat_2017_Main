import os
import sys
import threading
import time
import math
import socket  

class RoboBoatServerThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		print("End RoboBoatServerThread");

class XBeeThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		print("End RoboBoatServerXBeeThread");

'''
' Inicio del programa
'''
init();
# Create new threads
thread1 = RoboBoatServerThread(1, "RoboBoatServerThread");
thread2 = XBeeThread(2, "XBeeThread");

# Start new Threads
thread1.start();
thread2.start();
thread1.join();
thread2.join();

print ("Exiting Main Thread");