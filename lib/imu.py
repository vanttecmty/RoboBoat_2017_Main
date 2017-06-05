import sys
import os
sys.path.append('/usr/local/lib/python3.4/dist-packages/vnpy')
from vnpy import *
from inspect import getmembers
from pprint import pprint
import lib.variables as var


#Initialize IMU classes objects
vnSensor = VnSensor()
compData = CompositeData()
attitude = Attitude()
packet = Packet()
BOD = BinaryOutputRegister()


def print_model():
	if(var.imuPort == ''):
		print('Error : GetSerialPort must be called before this function')
	else:
		vnSensor.connect(var.imuPort, 115200)
		model = vnSensor.read_model_number()
		print(model)
		vnSensor.disconnect()
################################################################################
def test_function():
	#vnSensor.connect(var.imuPort,115200)
	ez = EzAsyncData.connect(var.imuPort, 115200)
	##COmando teórico: $VNWRG,75,2,16,01,7FFF*XX
	
	#ez.sensor.write_async_data_output_type(VNGPS)
	#ez.sensor.write_async_data_output_type(29)
	#print(ez.sensor.read_async_data_output_type())
	#cd = ez.current_data
	#pprint(getmembers(cd))
	#pprint(getmembers(ez.sensor.read_gps_solution_lla()))

	#print(BOD.async_mode)	
	imuMeasures        = ez.sensor.read_imu_measurements();
	deltaThetaVelocity = ez.sensor.read_delta_theta_and_delta_velocity();
	YawPitchRoll       = ez.sensor.read_yaw_pitch_roll();
	Qtn                = ez.sensor.read_attitude_quaternion();
	AngularRate        = ez.sensor.read_angular_rate_measurements();

	print(getmembers(ez.sensor.read_ins_solution_ecef()));
	#print(ez.sensor.read_angular_rate_measurements());
	#Con (22)
	#print(cd.has_any_position)
	#print("Any pos [deg,deg,m]: ",cd.any_position)
	#print(cd.has_yaw_pitch_roll)
	#print("YPR (Euler angles): ",cd.yaw_pitch_roll)
	#print(cd.has_any_attitude)
	#print("Any attitude (?):",cd.any_attitude)
	#print(cd.has_any_velocity)
	print("YPR (Euler angles): ", YawPitchRoll);
	print("Attitude Qtn (?): ", Qtn);
	print("Angular Rate  (rad/s): ", AngularRate);
	print("Delta vel (m/s): ", deltaThetaVelocity.delta_velocity);
	print("Imu Acc (m/s²): ", imuMeasures.accel);
	print("Imu Gyro (?): ", imuMeasures.gyro);
	print("Imu Mag (?): ", imuMeasures.mag);
	print("Imu Pressure (?): ", imuMeasures.pressure);
	print("Imu Temp (?): ", imuMeasures.temp);
	#Con (29) incluye todo en (22)
	#print(cd.has_any_acceleration)
	#print("Any Acc (m/s²): ",cd.any_acceleration)
	#print(cd.has_acceleration)
	#print("Acc (m/s²): ", imuMeasures.accel)
	#print(cd.has_any_angular_rate)
	#print("Any ang rate (rad/s): ",cd.any_angular_rate)
	#print(cd.has_angular_rate)
	#print("Ang rate (rad/s): ",cd.angular_rate)
	
	
	
	'''
	#Todo esto es lo que regresa false con la config actual (22) o (29)
	print("2",cd.has_quaternion)
	print("3",cd.has_direction_cosine_matrix)
	print("4",cd.has_any_magnetic)	
	print("7",cd.has_acceleration_linear_body)
	print("8",cd.has_acceleration_uncompensated)
	print("9",cd.has_acceleration_linear_ned)
	print("10",cd.has_acceleration_linear_ecef)
	print("11",cd.has_acceleration_ned)
	print("12",cd.has_acceleration_ecef)	
	print("15",cd.has_angular_rate_uncompensated)
	print("16",cd.has_any_pressure)	
	print("18",cd.has_position_gps_lla)	
	print(cd.has_temperature)
	print(cd.has_velocity_gps_ned)
	print(cd.has_delta_theta)
	print(cd.has_delta_velocity)
	'''
	
	print("")
	
	'''
	print("Yaw , Pitch , Roll" , vnSensor.read_yaw_pitch_roll())
	print("Attitude Quaternion " , vnSensor.read_attitude_quaternion())
	
	#print("Quat, Magn Acc, Angular " ,vnSensor.read_quaternion_magnetic_acceleration_and_angular_rates())
	print("Magn Measurements ", vnSensor.read_magnetic_measurements())
	print("Acc Measurements  ", vnSensor.read_acceleration_measurements())
	print("Ang rates Measurements ", vnSensor.read_angular_rate_measurements())
	#print("Mag acc and Ang rates", vnSensor.read_magnetic_acceleration_and_angular_rates())
	#print("Mag and Grav Ref Vec" , vnSensor.read_magnetic_and_gravity_reference_vectors())

	print("")
	print("Info: " , compData.yaw_pitch_roll)
	print("")
	'''
	
	#vnSensor.disconnect()
	ez.disconnect()
	
############################################################################
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
