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

    #open_communication();

    try:
        for scan in lidar.iter_scans(max_buf_meas = 500):
            f = open('lidar_measures.txt','w', os.O_NONBLOCK);

            for quality, degree, distance in scan:
                measurment = str(int(degree) % 360);
                measurment += "," + str(distance) + "\n";
                f.write(measurment);
                f.flush();

            f.close();
            #lidar.clear_input();
    except KeyboardInterrupt:
        print('Stoping...');

def test():
    return measurments;

def clear():
    lidar.clear_input()
