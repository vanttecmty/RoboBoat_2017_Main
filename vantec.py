import sys
import os
import lib.motors as motors
import lib.utility as utility
import lib.variables as var
import lib.imu as imu
import lib.lidar as lidar

utility.get_serial_ports()
#motors.open_communication()
#motors.test_motors('b', 128 , 128)
imu.test_function()
#motors.open_communication()
#motors.move_thrusters(var.rightThruster, 1400)
#motors.move_servo(var.leftServo, 120)