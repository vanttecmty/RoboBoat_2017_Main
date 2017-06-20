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
import xbee 
from PIL import Image
from bluetooth import *
from array import array
import lib.bluetoothServer as bt

xb = xbee('/dev/ttyUSB0')







