import sys
import os
import xbee
import time
import lib.imu as imu
import lib.variables as var

x = xbee.xbee("/dev/ttyUSB1")

challenges = ['autonomous','speed', 'follow', 'path', 'docking', 'return']

courses = ['courseA', 'courseB', 'courseC']

#To do: Sacar coordenadas de la imu
lat_long = ["29.151098","-81.016505"];

# challenge string
#challenge = 'N'

enable_pos = 0
R_kill_switch = 1
status = 2
course = 3
challenge_pos = 4
dock = 5


def start_mission():
	imu.init();
	for i in range(1,5):
		send_start(lat_long)

	while(var.challenge != 'd'):
		send_heartbeat()

	# Aqui esta haciendo el docking
	resp = '0'
	counter = 0
	print("Receiving docking data...")
	while resp == '0':
		s = x.receive_from_station();	
		resp = s[enable_pos]; 
		counter += 1
	
	print("Go to dock : ", s[dock])

	if(counter < 5):
		time.sleep(6-counter);
	else:
		print("Algo salio mal con la respuesta del dock")

	# To Do: Mover el barco hacia s[dock]

	# Espera a que se mande la 'e' de fin de mision
	while(var.challenge != 'e'):
		send_heartbeat()


def send_heartbeat():
	# To Do: Obtener coordenadas y cambiar en la siguiente linea
	coords = imu.get_gps_coords();
	x.set_latlong(coords['latitude'],coords['longitude']);
	x.set_challenge(var.challenge)
	x.send2station()
	time.sleep(1.05)


def send_start(latlong):
	x.set_flying("0");
	x.set_takeoff("0");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('s');
	x.send2station();
	time.sleep(1.05);

def send_end(latlong):
	x.set_flying("0");
	x.set_takeoff("0");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('e');
	x.send2station();
	time.sleep(1.05);

def send_return(latlong):
	x.set_flying("0");
	x.set_takeoff("0");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('r');
	x.send2station();
	time.sleep(1.05);

def send_follow(latlong):
	x.set_flying("0");
	x.set_takeoff("0");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('f');
	x.send2station();
	time.sleep(1.05);

def send_docking(latlong):
	x.set_flying("0");
	x.set_takeoff("0");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('d');
	x.send2station();
	time.sleep(1.05);

def send_heart_beat(latlong):
	x.set_flying("0");
	x.set_takeoff("0");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('N');
	x.send2station();
	time.sleep(1.05);

def send_takeoff(latlong):
	x.set_flying("0");
	x.set_takeoff("1");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('d');
	x.send2station();
	time.sleep(1.05);

def send_flying(latlong):
	x.set_flying("1");
	x.set_takeoff("1");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('d');
	x.send2station();
	time.sleep(1.05);

def send_landing(latlong):
	x.set_flying("0");
	x.set_takeoff("0");
	x.set_landing("1");
	x.set_latlong(latlong[0],latlong[1]);
	x.set_challenge('d');
	x.send2station();
	time.sleep(1.05);

#Send Testing OK
def send_testing():
	global enable_pos
	#while True:
	send_start(lat_long);
	send_start(lat_long);
	send_start(lat_long);

	for i in range(1,5):
		send_heart_beat(lat_long);
		if i == 2:
			send_docking(lat_long);
			send_docking(lat_long);
			time.sleep(2);
			resp = '0'
			counter = 0
			while resp == '0':
				print("Receiving")
				s = x.receive_from_station();	
				resp = s[enable_pos]; 
				counter += 1
				print("Go to dock : ", s[dock])

			if(counter < 5):
				time.sleep(6-counter);
			send_takeoff(lat_long);
			send_flying(lat_long);
			send_landing(lat_long);
		elif i == 5:
			send_follow(lat_long);
		elif i == 9:
			send_return(lat_long);

	send_end(lat_long);
	send_end(lat_long);
	send_end(lat_long);

	
def send_testing_2():
	resp = ''
	while(resp != '1'):
		s = x.receive_from_station();	
		resp = s[enable_pos];
	while(s[challenge_pos] == '0'):
		send_start(lat_long);
		s = x.receive_from_station();
	print("Starting")
	x.send_end();	

#Receive Testing
def receive_testing():
	s = x.receive_from_station();	
	print(s)
	return s



if __name__ == '__main__':
	start_mission()
	'''
	while True:
		s = receive_testing();
		if (s[enable_pos] == '1'):
			send_heart_beat()
	'''

