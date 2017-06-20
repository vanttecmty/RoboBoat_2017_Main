#Estación

#Comunicación del Serial independiende a la de Variable
#Esta comunicación es únicamente para la estación.

#Comunicación con el Bote a través de XBEE
#Establecer Comunicación con el Servidor de AUVSI
#Comunicarse con BT a la aplicación
#Leer Kill Switch del Bote
#Sí se puede saber del Kill Switch del Drone

import sys
import os
import serial
import io
from bluetooth import *
from PIL import Image
from array import array

arduinoBaudRate = 115200;
blueTooth = 0;


