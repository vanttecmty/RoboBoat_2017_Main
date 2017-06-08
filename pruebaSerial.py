import serial
import serial.tools.list_ports as ports

port = ''
pts = list(ports.comports())
if not pts:
	print ('Theres no connected sensors')
else:
	for p in pts :
		if (p[1].find('Serial') == 7):
			port = p[0]


ser = serial.Serial(port, baudrate = 9600, timeout = 1)

def getValues():

	#val = 't,' + 'b' + ',' + str(128) + ',' + str(128)
	#print(len(val))
	#for i in range(0, len(val)):
	#	print(val[i].encode())
	#	ser.write(val[i].encode())
	#	ser.flush()
	#ser.write(b'1')
	##ser.write(b'2')
	#ser.write(b'3')
	#ser.write(b'N')
	val = b't,b,128,128'
	ser.write(val)
	ser.flush()
	#arduinoData = ser.read(ser.inWaiting())
	arduinoData = ser.read(len(val))
	return arduinoData


while(1):

	userInput = input('Get data point?')

	if userInput == 'y':
		print("Valores que entran a python :" , getValues())
