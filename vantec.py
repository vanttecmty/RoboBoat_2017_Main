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

emptyMap       = None;
routeMap       = None;
boatMap        = None;
lidar_ready    = False;
start_time     = time.time();
routePoints    = [];
lidarObstacles = [];
orientationDegree = 0;
coordsGoal     = [0,0];

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

class LidarSocketThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		global lidarObstacles;
		s = socket.socket();
		s.bind(("localhost", 8893));
		s.listen(1);
		sc, addr = s.accept();
		  
		while cv2.waitKey(1) != 27:
		    message = sc.recv(2000);

		    if message == "quit":  
		        break        

		    strMeasures = message.decode('utf-8');
		    arrMeasures = strMeasures.split(";");

		    if(len(arrMeasures) > 0):
		    	lidarObstacles = arrMeasures;
		    	lidarObstacles.pop();

		print("adios");  
		sc.close();  
		s.close();

class MapThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		global routeMap, orientationDegree;
		capture = cv2.VideoCapture(0);

		if(capture.isOpened() == False):
			print("No hay cámara");
			return -1;
		else:
			print("cámara encendida");

		while cv2.waitKey(1) != 27:			
			routeMap = emptyMap.copy();

			'''
			'Set lidar obstacles in the map 
			''' 
			for measure in lidarObstacles:
				data = measure.split(",");
				degree = int(data[0]);
				if( (degree > 0 and degree < 90) or degree > 270 and degree < 360):
					coord_x = LIDAR_COORD_X + int (math.cos(math.radians(degree - 90)) * float(data[1]) / 25);
					coord_y = LIDAR_COORD_Y + int (math.sin(math.radians(degree - 90)) * float(data[1]) / 25);
					cv2.circle(routeMap, (coord_x, coord_y), int(BOUY_RADIOUS + BOAT_WIDTH * 0.7), (255, 255 , 255), -1, 8);
					cv2.circle(routeMap, (coord_x, coord_y), BOUY_RADIOUS, (0, 0, 255), -1, 8);

			'''
			'Set camera obstacles in the map 
			'''
			frame = capture.read();
			cv2.imshow('cam', frame[1]);
			values = dbscan.get_obstacles(frame[1],'yg', False);
			camObstacles = values[1];

			for obstacle in camObstacles:
				coord_x = LIDAR_COORD_X + int (math.cos(math.radians(obstacle[1] - 90)) * float(obstacle[0]) / 25);
				coord_y = LIDAR_COORD_Y + int (math.sin(math.radians(obstacle[1] - 90)) * float(obstacle[0]) / 25);
				cv2.circle(routeMap, (coord_x, coord_y), int(BOUY_RADIOUS + BOAT_WIDTH * 0.7), (255, 255 , 255), -1, 8);
				cv2.circle(routeMap, (coord_x, coord_y), BOUY_RADIOUS, (0, 0, 255), -1, 8);
				pass;

			routePoints = pathfinding.a_star([int(MAP_WIDTH/2), int(MAP_HEIGHT/2)],coordsGoal, routeMap);
			routeLenght = len(routePoints);

			for point in routePoints:
				routeMap[point[0]][point[1]] = [0, 0, 255];
				pass;
			
			add_boat(routeMap);	
			cv2.imshow('Route', routeMap);


			if(routeLength > 40):
				coord_x = routePoints[-40][0];
				coord_y = routePoints[-40][1];
				orientation = math.atan2(MAP_HEIGHT / 2 - coord_y, MAP_WIDTH / 2 - coord_x);
				orientationDegree = math.degree(orientation);
			else: 
				orientationDegree = 0;

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
		turn_degrees_accum = 0;

		while cv2.waitKey(1) != 27:
			#print(imu.compass());
			imu_angle = imu.get_delta_theta()['z']%360;

			if (imu_angle > 180):
				imu_angle = imu_angle - 360;

			print("Desire: ", orientationDegree);
			print("Imu: ", imu_angle);
			turn_degrees_accum += imu_angle;
			left_turn_degrees = orientationDegree + turn_degrees_accum;
			print("Left: ", left_turn_degrees);
			motors.thrusters_front(left_turn_degrees, 0);
			#motors.thrusters_back(0);
			pass;

class TestThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		capture = cv2.VideoCapture(0);

		if(capture.isOpened() == False):
			print("No hay cámara");
			return -1;
		else:
			print("cámara encendida");

		while cv2.waitKey(1) != 27:
			frame = capture.read();
			cv2.imshow('cam', frame[1]);
			cv2.waitKey(0);
			values = dbscan.get_obstacles(frame[1],'yg', True);
			print (values[1]);
			cv2.imshow('Obsta', values[0]);
			pass;
init();
#imu.get_magnetic_measurments();
# Create new threads
thread0 = LidarSocketThread(1, "LidarSocketThread");
thread1 = MapThread(2, "MapThread");
#thread2 = NavigationThread(3, "NavigationThread");
#thread3 = TestThread(3, "TestThread");

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
