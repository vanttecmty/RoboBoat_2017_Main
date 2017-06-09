import math
import sys
import os
sys.path.append('/usr/local/lib/python3.4/dist-packages/vnpy')
from vnpy import *
from inspect import getmembers
from pprint import pprint
import lib.variables as var

'''
	Last version: 08-June-2017, Marcopolo Gil Melchor.
	******************************************************************
	Imu Controller.
	This file has all the necesary functions to access the imu for the
	autonomous navigation, such as position, orientation, velocity,
	acceleration, etc.
	******************************************************************

	Functions:

		** init imu module connection **
			params: 
				None
			return:
				 None
			call:
				imu.init()

		** get gps coordenates **
			params: 
				None
			return:
				dynamic array  = {
					float longitud
					float latitude
				}
			call:
				get_gps_coords(); 

		** get yaw (absolute orientation) **
			params: 
				None
			return:
				float degree
			call:
				get_yaw_orientation

		** get gps velocity and acceleration **
			params: 
				None
			return:
				dynamic array  = {
					vec3f acceleration
					vec3f velocity
				}
			call:
				get_gps_acceleration_velocity
		
		** get gps acceleration **
			params: 
				None
			return:
				vec3f acceleration
			call:
				get_gps_acceleration

		** get angular rate **
			params: 
				None
			return:
				dynamic array  = {
					float x
					float y
					float z
				}
			call:
				get_angular_rates

		** get acceleration **
			params: 
				None
			return:
				vec3f unit acceleration
			call: 
				get_acceleration

		** delta theta angles**
			desc: 
				Gives the rotation angles since last request
				(Relative orientation) 
			params:
				None
			return
				dynamic array  = {
					float x
					float y
					float z
				}
			call:
				get_delta_theta

		** delta velocity** NOT TESTED
			desc: 
				Gives the relative velocity 
			params:
				None
			return
				dynamic array  = {
					float x
					float y
					float z
				}
			call:
				get_delta_velocity
	***
'''
####################
#	CONSTANTES     #
####################
NORTH_YAW = 87.35199737548828;
vnSensor = None

def init():
	global vnSensor;
	vnSensor = VnSensor();
	vnSensor.connect(var.imuPort, 115200);

def print_model():
	return vnSensor.read_model_number();

def get_num_satellites():
	return vnSensor.read_gps_solution_lla().num_sats;

def get_gps_coords():
	lla = vnSensor.read_gps_solution_lla();
	'''
	'gps_fix', 'lla', 'ned_acc', 'ned_vel', 'num_sats', 'speed_acc', 'this', 'time', 'time_acc', 'week'
	'''
	return {
		'latitude': lla.lla.x,
		'longitud': lla.lla.y
	};

def get_yaw_orientation():
	return vnSensor.read_yaw_pitch_roll().x%360;

def get_gps_acceleration_velocity():
	lla = vnSensor.read_gps_solution_lla();

	return {
		'acceleration': lla.ned_acc,
		'velocity': lla.ned_vel
	}

def get_angular_rates():
	angles = vnSensor.read_angular_rate_measurements();

	return {
		'x': angles.x%360,
		'y': angles.y%360,
		'z': angles.z%360,
	}

def get_acceleration():
	return vnSensor.read_acceleration_measurements();

def get_delta_theta():
	angles = vnSensor.read_delta_theta_and_delta_velocity().delta_theta;

	return {
		'x': angles.x%360,
		'y': angles.y%360,
		'z': angles.z%360,
	}

def get_delta_velocity():
	return vnSensor.read_delta_theta_and_delta_velocity().delta_velocity;


def get_degrees_to_north_orientation():
	degree = (get_yaw_orientation()%360) - NORTH_YAW;

	if (degree > 180):
		degree = degree - 360;

	return degree;

def get_degrees_to_gps_coords(latitude2, longitud2):
	north = (get_yaw_orientation()%360) - NORTH_YAW;

	if (north > 180):
		north = north - 360;

	coords = get_gps_coords();
	longitud_distance = (coords['longitud'] - longitud2);
	y_distance = math.sin(longitud_distance) * math.cos(latitude2);
	x_distance = math.cos(coords['latitude']) * math.sin(latitude2) - math.sin(coords['latitude']) * math.cos(latitude2) * math.cos(longitud_distance);
	bearing = math.atan2(y_distance, x_distance);
	bearing = math.degrees(bearing) + north;
	bearing = (bearing + 360) % 360;

	if (bearing > 180):
		bearing = bearing - 360;

	return bearing;