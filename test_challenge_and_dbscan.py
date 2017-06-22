
import numpy
import os
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import cv2
import challenge
import Jetson.dbscan as dbscan

tecla=-1
minVal=0
maxVal=47

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
			H,HS,S,SS,L,LS =area_stats(image)
			print(area_stats(image))
			
			HL=max([H-HS,0])
			SL=max([S-SS,0])
			LL=max([L-LS,0])
			HH=max([H+HS,0])
			SH=max([S+SS,0])
			LH=max([L+LS,0])
						
			lower=numpy.array([HL, SL, LL])
			upper=numpy.array([HH ,SH,LH])
			print (lower)
			print (upper)
			filtrada=cv2.inRange(hsv,lower, upper)
			cv2.imshow('filtrada',filtrada)
			print (x1,y1,x2,y2)

def area_stats(sourceImage):
	area=abs(x2-x1)*abs(y2-y1)	
	promedio=numpy.zeros((3, area),dtype=numpy.int)
	i=0
	for x in range(x1,x2):
		for y in range(y1,y2):
			promedio[0][i]=sourceImage[y][x][0]
			promedio[1][i]=sourceImage[y][x][1]
			promedio[2][i]=sourceImage[y][x][2]
			i+=1

	return numpy.mean(promedio[0]),numpy.std(promedio[0]),numpy.mean(promedio[1]),numpy.std(promedio[1]),numpy.mean(promedio[2]),numpy.std(promedio[2])

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_rectangle)


gl=numpy.array([  71.49535277,  150.41099537,    2.82631499])
gu=numpy.array([ 144.98700017,  229.38312228,   86.85799873])

yl=numpy.array([   0,          185.84549612,  214.80200567])
yu=numpy.array([  40.74302368,  247.40295108,  259.97206265])

bl=numpy.array([ 78.12765314,  26.00777318,   0.        ])
bu=numpy.array([ 148.10418077,   80.51817838,   53.99514731])

rl=numpy.array([   0,            0,          115.39777469])
ru=numpy.array([  43.71792393,   47.60779081,  239.44837916])

hsblue=numpy.array([ 107.19552311,  184.64772921,  102.44292567])
hsblue=numpy.array([ 109.66161975,  218.94410753,  164.98564576])


path='/home/naoitesm/RoboBoat_2017_Main/dataset/'
files=os.listdir(path)

circle_contour=numpy.load('circle.npy')

for image_file in files:
	image=cv2.imread(path+image_file)
	cv2.imshow("image",image)
	
	autonomous=challenge.Autonomous_Navigation()

	autonomous.get_destination(image)
	tecla=cv2.waitKey(0)
	print (tecla)
	if tecla==1048689 or tecla==113:
		break
