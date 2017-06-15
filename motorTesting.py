import os
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import threading
import time
import math
import numpy as np
import cv2
import random
import pathfinding 
import socket  
from scipy import misc
from scipy.ndimage import rotate
import lib.variables as var
import lib.motors as motors
import lib.imu as imu
import Jetson.dbscan_contours as dbscan

def navigation_init(self, threadID, name):
	threading.Thread.__init__(self);
	self.threadID = threadID;
	self.name = name;

def try_right(power):
	motors.move_right(100)
	motors.move_left(-100)

def try_left(power):
	motors.move_right(-100)
	motors.move_left(100)

curr = 0

def run():
	#imu.init();
	#imu.get_delta_theta();
	turn_degrees_accum = 0;
	start = time.gmtime()
	
	motors.move_both(0);

	while curr < 5:
		#print(imu.compass());
		#imu_angle = imu.get_delta_theta()['z']%360;
		#if(imu_angle > 180):
	#	imu_angle = imu_angle -360;

		#print(imu_angle);
		motors.move_left(0)
		motors.move_right(0)

		curr = time.gmtime() - start

	motors.move_both(0)

if __name__ == '__main__':
	run()