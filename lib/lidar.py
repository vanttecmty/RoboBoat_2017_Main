import os
import sys
import time
import math
import numpy as np
import lib.variables as var
from rplidar import RPLidar 

lidar = None;
measurments = [];

for i in range(360):
    measurments.append(0);

def open_communication():
    global lidar;
    lidar = RPLidar(var.lidarPort);
    lidar.connect();

def init():
    global measurments;
    global mapa;
    global sensor_coord_x;
    global sensor_coord_y;

    open_communication();

    try:
        for measurment in lidar.iter_measurments():
            if(measurment != 'Wrong body size'):
                measurments[int(measurment[2])%360] = measurment[3];
                #print(measurments[int(measurment[2])%360]);
            else:
                return 'Wrong body size'
    except KeyboardInterrupt:
        print('Stoping...');

def test():
    return measurments;

def lidar_stop():
    lidar.stop();
    lidar.stop_motor();
    lidar.disconnect();