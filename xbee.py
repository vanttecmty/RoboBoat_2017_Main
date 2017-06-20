import datetime
import serial

class xbee:
	def __init__(self,USB):
		self.connection=serial.Serial(USB,9600)
		self.timestamp=''
		self.challenge='0'
		self.latlon='HDDD.DDDDDD'
		self.takeoff='0'
		self.flying='0'

	def set_latlong(self,latitude,longitude):
		self.latlon='HDDD.DDDDDD'

	def set_takeoff(self,take):
		self.takeoff=take

	def set_flying(self, fly):
		self.flying=fly

	def send2station(self):
		date=str(datetime.datetime.now())
		print(date)
		fecha=date.split('-')
		dia=fecha[2].split(' ')[0]
		horas=fecha[2].split(' ')[1].split(':')
		self.timestamp=fecha[0]+fecha[1]+dia+horas[0]+horas[1]+horas[2][:2]
		string=self.timestamp+','+self.latlon+','+self.challenge+','+self.takeoff+','+self.flying
		print(string)
		self.connection.write(bytes(string, encoding='utf-8'))

	def send2boat(self,string):
		self.connection.write(bytes(string, encoding='utf-8'))

	def receive_from_station(self):
		leido=self.connection.read(9).decode("utf-8")
		print('Read',leido)

	def receive_from_boat(self):
		leido=self.connection.read(27).decode("utf-8")
		print('Read',leido)