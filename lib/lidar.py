import os
import sys
import time
import numpy as np
import lib.variables as var
from rplidar import RPLidar 

lidar_measures = [];

def open_communication():
	lidar = RPLidar(var.lidarPort);
	lidar.connect();

def close_communication():	
	lidar = RPLidar(var.lidarPort);
	lidar.stop();
	lidar.stop_motor();
	lidar.disconnect();

def init_lidar():
	open_communication();

	for i in range(360):
       lidar_measures.append(0);

def print_RPLidar():
	if(var.lidarPort == ''):
		print('Error : utility.get_serial_ports() must be called before this function');
	else :
		lidar = RPLidar(var.lidarPort);
		lidar.connect();
		print(lidar.get_info());
		lidar.stop();
		lidar.stop_motor();
		lidar.disconnect();

def print_measurements():
	lidar = RPLidar(var.lidarPort);
	lidar.connect();
	measurements = lidar.iter_measurments()
	print(line = '\t'.join(str(v) for v in measurements));
	print(measurements);
	lidar.stop()
	lidar.stop_motor()
	lidar.disconnect()

def get_measurements():
	lidar = RPLidar(var.lidarPort)
	lidar.connect()
	try:
		print('Recording Measurements ... Press ctrl+c to stop')
		for measurements in lidar.iter_measurments():
			line = '\t'.join(str(v) for v in measurments)
			print(line+'\n')
	except KeyboardInterrupt:
		print('Stopping')
	lidar.stop()
	lidar.stop_motor()
	lidat.disconnect()