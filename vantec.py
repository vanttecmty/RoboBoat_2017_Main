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
			lidarMeasures = lidar.test();
			routeMap = emptyMap.copy();

			for i in range(0, 90):
				if lidarMeasures[i] != 0:
					#print(i, lidarMeasures[i]);
					coord_x = LIDAR_COORD_X + int (math.cos(math.radians(i - 90)) * lidarMeasures[i] / 25);
					coord_y = LIDAR_COORD_Y + int (math.sin(math.radians(i - 90)) * lidarMeasures[i] / 25);
					cv2.circle(routeMap, (coord_x, coord_y), int(BOUY_RADIOUS + BOAT_WIDTH * 0.7), (255, 255 , 255), -1, 8);
					cv2.circle(routeMap, (coord_x, coord_y), BOUY_RADIOUS, (0, 0, 255), -1, 8);		

			for i in range(270, 359):
				if lidarMeasures[i] != 0:
					#print(i -360, lidarMeasures[i]);
					coord_x = LIDAR_COORD_X + int (math.cos(math.radians(i - 90)) * lidarMeasures[i] / 25);
					coord_y = LIDAR_COORD_Y + int (math.sin(math.radians(i - 90)) * lidarMeasures[i] / 25);
					cv2.circle(routeMap, (coord_x, coord_y), int(BOUY_RADIOUS + BOAT_WIDTH * 0.7), (255, 255 , 255), -1, 8);
					cv2.circle(routeMap, (coord_x, coord_y), BOUY_RADIOUS, (0, 0, 255), -1, 8);

			'''lidar.lidar.stop();
			routePoints = pathfinding.a_star([int(MAP_WIDTH/2), int(MAP_HEIGHT/2)],[10, 10], routeMap);

			for point in routePoints:
				routeMap[point[0]][point[1]] = [0, 0, 255];
			'''
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
		imu.get_magnetic_measurments();

init();
lidar.open_communication();
#imu.get_magnetic_measurments();
# Create new threads
thread0 = LidarThread(0, "LidarThread");
thread1 = MapThread(1, "MapThread");
thread2 = NavigationThread(2, "NavigationThread");
#thread9 = PathFindingThread(9, "PathFindingThread");
#thread3 = imuThread(3, "imuThread");

# Start new Threads
thread0.start();
thread1.start();
thread2.start();
#thread3.start();
thread0.join();
thread1.join();
thread2.join();
#thread3.join();
print ("Exiting Main Thread");