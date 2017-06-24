
import numpy as np
import os
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import cv2
import challenges as challenge
import Jetson.dbscan_contours as dbscan

tecla=-1
minVal=0
maxVal=47
primera=True
def draw_rectangle(event,x,y,flags,param):
	global x1,x2,y1,y2,primera
	if event==cv2.EVENT_LBUTTONDOWN:
		if primera:		
			#print 'Primer Click'
			primera=False
			x1=x
			y1=y
		else:
			#print 'Segundo Click'
			x2=x
			y2=y
			imagen2=image.copy()
			cv2.rectangle(imagen2, (x1,y1),(x2,y2),(0,0,255),2)
			primera=True

			hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
			cv2.imshow('hsv',hsv)

			H,HS,S,SS,L,LS =area_stats(image)
			H2,HS2,S2,SS2,L2,LS2 =area_stats(hsv)
			print(area_stats(image))
			print(area_stats(hsv))
			HL=max([H-HS,0])
			SL=max([S-SS,0])
			LL=max([L-LS,0])
			HH=max([H+HS,0])
			SH=max([S+SS,0])
			LH=max([L+LS,0])

			HL2=max([H2-HS2,0])
			SL2=max([S2-SS2,0])
			LL2=max([L2-LS2,0])
			HH2=max([H2+HS2,0])
			SH2=max([S2+SS2,0])
			LH2=max([L2+LS2,0])
						
			lower=np.array([HL, SL, LL])
			upper=np.array([HH ,SH,LH])
			print (lower)
			print (upper)
			lower2=np.array([HL2, SL2, LL2])
			upper2=np.array([HH2 ,SH2,LH2])
			print (lower2)
			print (upper2)
			filtrada=cv2.inRange(image,lower, upper)
			cv2.imshow('filtrada normal',filtrada)
			filtrada2=cv2.inRange(hsv,lower2, upper2)
			cv2.imshow('filtrada hsv',filtrada2)
			print (x1,y1,x2,y2)

def area_stats(sourceImage):
	area=abs(x2-x1)*abs(y2-y1)	
	promedio=np.zeros((3, area),dtype=np.int)
	i=0
	for x in range(x1,x2):
		for y in range(y1,y2):
			promedio[0][i]=sourceImage[y][x][0]
			promedio[1][i]=sourceImage[y][x][1]
			promedio[2][i]=sourceImage[y][x][2]
			i+=1

	return np.mean(promedio[0]),np.std(promedio[0]),np.mean(promedio[1]),np.std(promedio[1]),np.mean(promedio[2]),np.std(promedio[2])

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_rectangle)





gl=np.array([ 93.87969614,  86.42179145,  33.96279703])  #buoy cans
gu=np.array([ 137.11582457,  127.58940676,   66.06295885])

yl=np.array([   0,          185.84549612,  214.80200567])
yu=np.array([  40.74302368,  247.40295108,  259.97206265])

bl=np.array([ 78.12765314,  26.00777318,   0.        ])
bu=np.array([ 148.10418077,   80.51817838,   53.99514731])

rl=np.array([   0,            0,          115.39777469])
ru=np.array([  43.71792393,   47.60779081,  239.44837916])

hsblue=np.array([ 107.19552311,  184.64772921,  102.44292567])
hsblue=np.array([ 109.66161975,  218.94410753,  164.98564576])



capture=cv2.VideoCapture(1)
frame = capture.read();
autonomous=challenge.Autonomous_Navigation()
tecla=255
while(True):

	frame = capture.read();
	image=frame[1]
	cv2.imshow("image",image)
	
	foundRed,foundGreen,x,y=autonomous.get_destination(image)
	
		
	#print(foundRed,foundGreen,x,y)
	tecla=cv2.waitKey(0)
	#print (tecla)
	if tecla==1048689 or tecla==113:
		break


