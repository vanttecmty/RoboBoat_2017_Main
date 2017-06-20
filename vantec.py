import os
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import threading
import time
import math
import numpy as np
import cv2
import random
import pathfindingv2 as pathfinding
import socket  
from scipy import misc
from scipy.ndimage import rotate
import lib.variables as var
import lib.motors as motors
import lib.imu as imu
import Jetson.dbscan_contours as dbscan

#Navigation class
MAP_WIDTH       = 200;#400
MAP_HEIGHT      = 200;
BOUY_RADIOUS    = 3;#6
BOAT_HEIGHT     = 58/2;#58
BOAT_WIDTH      = 34/2;#34
BOAT_X1         = int(MAP_WIDTH/2 - BOAT_WIDTH/2);
BOAT_Y1         = int(MAP_HEIGHT/2 - BOAT_HEIGHT/2);
BOAT_X2         = int(MAP_WIDTH/2 + BOAT_WIDTH/2);
BOAT_Y2         = int(MAP_HEIGHT/2 + BOAT_HEIGHT/2);
LIDAR_COORD_X   = 100;#200
LIDAR_COORD_Y   = int(100 - BOAT_HEIGHT / 2);#200

runProgram        = True;
capture           = None;
emptyMap          = None;
routeMap          = None;
boatMap           = None;
lidar_ready       = False;
start_time        = time.time();
destiny           = {'degree': 0, 'distance': 0};
destinyCoords     = [0,0];
routePoints       = [];
lidarObstacles    = [];
orientationDegree = 0;
pixelsGoal        = [0,0];

class LidarSocketThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		global lidarObstacles;
		s = socket.socket();
		s.bind(("localhost", 8895));
		s.listen(1);

		sc, addr = s.accept();
		  
		while runProgram:
		    message = sc.recv(2000);

		    if message == "quit":  
		        break        

		    strMeasures = message.decode('utf-8');
		    arrMeasures = strMeasures.split(";");

		    if(len(arrMeasures) > 0):
		    	lidarObstacles = arrMeasures;
		    	lidarObstacles.pop();

		sc.close();  
		s.close();
		print("End thread Socket");

class MapThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		global routeMap, orientationDegree;

		emptyMap = self.new_map(MAP_WIDTH, MAP_HEIGHT);
		routeMap = emptyMap.copy();

		while runProgram:
			routeMap = emptyMap.copy();

			'''
			'Set lidar obstacles in the map 
			''' 
			for measure in lidarObstacles:
				data = measure.split(",");
				#print(measure);
				degree = int(data[0]);
				distance = int(data[1]);

				if( (degree > 0 and degree < 90) or (degree > 270 and degree < 360) and distance > 1000):
					#pasar de milimetros a centimetros -> dividir entre 10
					pixelX = LIDAR_COORD_X + int (math.cos(math.radians(degree - 90)) * float(distance/10) / 5);
					pixelY = LIDAR_COORD_Y + int (math.sin(math.radians(degree - 90)) * float(distance/10) / 5);
					#print(pixelX, pixelY);
					cv2.circle(routeMap, (pixelX, pixelY), int(BOUY_RADIOUS + BOAT_WIDTH * 0.8), (255, 255 , 255), -1, 8);
					cv2.circle(routeMap, (pixelX, pixelY), BOUY_RADIOUS, (0, 0, 255), -1, 8);

			'''
			'Set camera obstacles in the map 
			'''
			frame = capture.read();
			#cv2.imshow('cam', frame[1]);
			cv2.waitKey(5);
			values = dbscan.get_obstacles(frame[1],'yg', False);
			camObstacles = values[1];

			for obstacle in camObstacles:
				#obstacle is [distance, degree]
				#print("cam obstacles");
				pixelX = LIDAR_COORD_X + int (math.cos(math.radians(obstacle[1] - 90)) * float(obstacle[0]) / 5);
				pixelY = LIDAR_COORD_Y + int (math.sin(math.radians(obstacle[1] - 90)) * float(obstacle[0]) / 5);
				cv2.circle(routeMap, (pixelX, pixelY), int(BOUY_RADIOUS + BOAT_WIDTH * 0.8), (255, 255 , 255), -1, 8);
				cv2.circle(routeMap, (pixelX, pixelY), BOUY_RADIOUS, (0, 0, 255), -1, 8);
				pass;

			#print("destiny", destiny);
			
			#print(destiny);
			#locate destiny pixels if is less than 8 meters.
			if(destiny['distance'] < 8):
				#escalar medidad de metros a centimetro -> multiplicar entre 100 
				destinyPixelX = LIDAR_COORD_X + int (math.cos(math.radians(destiny['degree'] + 90)) * float(destiny['distance'] *100) / 5);
				destinyPixelY = LIDAR_COORD_Y + int (math.sin(math.radians(destiny['degree'] + 90)) * float(destiny['distance'] *100) / 5);
				destinyPixel = [destinyPixelY, destinyPixelX];
			#locate destiny by orientation.
			else:
				#locate destiny in top border.
				if(math.fabs(destiny['degree']) < 45):
					destinyDistanceY = MAP_HEIGHT/2;
					destinyPixelY    = 0;
					destinyDistanceX = destinyDistanceY / math.tan(math.radians(destiny['degree'] + 90));
					#print("destinyDistanceX ", destinyDistanceX);
					destinyPixelX    = int(MAP_WIDTH/2 + destinyDistanceX);
					#print("destinyPixelX ", destinyPixelX);
					destinyPixel     = [destinyPixelY, destinyPixelX];
				#locate destiny in right border
				elif(destiny['degree'] < -45 and  destiny['degree'] > -135):
					destinyDistanceX = MAP_HEIGHT/2;
					destinyPixelX    = MAP_WIDTH - 1;
					destinyDistanceY = math.tan(math.radians(destiny['degree'] + 90)) * destinyDistanceX;
					destinyPixelY    = int(MAP_WIDTH/2 - destinyDistanceY);
					destinyPixel     = [destinyPixelY, destinyPixelX];
				#locate destiny in left border
				elif(destiny['degree'] > 45 and  destiny['degree'] < 135):
					destinyDistanceX = MAP_HEIGHT/2;
					destinyPixelX    = 0;
					destinyDistanceY = math.tan(math.radians(destiny['degree'] + 90)) * destinyDistanceX;
					destinyPixelY    = int(MAP_WIDTH/2 + destinyDistanceY);
					destinyPixel     = [destinyPixelY, destinyPixelX];
				#locate destiny in bottom border
				elif(math.fabs(destiny['degree']) > 135):
					destinyDistanceY = MAP_HEIGHT/2;
					destinyPixelY    = MAP_HEIGHT - 1;
					destinyDistanceX = destinyDistanceY / math.tan(math.radians(destiny['degree'] + 90));
					destinyPixelX    = int(MAP_WIDTH/2 + destinyDistanceX);
					destinyPixel     = [destinyPixelY, destinyPixelX];

			#print("destiny pixel: ", destinyPixel);
			cv2.imshow('Route', routeMap);
			#cv2.imwrite('route_test.png',routeMap)
			#Todo: check if destiny is inside obstacle;
			routePoints = pathfinding.a_star([int(MAP_WIDTH/2), int(MAP_HEIGHT/2)], destinyPixel, routeMap);
			routeLength = len(routePoints);

			for point in routePoints:
				routeMap[point[0]][point[1]] = [0, 0, 255];
				pass;

			if(routeLength > 40):
				pixelX = routePoints[-40][1];
				pixelY = routePoints[-40][0];
				#print("y=", pixelY, " x=", pixelX);
				orientation = math.atan2(MAP_HEIGHT / 2 - pixelY, pixelX - MAP_WIDTH / 2);
				orientationDegree = math.degrees(orientation) - 90;
			else: 
				orientationDegree = 0;
			#print("orientation degree mapa: ", orientationDegree);

			self.add_boat(routeMap);	
			cv2.imshow('Route', routeMap);
		time.sleep(1)

		print("End thread Map");

	def new_map(self, rows, cols):
		mapa = np.full((rows, cols, 3),0, dtype = np.uint8);
		return mapa;

	def add_boat(self, mapa):
		cv2.rectangle(mapa,(BOAT_X1, BOAT_Y1),(BOAT_X2, BOAT_Y2), (0,255,0), 1, 8);	

class NavigationThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name     = name;
	def run(self):
		global orientationDegree, destinyCoords;
		destinyCoords = [25.649529, -100.290430];
		self.go_to_destiny(25.649529, -100.290430);

	def go_to_destiny(self, latitude2, longitud2):
		global destiny, runProgram;
		destiny               = imu.get_degrees_and_distance_to_gps_coords(latitude2, longitud2);
		orientationDegree     = destiny['degree'];
		lastOrientationDegree = orientationDegree;
		turn_degrees_needed   = orientationDegree;
		turn_degrees_accum    = 0;
		#clean angle;
		imu.get_delta_theta();

		#Condition distance more than 2 meters. 
		while destiny['distance'] > 2 and runProgram:
			#print("orientation degrees", orientationDegree);
			if(lastOrientationDegree != orientationDegree):
				turn_degrees_needed = orientationDegree;
				turn_degrees_accum  = 0;

				#clean angle;
				imu.get_delta_theta();
				lastOrientationDegree = orientationDegree;

			#If same direction, keep route
			#while math.fabs(turn_degrees_needed) > 10:
			imu_angle = imu.get_delta_theta()['z']%360;

			if(imu_angle > 180):
				imu_angle = imu_angle -360;
			#print("grados imu: ", imu_angle);
			turn_degrees_accum += imu_angle;
			#print("grados acc: ", turn_degrees_accum);
			turn_degrees_needed = (orientationDegree + turn_degrees_accum)%360;

			if(turn_degrees_needed > 180): 
				turn_degrees_needed = turn_degrees_needed - 360;
			elif (turn_degrees_needed < 180):
				turn_degrees_needed = turn_degrees_needed + 360;
			#print("grados a voltear: ", turn_degrees_needed);

			if(math.fabs(turn_degrees_needed) < 5): 
				print("Tengo un margen menor a 5 grados");
				motors.move(100,100);
			else:
				#girar
				if(turn_degrees_needed > 0):
					print("Going to move left")
					motors.move(100,0);
				else: 
					print("Going to move right")
					motors.move(0,100);
			#ir derecho;
			#recorrer 2 metros
			destiny = imu.get_degrees_and_distance_to_gps_coords(latitude2, longitud2);
			runProgram = cv2.waitKey(1) != 27;
			time.sleep(1);

		print("End thread Navigation");
		
class TestThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		
		while cv2.waitKey(1) != 27:
			imu.get_magnetic_measurments();
			imu.get_yaw_orientation();
			pass;

def init():
	global capture;

	imu.init();
	capture = cv2.VideoCapture(1);

	if(capture.isOpened() == False):
		print("No hay cámara");
		return -1;
	else:
		print("cámara encendida");

'''
' Inicio del programa
'''
init();
# Create new threads
thread1 = LidarSocketThread(1, "LidarSocketThread");
thread2 = MapThread(2, "MapThread");
thread3 = NavigationThread(2, "NavigationThread");

# Start new Threads
thread1.start();
thread2.start();
thread3.start();
thread1.join();
thread2.join();
thread3.join();

print ("Exiting Main Thread");