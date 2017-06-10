import os
import sys
import tty
import time
import termios
#import lib.imu as imu
import lib.lidar as lidar
import lib.variables as var
import lib.utility as utility
import lib.motors as motors
import lib.navigation as nav

utility.get_serial_ports();
#motors.open_communication()
#motors.test_motors('b', 128 , 128)
#motors.open_communication()
#motors.move_thrusters(var.rightThruster, 1400)
#motors.move_servo(var.leftServo, 120)
#imu.init();
#print(imu.get_gps_coords());
#print(imu.get_yaw_orientation());
#print(imu.get_gps_acceleration_velocity());
#print(imu.get_angular_rates());
#print(imu.get_acceleration());
#print(imu.get_delta_theta());
#print(imu.get_delta_velocity());
#imu.get_degrees_to_north_orientation();
#print(imu.get_degrees_to_gps_coords(25.6500019, -100.2907928));