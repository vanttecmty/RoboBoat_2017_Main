import sys
import os
import xbee

x = xbee.xbee('/dev/ttyUSB0');
x.send2boat('000000000');