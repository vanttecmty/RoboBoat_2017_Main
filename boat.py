import sys
import os
import xbee

status = 1

while status != 0:
	x = xbee.xbee("/dev/ttyUSB1")
	x.set_latlong("-25.21341234","100.265326") 
	x.set_takeoff("0")
	x.set_flying("0")
	x.send2station()
	while status != '0' and status != '1':
		satus = x.receive_from_station()	
	