/*
 *  RPLIDAR
 *  Ultra Simple Data Grabber Demo App
 *
 *  Copyright (c) 2009 - 2014 RoboPeak Team
 *  http://www.robopeak.com
 *  Copyright (c) 2014 - 2016 Shanghai Slamtec Co., Ltd.
 *  http://www.slamtec.com
 *
 */
/*
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>    //strlen
#include <sys/socket.h>    //socket
#include <arpa/inet.h> //inet_addr

#include "rplidar.h" //RPLIDAR standard sdk, all-in-one header

#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

#ifdef _WIN32
#include <Windows.h>
#define delay(x)   ::Sleep(x)
#else
#include <unistd.h>
static inline void delay(_word_size_t ms){
    while (ms>=1000){
        usleep(1000*1000);
        ms-=1000;
    };
    if (ms!=0)
        usleep(ms*1000);
}
#endif

using namespace rp::standalone::rplidar;

bool checkRPLIDARHealth(RPlidarDriver * drv)
{
    u_result     op_result;
    rplidar_response_device_health_t healthinfo;


    op_result = drv->getHealth(healthinfo);
    if (IS_OK(op_result)) { // the macro IS_OK is the preperred way to judge whether the operation is succeed.
        printf("RPLidar health status : %d\n", healthinfo.status);
        if (healthinfo.status == RPLIDAR_STATUS_ERROR) {
            fprintf(stderr, "Error, rplidar internal error detected. Please reboot the device to retry.\n");
            // enable the following code if you want rplidar to be reboot by software
            // drv->reset();
            return false;
        } else {
            return true;
        }

    } else {
        fprintf(stderr, "Error, cannot retrieve the lidar health code: %x\n", op_result);
        return false;
    }
}

#include <signal.h>
bool ctrl_c_pressed;
void ctrlc(int)
{
    ctrl_c_pressed = true;
}

int main(int argc, const char * argv[]) {
    const char * opt_com_path = NULL;
    _u32         opt_com_baudrate = 115200;
    u_result     op_result;

    printf("Ultra simple LIDAR data grabber for RPLIDAR.\n"
           "Version: "RPLIDAR_SDK_VERSION"\n");

    // read serial port from the command line...
    if (argc>1) opt_com_path = argv[1]; // or set to a fixed value: e.g. "com3" 

    // read baud rate from the command line if specified...
    if (argc>2) opt_com_baudrate = strtoul(argv[2], NULL, 10);


    if (!opt_com_path) {
#ifdef _WIN32
        // use default com port
        opt_com_path = "\\\\.\\com3";
#else
        opt_com_path = "/dev/ttyUSB0";
#endif
    }

    // create the driver instance
    RPlidarDriver * drv = RPlidarDriver::CreateDriver(RPlidarDriver::DRIVER_TYPE_SERIALPORT);
    
    if (!drv) {
        fprintf(stderr, "insufficent memory, exit\n");
        exit(-2);
    }


    // make connection...
    if (IS_FAIL(drv->connect(opt_com_path, opt_com_baudrate))) {
        fprintf(stderr, "Error, cannot bind to the specified serial port %s.\n"
            , opt_com_path);
        goto on_finished;
    }

    rplidar_response_device_info_t devinfo;

	// retrieving the device info
    ////////////////////////////////////////
    op_result = drv->getDeviceInfo(devinfo);

    if (IS_FAIL(op_result)) {
        fprintf(stderr, "Error, cannot get device info.\n");
        goto on_finished;
    }

    // print out the device serial number, firmware and hardware version number..
    printf("RPLIDAR S/N: ");
    for (int pos = 0; pos < 16 ;++pos) {
        printf("%02X", devinfo.serialnum[pos]);
    }

    printf("\n"
            "Firmware Ver: %d.%02d\n"
            "Hardware Rev: %d\n"
            , devinfo.firmware_version>>8
            , devinfo.firmware_version & 0xFF
            , (int)devinfo.hardware_version);

    // check health...
    if (!checkRPLIDARHealth(drv)) {
        goto on_finished;
    }

	signal(SIGINT, ctrlc);

	drv->startMotor();
    // start scan...
    drv->startScan();

    int sock;
    struct sockaddr_in server;
    char message[2000];
    char measure[50];
    int measures[360];
    memset(measures, 0, 360);
     
    //Create socket
    sock = socket(AF_INET , SOCK_STREAM , 0);
    if (sock == -1)
    {
        printf("Could not create socket");
    }
    puts("Socket created");
     
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 8893 );
 
    //Connect to remote server
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
        perror("connect failed. Error");
        return 1;
    }
     
    puts("Connected\n");

    // fetech result and print it out...
    while (1) {
        rplidar_response_measurement_node_t nodes[360*2];
        size_t   count = _countof(nodes);
        op_result = drv->grabScanData(nodes, count);

        if (IS_OK(op_result)) {
            drv->ascendScanData(nodes, count);
            for (int pos = 0; pos < (int)count ; ++pos) { 
                //Has scan been completed?
                if(nodes[pos].sync_quality & RPLIDAR_RESP_MEASUREMENT_SYNCBIT) {
                    memset(message, 0, sizeof(message));

                    for (int i = 0; i < 360; ++i) {
                        if(measures[i] > 0) {
                            sprintf( 
                                measure, 
                                "%d,%d;", 
                                i,
                                measures[i]
                            );

                            strcat(message, measure);
                        }
                    }

                    if( send(sock , message , strlen(message) , 0) < 0) {
                        printf("a\n");
                        puts("Send failed");
                        return 1;
                    } else {
                        //printf("Mandado: %s\n", message);
                    }
                }

                measures[int((nodes[pos].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT)/64.0f) % 360] = int(nodes[pos].distance_q2/4.0f);
            }
        }

        if (ctrl_c_pressed) { 
			break;
		}
    }

    drv->stop();
    drv->stopMotor();
    // done!

on_finished:
    RPlidarDriver::DisposeDriver(drv);
    return 0;
}

