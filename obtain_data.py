import datetime
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
			date=str(datetime.datetime.now())
			name='dataset/'+date[:10]+'-'+date[11:19]
			print(name)
			cv2.imwrite(name+'.png',frame[1])
			cv2.waitKey(5);
			values = dbscan.get_obstacles(frame[1],'rgby', False);
			camObstacles = values[1];

			coordenadas=imu.get_gps_coords()
			yaw=imu.get_yaw_orientation()
			magnetic=get_magnetic_measurments()
			with open("measurements.txt", "a") as myfile:
				myfile.write(name+','+coordeandas+','+yaw+','+magnetic)
			for obstacle in camObstacles:
				#obstacle is [distance, degree]
				#print("cam obstacles");
				pixelX = LIDAR_COORD_X + int (math.cos(math.radians(obstacle[1] - 90)) * float(obstacle[0]) / 5);
				pixelY = LIDAR_COORD_Y + int (math.sin(math.radians(obstacle[1] - 90)) * float(obstacle[0]) / 5);
				cv2.circle(routeMap, (pixelX, pixelY), int(BOUY_RADIOUS + BOAT_WIDTH * 0.8), (255, 255 , 255), -1, 8);
				cv2.circle(routeMap, (pixelX, pixelY), BOUY_RADIOUS, (0, 0, 255), -1, 8);
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

# Start new Threads
thread1.start();
thread2.start();
thread1.join();
thread2.join();;


