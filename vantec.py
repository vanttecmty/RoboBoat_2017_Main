import os
import sys
import tty
import time
import termios
import lib.imu as imu
import lib.lidar as lidar
import lib.variables as var
import lib.utility as utility
import lib.motors as motors
import lib.navigation as nav

utility.get_serial_ports()
imu.test_function()

