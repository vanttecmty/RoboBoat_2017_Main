'''
	@author Gabriel Sahagún
'''

import os
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import datetime
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
#import lib.variables as var
#import lib.motors as motors
import lib.imu as imu
import Jetson.dbscan_contours as dbscan
import serial

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
connection=[]

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

class MapThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;

	def new_map(self, rows, cols):
		mapa = np.full((rows, cols, 3),0, dtype = np.uint8);
		return mapa;

	def add_boat(self, mapa):
		cv2.rectangle(mapa,(BOAT_X1, BOAT_Y1),(BOAT_X2, BOAT_Y2), (0,255,0), 1, 8);	

	def run(self):
		global routeMap, orientationDegree;

		emptyMap = self.new_map(MAP_WIDTH, MAP_HEIGHT);
		routeMap = emptyMap.copy();

		while runProgram:
			'''
			routeMap = emptyMap.copy();

	
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
			

			frame = capture.read();
			#cv2.imshow('cam', frame[1]);
			date=str(datetime.datetime.now())
			name=date[:10]+'-'+date[11:19]
			print(name)
			cv2.imwrite('dataset/'+name+'.png',frame[1])

			foundRed,foundGreen,x,y,returned_image=autonomous.get_destination(image)
			cv2.imwrite('dataset_autonomous/'+name+'.png',returned_image)
			coordenadas=imu.get_gps_coords();
			yaw=imu.get_yaw_orientation();
			magnetic=imu.get_magnetic_measurments();

			leido=self.connection.read(2).decode("utf-8")
			
			if leido.find('a')!=-1:
				with open("waypoints.txt", "a")as myfile:
					myfile.write(str(coordenadas['longitud'])+','+str(coordenadas['latitude'])+'\n')

			#cv2.imwrite(name+'-map.png',routeMap)
			cv2.waitKey(500)


def init():
	global capture, connection;

	imu.init();
	capture = cv2.VideoCapture(0);
	connection=serial.Serial('/dev/ttyACM0',9600)

	if(capture.isOpened() == False):
		print("No hay cámara");
		return -1;
	else:
		print("cámara encendida");
z««««««««««««««««««««««««««««««
'''
' Inicio del programa
'''
init();
# Create new threads
#thread1 = LidarSocketThread(1, "LidarSocketThread");
thread2 = MapThread(2, "MapThread");

# Start new Threads
#thread1.start();
thread2.start();
#thread1.join();
thread2.join();


