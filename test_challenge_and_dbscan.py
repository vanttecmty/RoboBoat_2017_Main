
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

def nothing(x):
	pass

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
			#print(area_stats(image))
			#print(area_stats(hsv))
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
			#print (lower)
			#print (upper)
			lower2=np.array([HL2, SL2, LL2])
			upper2=np.array([HH2 ,SH2,LH2])
			#print (lower2)
			#print (upper2)
			filtrada=cv2.inRange(image,lower, upper)
			cv2.imshow('filtrada BGR',filtrada)
			filtrada2=cv2.inRange(hsv,lower2, upper2)
			cv2.imshow('filtrada HSV',filtrada2)
			print ('BGR: '+str(HL)+','+str(SL)+','+str(LL)+','+str(HH)+','+str(SH)+','+str(LH))
			print ('HSV: '+str(HL2)+','+str(SL2)+','+str(LL2)+','+str(HH2)+','+str(SH2)+','+str(LH2))

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


#path='/home/naoitesm/RoboBoat_2017_Main/dataset/'
path='/home/naoitesm/RoboBoat_2017_Main/postes/'
files=os.listdir(path)

autonomous=challenge.Autonomous_Navigation()
docking=challenge.Automated_Docking()
for image_file in files:

	image=cv2.imread(path+image_file)
	print('Image name:',image_file)
	
	
	
	tecla=-1
	while(tecla==-1):
		foundRed,foundGreen,x,y,returned_image=autonomous.get_destination(image)
		
		#docking.search_number(image,1)
		cv2.imshow("image",image)
		
		#print(foundRed,foundGreen,x,y)
		tecla=cv2.waitKey(0)
		#print (tecla)
		if tecla==1048689 or tecla==113:
			break

	if tecla==1048689 or tecla==113:
			break
