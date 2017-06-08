import sys
import os
sys.path.append('/usr/local/lib/python3.4/dist-packages/vnpy')
from vnpy import *
from inspect import getmembers
from pprint import pprint
import lib.variables as var

'''
	imu

	********************************

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
		
	***
'''
vnSensor = None
NORTH_YAW = 87.35199737548828;

def init():
	global vnSensor;
	vnSensor = VnSensor();
	vnSensor.connect(var.imuPort , 115200);

def print_model():
	return vnSensor.read_model_number();

def get_num_satellites():
	return vnSensor.read_gps_solution_lla().num_sats;

def get_gps_coords():
	lla    = vnSensor.read_gps_solution_lla();
	'''
	'gps_fix', 'lla', 'ned_acc', 'ned_vel', 'num_sats', 'speed_acc', 'this', 'time', 'time_acc', 'week'
	'''
	return {
		'latitude': lla.lla.x,
		'longitud': lla.lla.y
	};

def get_yaw_orientation():
	return vnSensor.read_yaw_pitch_roll().x;

def get_gps_acceleration_velocity():
	lla = vnSensor.read_gps_solution_lla();

	return {
		'acceleration': lla.ned_acc,
		'velocity': lla.ned_vel
	}

def get_angular_rates():
	return vnSensor.read_angular_rate_measurements();

def get_acceleration():
	return vnSensor.read_acceleration_measurements();

def get_delta_theta():
	return vnSensor.read_delta_theta_and_delta_velocity().delta_theta;

def get_delta_velocity():
	return vnSensor.read_delta_theta_and_delta_velocity().delta_velocity;


def get_degrees_to_north_orientation():
	degree = (get_yaw_orientation()%360) - NORTH_YAW;

	if (degree > 180):
		degree = degree - 360;

	return degree;