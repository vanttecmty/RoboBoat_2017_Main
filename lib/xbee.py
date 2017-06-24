import datetime
import serial
import time

leidoAnterior = ""

class xbee:
	def __init__(self,USB):
		self.connection=serial.Serial(USB,9600)
		self.timestamp=''
		self.challenge='0'
		self.latitude= 'HDDD.DDDDDD'
		self.longitude='HDDD.DDDDDD'
		self.takeoff='0'
		self.flying='0'
		self.landing = '0'

	def set_challenge(self,chal='N'):
		self.challenge = chal

	def set_latlong(self,latitude,longitude):
		self.latitude=latitude
		self.longitude=longitude

	def set_takeoff(self,take):
		self.takeoff=take

	def set_flying(self, fly):
		self.flying=fly

	def set_landing(self, land):
		self.landing=land

	def send2station(self):
		date=str(datetime.datetime.now())
		#print(date)
		fecha=date.split('-')
		dia=fecha[2].split(' ')[0]
		horas=fecha[2].split(' ')[1].split(':')
		self.timestamp=fecha[0]+fecha[1]+dia+horas[0]+horas[1]+horas[2][:2]
		string=self.timestamp+','+self.latitude+','+self.longitude+','+self.challenge+','+self.takeoff+','+self.flying+','+self.landing+','+'%'
		print(string)
		self.connection.write(bytes(string, encoding='utf-8'))

	def send2boat(self,data):
		transmit = data[0]
		R_kill_switch = data[1]
		status = data[2] 
		course = data[3]
		challenge = data[4]
		dock = data[5]
		string=','+str(transmit)+','+str(R_kill_switch)+','+str(status)+','+str(course)+','+str(challenge)+','+str(dock)+','+'%'
		print(string)
		self.connection.write(bytes(string, encoding='utf-8'))

	def receive_from_station(self):
		leido=self.connection.read(17).decode("utf-8")
		data = leido.split(',');
		data = data[1 :]
		data = data[: 6]
		return data

	#29.151098, -81.016505
	def receive_from_boat(self):
		leido=self.connection.read(47).decode("utf-8")
		return leido;

