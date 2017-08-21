#!/usr/bin/env python
'''
	@author Juan Carlos Aguilera
'''

import sys
import json
import requests
'''
server = IP
server = http://...
'''
url = 'http://betatestback.journeytheapp.com' ;
teamCode = 'vant-TEC' ;
PORT = 80 ;
retryCount = 0 ;
connectionLost = False;
courseA = 'CourseA';
courseB = 'CourseB';
courseC = 'CourseC';

def send_http_followLeader(course):
	'''
		GET
		/followLeader/{course}/{teamCode}
	'''
	'''
		expected return value {"code":"23"}
	'''
	addr = '/followLeader/';
	
	server = url + addr + course + '/' + teamCode ;
	
	r = requests.get(server);

	print(server)

	if(r.status_code == 200):
		print ('Status 200: OK');
		print((r.text))
	elif(r.status_code == 400):
		print('Status 400: The requested Form isnt Ok, Please check it');
	elif(r.status_code == 404):
		print('Status 404: Course or Team are Wrong');
	elif(r.status_code == 500):
		print('Status 500: The gate assigment is broken');
	elif(r.status_code == 503):
		print('Status 503: Please try the request again');
		if(retryCount < 100):
			send_http_heartbeat(course,timestamp,challenge,latitude,longitude)
		else:
			retryCount = 0;
			connectionLost = True;

def send_http_heartbeat(course,timestamp,challenge,latitude,longitude):
	'''
		POST
		/heartbeat/
		course
		teamCode
		timestamp = YYYYMMDDHHMMSS in UTC
		challenge = "speed", "docking", "path", "follow" or "return"
		latitude  = hddd.dddddd
		longitude = hddd.dddddd
	'''
	'''
		expected return value {"success":<status>}
		status = true  //Run still active
		status = felse //Run have ended
	'''
	addr = '/heartbeat/' + course + '/' + teamCode;

	server = url + addr ;

	payload = {'timestamp':timestamp, 'challenge':challenge, 'latitude':round(latitude,6), 'longitude':round(longitude,6)} ;

	r = requests.post(server, data=payload) ;

	print(server)
	print(payload)

	if(r.status_code == 200):
		print ('Status 200: OK');
		print((r.text))
	elif(r.status_code == 400):
		print('Status 400: The requested Form isnt Ok, Please check it');
	elif(r.status_code == 404):
		print('Status 404: Course or Team are Wrong');
	elif(r.status_code == 500):
		print('Status 500: The gate assigment is broken');
	elif(r.status_code == 503):
		print('Status 503: Please try the request again');
		if(retryCount < 100):
			send_http_heartbeat(course,timestamp,challenge,latitude,longitude)


def send_http_docking_2(course,filename):
	'''
		POST
		/docking/image/
		course
		teamCode
		name = file
		filename = 'test.jpg'
	'''
	'''
		expected return value {"id":<imageID>}}
	'''

	addr = '/docking/image/' + course +'/' + teamCode ;
	
	headers = {'Content-type':'multipart/form-data'} ;
	
	server = url + addr ;
	
	files = {'name' : open(filename,'rb') } 

	payload = {'filename': filename } ;

	r = requests.post(server, data = payload, files=files) ;

	if(r.status_code == 100):
		print ('Status 100: Server is ready to accept multipart chunk');
	elif(r.status_code == 200):
		print ('Status 200: OK');
		print((r.text))
		imgId = json.loads(r.text)
	elif(r.status_code == 202):
		print('Status 202: Upload successfully completed');
		print((r.text))
		imgId = json.loads(r.text)
	elif(r.status_code == 400):
		print('Status 400: The requested Form isnt Ok, Please check it');
	elif(r.status_code == 404):
		print('Status 404: Course or Team are Wrong');
	elif(r.status_code == 500):
		print('Status 500: The gate assigment is broken');
	elif(r.status_code == 503):
		print('Status 503: Please try the request again');
		if(retryCount < 100):
			send_http_heartbeat(course,timestamp,challenge,latitude,longitude)

	return imgId

