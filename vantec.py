import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import threading
import time
import math
import numpy as np
import cv2
import random
from scipy import misc
from scipy.ndimage import rotate
import lib.variables as var
import lib.motors as motors
import lib.lidar as lidar
import lib.imu as imu

#Navigation class
MAP_WIDTH     = 400;
MAP_HEIGHT    = 400;
BOUY_RADIOUS  = 6;
LIDAR_RADIOUS = 1;
BOAT_HEIGHT   = 58;
BOAT_WIDTH    = 34;
BOAT_X1       = int(MAP_WIDTH/2 - BOAT_WIDTH/2);
BOAT_Y1       = int(MAP_HEIGHT/2 - BOAT_HEIGHT/2);
BOAT_X2       = int(MAP_WIDTH/2 + BOAT_WIDTH/2);
BOAT_Y2       = int(MAP_HEIGHT/2 + BOAT_HEIGHT/2);
LIDAR_COORD_X = 200;
LIDAR_COORD_Y = 200 - BOAT_HEIGHT / 2;
LIDAR_EXIT_FLAG = False;

boat_map = None;

def new_map(rows, cols):
	mapa = np.full((rows, cols, 3),0, dtype = np.uint8)
	return mapa

def add_lidar_obstacles(mapa):
	medidas = lidar.test();

	for i in range(0, 90):
   		if medidas[i] != 0:
   			coord_x = LIDAR_COORD_X + int (math.cos(math.radians(i - 90)) * medidas[i] / 25);
   			coord_y = LIDAR_COORD_Y + int (math.sin(math.radians(i - 90)) * medidas[i] / 25);
   			cv2.circle(mapa, (coord_x, coord_y), BOUY_RADIOUS, (255,255,255), -1, 8);

	for i in range(270, 359):
		if medidas[i] != 0:
			coord_x = LIDAR_COORD_X + int (math.cos(math.radians(i - 90)) * medidas[i] / 25);
			coord_y = LIDAR_COORD_Y + int (math.sin(math.radians(i - 90)) * medidas[i] / 25);
			cv2.circle(mapa, (coord_x, coord_y), BOUY_RADIOUS, (255,255,255), -1, 8);

def add_boat(mapa):
	cv2.circle(mapa, (LIDAR_COORD_X, LIDAR_COORD_Y), LIDAR_RADIOUS, (255,255,255), -1, 8);
	cv2.rectangle(mapa,(BOAT_X1, BOAT_Y1),(BOAT_X2, BOAT_Y2), (0,255,0), 1, 8);

def init():
	global boat_map;
	boat_map = new_map(MAP_WIDTH, MAP_HEIGHT);
	add_boat(boat_map);

class lidarThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self);
      self.threadID = threadID;
      self.name = name;
   def run(self):
   	lidar.init();

class navigationThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self);
      self.threadID = threadID;
      self.name = name;
   def run(self):
      init(); 

      while cv2.waitKey(1) != 27:
         lidar_map = boat_map.copy();
         add_lidar_obstacles(lidar_map);
         cv2.imshow('mapa',lidar_map);
      
      lidar.lidar.stop();
      lidar.lidar.stop_motor();
      lidar.lidar.disconnect();

class imuThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self);
      self.threadID = threadID;
      self.name = name;
   def run(self):
      imu.init();

      while cv2.waitKey(1000) != 27:
         #print(imu.get_yaw_orientation());
         #print(imu.get_magnetic_and_gravity_reference().mag_ref);
         #print(imu.get_magnetic_and_gravity_reference().acc_ref);
         print(imu.get_magnetic_measurments());
         #print(imu.vnSensor.read_yaw_pitch_roll_magnetic_acceleration_and_angular_rates().mag);
         


         #print(imu.get_delta_theta());
         #degrees  = imu.get_degrees_to_gps_coords(25.649864, -100.290795);
         #distance = imu.get_distance_to_gps_coords(25.649864, -100.290795);
         #print(degrees, distance);

# Create new threads
#thread1 = lidarThread(1, "lidarThread");
#thread2 = navigationThread(2, "navigationThread");
thread3 = imuThread(3, "imuThread");

# Start new Threads
#thread1.start();
#thread2.start();
thread3.start();
#thread1.join();
#thread2.join();
thread3.join();
print ("Exiting Main Thread");