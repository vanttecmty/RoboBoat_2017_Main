'''
	vantec.py
    @desc 		Principal file for RoboBoat competition
   				Here are the principals threads to make the boat work.
	@author 	Marcopolo Gil Melchor marcogil93@gmail.com
	@created_at 2017-06-05
	@updated_at 2017-08-21
	@requires	python3
'''

'''
	Required python libraries 
'''
import os
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import threading
import time
import math
import numpy as np
import cv2
import random
import socket  
from scipy import misc
from scipy.ndimage import rotate
import datetime

'''
	Required project python libraries 
'''
import pathfindingv2 as pathfinding
import lib.variables as var
import lib.motors as motors
import lib.imu as imu
import Jetson.dbscan_contours as dbscan
import challenges as challenge


##############ADDED BY JC NEED TO BE TESTED#############
import lib.boat as boat
#Variable que se usará para poder cambiar los challenges
#Posibles valores : 
#'a' = "Autonomous"
#'d' = "Docking"
#'s' = "Speed"
#'N' = "Transitions"
#'r' = "Return"
#'e' = "End"
#'p' = "Path"
#'f' = "Follow"
var.currChallenge = 'N'
##############ADDED BY JC NEED TO BE TESTED#############

'''
	RADAR DIMENSION, OBJECTS SCALED SIZE, COORDENATES OF OBJECT CENTROIDES
	@desc The resolution of the radar is 10 meters.
'''
MAP_WIDTH       = 400;
MAP_HEIGHT      = 400;
BOUY_RADIOUS    = 6;
BOAT_HEIGHT     = 58;
BOAT_WIDTH      = 34;
BOAT_X1         = int(MAP_WIDTH/2 - BOAT_WIDTH/2);
BOAT_Y1         = int(MAP_HEIGHT/2 - BOAT_HEIGHT/2);
BOAT_X2         = int(MAP_WIDTH/2 + BOAT_WIDTH/2);
BOAT_Y2         = int(MAP_HEIGHT/2 + BOAT_HEIGHT/2);
LIDAR_COORD_X   = 100;
LIDAR_COORD_Y   = int(100 - BOAT_HEIGHT / 2);#200


#   courseDelta = 
#   courseAlfa  = 
#   cpurse
courseId          = 0;
runProgram        = True;
frame             = None;
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
alfaDockingLatitude    =  29.15168;
alfaDockingLongitud    = -81.01726;
bravoDockingLatitude   =  29.15208;
bravoDockingLongitud   = -81.01656;
charlieDockingLatitude =  29.15137;
charlieDockingLongitud = -81.01627;
#Xbee Variables
drone_takeoff = 0
drone_flying = 0
endOfTasks = 0

##############ADDED BY JC NEED TO BE TESTED#############
class sendXbeeThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		boat.start_mission()
##############ADDED BY JC NEED TO BE TESTED#############

class LidarSocketThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
	def run(self):
		global lidarObstacles, runProgram;
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

		    runProgram = cv2.waitKey(1) != 27;

		sc.close();  
		s.close();
		print("End thread Socket");

class MapThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;
		self.previous_map=np.array((MAP_HEIGHT,MAP_WIDTH),dtype=np.uint8)


	def join_maps(self):
		routeMap=np.bitwise_or(routeMap,self.previous_map)

	def translate_previous(self,dx,dy):
		cols,rows,ch=self.previous_map.shape
		M=np.float32([[1,0,dx],[0,1,dy]])
		self.previous_map=cv2.warpAffine(self.previous_map,M,(cols,rows))

	def run(self):
		global routeMap, orientationDegree, frame;

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

				if (degree > 0 and degree < 90) or (degree > 270 and degree < 360):
					#pasar de milimetros a centimetros -> dividir entre 10
					pixelX = LIDAR_COORD_X + int (math.cos(math.radians(degree - 90)) * float(distance/10) / 5);
					pixelY = LIDAR_COORD_Y + int (math.sin(math.radians(degree - 90)) * float(distance/10) / 5);
					#print(pixelX, pixelY);
					cv2.circle(routeMap, (pixelX, pixelY), int(BOUY_RADIOUS + BOAT_WIDTH * 0.8), (255, 255 , 255), -1, 8);
					cv2.circle(routeMap, (pixelX, pixelY), BOUY_RADIOUS, (0, 0, 255), -1, 8);

			'''
			'Set camera obstacles in the map 
			'''
			'''
			frame = capture.read();
			#cv2.imshow('cam', frame[1]);
			cv2.waitKey(100);
			if frame[0]:
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
			'''
			#print("destiny", destiny);
			
			#print(destiny);
			#locate destiny pixels if is less than 8 meters.
			'''
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
			#cv2.waitKey(100);
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
				cv2.circle(routeMap, (pixelX, pixelY), 2, (255, 255 , 255), -1, 8);
				#print("yy= ", MAP_HEIGHT / 2 - pixelY, "xx= ", pixelX - MAP_WIDTH / 2);
				orientation = math.atan2(MAP_HEIGHT / 2 - pixelY, pixelX - MAP_WIDTH / 2);
				#print("orientation= ", orientation);
				#orientationDegree = math.degrees(orientation) - 90;
			#else: 
				#orientationDegree = 0;
			#print("orientation degree mapa: ", orientationDegree);
			'''
			self.add_boat(routeMap);	
			cv2.imshow('Route', routeMap);
			cv2.waitKey(100);
			#time.sleep(1)
			#print("run5 ", runProgram);
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
		global orientationDegree, destinyCoords, frame;
		#destinyCoords = [29.190093, -81.050142];
		#self.go_to_destiny(29.190093, -81.050142);
		var.currChallenge = 'a';
		#self.challenge_1();
		#motors.move(50, 50);
		#time.sleep(2);
		#motors.move(0, 0);
		var.currChallenge = 'N';
		#curso muelle
		#self.go_to_destiny(29.15168, -81.017377);
		time.sleep(10);
		var.currChallenge = 'd';
		time.sleep(120);
		self.go_to_destiny(29.151322, -81.017508);

		while(boat.dockId == 0):
			time.sleep(1);

	def go_to_destiny(self, latitude2, longitud2):
		global destiny;
		destiny               = imu.get_degrees_and_distance_to_gps_coords(latitude2, longitud2);
		orientationDegree     = destiny['degree'];
		lastOrientationDegree = orientationDegree;
		turn_degrees_needed   = orientationDegree;
		turn_degrees_accum    = 0;
		#clean angle;
		imu.get_delta_theta();

		#Condition distance more than 2 meters. 
		while destiny['distance'] > 3 and runProgram:
			#print("degrees: ", imu.NORTH_YAW);
			#print("coords: ", imu.get_gps_coords());
			print("destiny: ", destiny);
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

			#threshold
			if(math.fabs(imu_angle) > 1):
				turn_degrees_accum += imu_angle;

			#print("grados acc: ", turn_degrees_accum);
			turn_degrees_needed = (orientationDegree + turn_degrees_accum)%360;

			if(turn_degrees_needed > 180): 
				turn_degrees_needed = turn_degrees_needed - 360;
			elif (turn_degrees_needed < -180):
				turn_degrees_needed = turn_degrees_needed + 360;
			
			#print("grados a voltear: ", turn_degrees_needed);

			if(math.fabs(turn_degrees_needed) < 10): 
				print("Tengo un margen menor a 10 grados");
				velocity = destiny['distance'] * 10;

				if (velocity > 300):
					velocity = 200;

				motors.move(velocity, velocity);
			else:
				#girar
				if(turn_degrees_needed > 0):
					print("Going to move left")
					motors.move(70, -70);
				else: 
					print("Going to move right")
					motors.move(-70, 70);
			#ir derecho;
			#recorrer 2 metros
			destiny = imu.get_degrees_and_distance_to_gps_coords(latitude2, longitud2);
			#time.sleep(1);


		motors.move(0,0);
		print("End thread Navigation");
	
	'''
	def challenge_2(self):
		global destiny, runProgram;
		ch1_image = capture.read();		
		cv2.imshow('frame', ch1_image[1]);
		cv2.waitKey(1);
		autonomous = challenge.Autonomous_Navigation();
		foundRed,foundGreen, centroideX, centroideY, image2 = autonomous.get_destination(ch1_image[1]);
		date=str(datetime.datetime.now())
		name=date[:10]+'-'+date[11:19]
		cv2.imwrite('postes/'+name+'.png',image)
		lastCentroideDegree = 0;
		centroideDegree = lastCentroideDegree;
		turn_degrees_needed = 0;
		turn_degrees_accum = 0;
		#clean angle;
		imu.get_delta_theta();
		LastCentroideY = centroideY;
		counter = 0;

		myFirstCoords = imu.get_gps_coords();
		ch1_destiny = {};
		ch1_destiny['distance'] = 0;

		while foundRed or foundGreen or counter < 100 or math.fabs(ch1_destiny['distance']) < 15:
			print("rojo ", foundRed, "verde ", foundGreen, "counter ", counter);
			centroideDegree = (centroideX * 69.0/680.0 - 35) * -1;

			if(foundRed and not foundGreen):
				print("solo rojo");
				centroideDegree = centroideDegree - 45;
			elif(not foundRed and foundGreen):
				print("solo  verde");
				centroideDegree = centroideDegree + 45;

			print("centroideDegree", centroideDegree);

			if(centroideDegree != lastCentroideDegree):
				turn_degrees_needed = centroideDegree;
				turn_degrees_accum  = 0;

				#clean angle;
				imu.get_delta_theta();
				lastCentroideDegree = centroideDegree;

			imu_angle = imu.get_delta_theta()['z']%360;

			if(imu_angle > 180):
				imu_angle = imu_angle -360;
			#print("grados imu: ", imu_angle);

			#threshold
			if(math.fabs(imu_angle) > 1):
				turn_degrees_accum += imu_angle;

			#print("grados acc: ", turn_degrees_accum);
			turn_degrees_needed = (lastCentroideDegree + turn_degrees_accum)%360;

			if(turn_degrees_needed > 180): 
				turn_degrees_needed = turn_degrees_needed - 360;
			elif (turn_degrees_needed < -180):
				turn_degrees_needed = turn_degrees_needed + 360;

			#print("grados a voltear: ", turn_degrees_needed);

			if(math.fabs(turn_degrees_needed) < 10): 
				print("Tengo un margen menor a 10 grados");
				motors.move(70, 70);
			else:
				#girar
				if(turn_degrees_needed > 0):
					print("Going to move left")
					motors.move(25, -25);
				else: 
					print("Going to move right")
					motors.move(-25, 25);
			
			#recorrer 2 metros
			ch1_image = capture.read();
			cv2.imshow('frame', ch1_image[1]);
			cv2.waitKey(1);

			if(LastCentroideY != centroideY):
				LastCentroideY = centroideY;

			foundRed,foundGreen, centroideX, centroideY, image2 = autonomous.get_destination(ch1_image[1]);
			date=str(datetime.datetime.now())
			name=date[:10]+'-'+date[11:19]
			cv2.imwrite('postes/'+name+'.png',image)
			cv2.imwrite('postes/'+name+'-found.png',image2)
			counter = (counter + 1)%1000000;
			ch1_destiny = imu.get_degrees_and_distance_to_gps_coords(myFirstCoords['latitude'], myFirstCoords['longitud']);
		
		motors.move(100, 100);
		time.sleep(2);
		motors.move(0, 0);
	'''

	def challenge_1(self):
		global destiny, runProgram;
		ch1_image = capture.read();		
		#cv2.imshow('frame', ch1_image[1]);
		cv2.waitKey(100);
		autonomous = challenge.Autonomous_Navigation();
		foundRed,foundGreen, centroideX, centroideY, image2 = autonomous.get_destination(ch1_image[1]);
		date=str(datetime.datetime.now())
		name=date[:10]+'-'+date[11:19]
		cv2.imwrite('postes/'+name+'.png',image2)
		lastCentroideDegree = 0;
		centroideDegree = lastCentroideDegree;
		turn_degrees_needed = 0;
		turn_degrees_accum = 0;
		#clean angle;
		imu.get_delta_theta();
		LastCentroideY = centroideY;
		counter = 0;

		myFirstCoords = imu.get_gps_coords();
		ch1_destiny = {};
		ch1_destiny['distance'] = 0;

		while foundRed or foundGreen or counter < 100 or math.fabs(ch1_destiny['distance']) < 10:
			print("rojo ", foundRed, "verde ", foundGreen, "counter ", counter);
			centroideDegree = (centroideX * 69.0/680.0 - 35) * -1;

			if(foundRed and not foundGreen):
				print("solo rojo");
				centroideDegree = centroideDegree - 20;
			elif(not foundRed and foundGreen):
				print("solo  verde");
				centroideDegree = centroideDegree + 20;

			print("centroideDegree", centroideDegree);

			if(centroideDegree != lastCentroideDegree):
				turn_degrees_needed = centroideDegree;
				turn_degrees_accum  = 0;
				#clean angle;
				imu.get_delta_theta();
				lastCentroideDegree = centroideDegree;

			imu_angle = imu.get_delta_theta()['z']%360;

			if(imu_angle > 180):
				imu_angle = imu_angle -360;
			#print("grados imu: ", imu_angle);

			#threshold
			if(math.fabs(imu_angle) > 1):
				turn_degrees_accum += imu_angle;

			#print("grados acc: ", turn_degrees_accum);
			turn_degrees_needed = (lastCentroideDegree + turn_degrees_accum)%360;

			if(turn_degrees_needed > 180): 
				turn_degrees_needed = turn_degrees_needed - 360;
			elif (turn_degrees_needed < -180):
				turn_degrees_needed = turn_degrees_needed + 360;

			#print("grados a voltear: ", turn_degrees_needed);

			if(math.fabs(turn_degrees_needed) < 10): 
				print("Tengo un margen menor a 10 grados");
				motors.move(100, 100);
			else:
				#girar
				if(turn_degrees_needed > 0):
					print("Going to move left")
					motors.move(50, -50);
				else: 
					print("Going to move right")
					motors.move(-50, 50);
			
			#recorrer 2 metros
			ch1_image = capture.read();
			#cv2.imshow('frame', ch1_image[1]);
			cv2.waitKey(200);

			if(LastCentroideY != centroideY):
				LastCentroideY = centroideY;

			foundRed,foundGreen, centroideX, centroideY, image2 = autonomous.get_destination(ch1_image[1]);
			date=str(datetime.datetime.now())
			name=date[:10]+'-'+date[11:19]
			cv2.imwrite('postes/'+name+'.png',image2)
			counter = (counter + 1)%1000000;
			ch1_destiny = imu.get_degrees_and_distance_to_gps_coords(myFirstCoords['latitude'], myFirstCoords['longitud']);
		
		#motors.move(100, 100);
		time.sleep(2);
		motors.move(0, 0);


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
	imu.NORTH_YAW = imu.get_yaw_orientation();
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
thread3 = NavigationThread(3, "NavigationThread");
thread4 = sendXbeeThread(4, "sendXbeeThread");

# Start new Threads
#thread1.start();
#thread2.start();
thread3.start();
thread4.start();

#thread1.join();
#thread2.join();
thread3.join();
thread4.join();

print ("Exiting Main Thread");