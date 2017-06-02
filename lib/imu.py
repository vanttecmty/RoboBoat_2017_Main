import sys
import os
sys.path.append('/usr/local/lib/python3.4/dist-packages/vnpy')
from vnpy import *
import lib.variables as var


#Initialize IMU classes objects
vnSensor = VnSensor()
compData = CompositeData()
attitude = Attitude()
packet = Packet()


def print_model():
	if(var.imuPort == ''):
		print('Error : GetSerialPort must be called before this function')
	else:
		vnSensor.connect(var.imuPort, 115200)
		model = vnSensor.read_model_number()
		print(model)
		vnSensor.disconnect()

def test_function():
	vnSensor.connect(var.imuPort,115200)
	print("Yaw , Pitch , Roll" , vnSensor.read_yaw_pitch_roll())
	print("Attitude Quaternion " , vnSensor.read_attitude_quaternion())
	#print("Quat, Magn Acc, Angular " ,vnSensor.read_quaternion_magnetic_acceleration_and_angular_rates())
	print("Magn Measurements ", vnSensor.read_magnetic_measurements())
	print("Acc Measurements  ", vnSensor.read_acceleration_measurements())
	print("Ang rates Measurements ", vnSensor.read_angular_rate_measurements())
	#print("Mag acc and Ang rates", vnSensor.read_magnetic_acceleration_and_angular_rates())
	#print("Mag and Grav Ref Vec" , vnSensor.read_magnetic_and_gravity_reference_vectors())
	vnSensor.disconnect()

def open_communication():
	if(var.imuPort == ''):
		print('Error : GetSerialPort must be called before this function')
	else:
		vnSensor.connect(var.imuPort, 115200)


def close_communication():
		vnSensor.disconnect()

'''
def get_acceleration():
	if(vnSensor.is_connected()):
		return vnSensor.read_acceleration_measurements()
	else:
		print("VnSensor Is not connected")

def get_angular():
	if(vnSensor.is_connected()):
		return vnSensor.read_angular_rate_measurements()
	else:
		print("VnSensor Is not connected")
'''