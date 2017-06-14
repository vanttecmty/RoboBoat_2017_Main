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
from scipy import misc
from scipy.ndimage import rotate
import lib.variables as var
import lib.motors as motors
import lib.lidar as lidar
import lib.imu as imu
import Jetson.dbscan_contours as dbscan

#Navigation class
MAP_WIDTH       = 400;
MAP_HEIGHT      = 400;
BOUY_RADIOUS    = 6;
LIDAR_RADIOUS   = 1;
BOAT_HEIGHT     = 58;
BOAT_WIDTH      = 34;
BOAT_X1         = int(MAP_WIDTH/2 - BOAT_WIDTH/2);
BOAT_Y1         = int(MAP_HEIGHT/2 - BOAT_HEIGHT/2);
BOAT_X2         = int(MAP_WIDTH/2 + BOAT_WIDTH/2);
BOAT_Y2         = int(MAP_HEIGHT/2 + BOAT_HEIGHT/2);
LIDAR_COORD_X   = 200;
LIDAR_COORD_Y   = int(200 - BOAT_HEIGHT / 2);
LIDAR_EXIT_FLAG = False;

emptyMap       = None;
routeMap       = None;
boatMap        = None;
lidar_ready    = False;
start_time     = time.time();
routePoints    = [];
lidarMeasures  = []; 

def new_map(rows, cols):
	mapa = np.full((rows, cols, 3),0, dtype = np.uint8);
	return mapa;

def add_boat(mapa):
	cv2.circle(mapa, (LIDAR_COORD_X, LIDAR_COORD_Y), LIDAR_RADIOUS, (255,255,255), -1, 8);
	cv2.rectangle(mapa,(BOAT_X1, BOAT_Y1),(BOAT_X2, BOAT_Y2), (0,255,0), 1, 8);	

def init():
	global emptyMap
	global routeMap;
	emptyMap = new_map(MAP_WIDTH, MAP_HEIGHT);
	routeMap = emptyMap.copy();

class LidarThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		global lidar_ready;
		lidar_ready = True;
		lidar.init();

class MapThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		global lidarMeasures;
		global routeMap;

		while cv2.waitKey(1) != 27:
			#lidarMeasures = lidar.test();
			f = open('lidar_measures.txt','r', os.O_NONBLOCK);
			lidarMeasures = f.readlines();			
			#print (lidarMeasures);
			routeMap = emptyMap.copy();

			for measure in lidarMeasures:
				data = measure.split(",");
				degree = int(data[0]);
				if( (degree > 0 and degree < 90) or degree > 270 and degree < 360):
					coord_x = LIDAR_COORD_X + int (math.cos(math.radians(degree - 90)) * float(data[1]) / 25);
					coord_y = LIDAR_COORD_Y + int (math.sin(math.radians(degree - 90)) * float(data[1]) / 25);
					cv2.circle(routeMap, (coord_x, coord_y), int(BOUY_RADIOUS + BOAT_WIDTH * 0.7), (255, 255 , 255), -1, 8);
					cv2.circle(routeMap, (coord_x, coord_y), BOUY_RADIOUS, (0, 0, 255), -1, 8);

			f.close();
			routePoints = pathfinding.a_star([int(MAP_WIDTH/2), int(MAP_HEIGHT/2)],[10, 10], routeMap);

			for point in routePoints:
				routeMap[point[0]][point[1]] = [0, 0, 255];
			
			add_boat(routeMap);	
			cv2.imshow('Route', routeMap);
			#lidar.lidar.start();

		lidar.lidar.stop_motor();
		lidar.lidar.disconnect();

class PathFindingThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		#global routePoints;
		print("hola");
		while cv2.waitKey(1) != 27:
			#print("hola");
			mapa = routeMap.copy();

			routePoints = pathfinding.a_star([int(MAP_WIDTH/2), int(MAP_HEIGHT/2)],[10, 10], mapa);

			for point in routePoints:
				routeMap[point[0]][point[1]] = [0, 0, 255];

			add_boat(mapa);	
			cv2.imshow('Route', mapa);

class NavigationThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		imu.init();
		imu.get_delta_theta();
		imu.get_delta_theta();
		turn_degrees_accum = 0;
		capture=cv2.VideoCapture(4)
		while True:
			#print(imu.compass());
			frame = capture.read()
			#print (frame)
			cv2.imshow('cam',frame[1])
			cv2.waitKey(0)
			values=dbscan.get_obstacles(frame[1])
			print (values)
			#cv2.imshow('Obsta',values[0])
			#print (values[1])
			turn_degrees_accum += imu.get_delta_theta()['z'];

			left_turn_degrees = degrees_to_turn - turn_degrees_accum;

			if(left_turn_degrees < 10):
				motors.turn_right();
			elif(left_turn_degrees > 10):
				motors.turn_left();

			#motors.move_servo(left_turn_degrees);
			#motors.move_thrusters_back();
			#motors.move_thrusters_front();

			pass;

init();
#degrees_to_turn = 45;
lidar.open_communication();
#imu.get_magnetic_measurments();
# Create new threads
thread0 = LidarThread(1, "LidarThread");
thread1 = MapThread(2, "MapThread");
#thread2 = NavigationThread(3, "NavigationThread");
#thread3 = imuThread(3, "imuThread");

# Start new Threads
thread0.start();
thread1.start();
#thread2.start();
#thread3.start();
thread0.join();
thread1.join();
#thread2.join();
#thread3.join();
print ("Exiting Main Thread");
