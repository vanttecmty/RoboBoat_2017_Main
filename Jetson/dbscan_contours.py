import cv2
import numpy as np
import os
import math
import time
tecla=-1

minRadius=30
buoy_diameter=20.32 #cm
global_image=None
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
			#imagen2=image.copy()
			#cv2.rectangle(imagen2, (x1,y1),(x2,y2),(0,0,255),2)
			primera=True
			
			#hsv=cv2.cvtColor(global_image,cv2.COLOR_BGR2HSV)
			##cv2.imshow('hsv',hsv)
			H,HS,S,SS,L,LS =area_stats(global_image)
			print(area_stats(global_image))
			
			HL=max([H-HS,0])
			SL=max([S-SS,0])
			LL=max([L-LS,0])
			HH=max([H+HS,0])
			SH=max([S+SS,0])
			LH=max([L+LS,0])
						
			lower=np.array([HL, SL, LL])
			upper=np.array([HH ,SH,LH])
			print (lower)
			print (upper)
			filtrada=cv2.inRange(global_image,lower, upper)
			#cv2.imshow('filtrada',filtrada)
			#cv2.waitKey(0)
			#print x1,y1,x2,y2

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
	
	
	#yrgb
def DBSCAN(array, epsylon, minPts,return_centroid=False,blu=False):
	start_time = time.time()

	todos_contornos=cv2.findContours(array,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#print(todos_contornos[1])
	contours=[]
	for contorno in todos_contornos[1]:
		area=cv2.contourArea(contorno)
		if area>minPts:
			contours.append(contorno)

	
	obstacles=np.zeros(array.shape,dtype=np.uint8)
	#print 'Contornos en la imagen: ',len(contours)
	if len(contours)<1:
		return

	if len(contours)==1:
		(x,y),radius = cv2.minEnclosingCircle(contours[0])
		center = (int(x),int(y))
		radius = int(radius)
		cv2.circle(obstacles,center,radius,255,2)

	if len(contours)>1:
		centroids=np.zeros((len(contours),2),dtype=np.uint32)
		for i,contorno in enumerate(contours):
			#agregar condicion de area aqui para filtrar muy pequenos?
			M1 = cv2.moments(contorno)
			if (M1['m00']==0):
				M1['m00']=1
			cx1 = int(M1['m10']/M1['m00'])
			cy1 = int(M1['m01']/M1['m00'])
			centroids[i]=[cy1,cx1]

		distance_matrix=np.zeros((len(contours),len(contours)),dtype=np.float32)
		#print centroids
		for A in range(0,len(contours)):
			for B in range(A+1,len(contours)):
			
				pointA=centroids[A]
				pointB=centroids[B]
				#print pointA, pointB
				if pointA[0]>pointB[0]:
					x=pow((pointA[0]-pointB[0]),2)
				else:
					x=pow((pointB[0]-pointA[0]),2)
			
				if pointA[1]>pointB[1]:
					y=pow((pointA[1]-pointB[1]),2)
				else:
					y=pow((pointB[1]-pointA[1]),2)

				dist=math.sqrt(x+y)
				distance_matrix[A][B]=dist
				distance_matrix[B][A]=dist
	
			distance_matrix[A][A]=999

		#print(distance_matrix)

		links=np.argwhere(distance_matrix<epsylon)
	
		segmentation_vector=np.zeros(len(contours),dtype=np.uint8)

		counter=1
		for i,link in enumerate(links):
			#print 'iteration ', i
			point1=centroids[link[0]]
			point2=centroids[link[1]]
			#print point1,point2
			#print link[0],link[1]
			A=link[0]
			B=link[1]

			if ( segmentation_vector[A]==0 and segmentation_vector[B]==0 ):
				segmentation_vector[A]=counter
				segmentation_vector[B]=counter
				counter+=1
			elif(segmentation_vector[A]==0 or segmentation_vector[B]==0):
				if segmentation_vector[A]>segmentation_vector[B]:
					segmentation_vector[B]=segmentation_vector[A]
				else:
					segmentation_vector[A]=segmentation_vector[B]
	
	
		num_objetos=np.amax(segmentation_vector)
		#print(num_objetos)

		contornos=[]

		#print segmentation_vector

		
		
		for i in range(1,num_objetos+1):
			puntos=[]
			#print 'Objeto ',i
			indexes=np.argwhere(segmentation_vector==i)
			#print 'Indexes:', indexes
			for index in indexes:
				#print 'Index: ',index[0]
				contor=contours[index[0]]
				#print contor
				#print len(contor)
				for punto in contor:
					puntos.append(punto)


			enclose=np.asarray(puntos)
			#print enclose
			#print 'cantidad de puntos:',len(enclose)
			if len(enclose)>minPts:
				(x,y),radius = cv2.minEnclosingCircle(enclose)
				center = (int(x),int(y))
				radius = int(radius)
				if radius>40:
					continue
				if blu:
					
					#print center,radius
					if y<240 and radius>20:
						continue
				cv2.circle(obstacles,center,radius,255,2)
				

	#elapsed_time = time.time() - start_time
	#print ('Elapsed Time ',elapsed_time)
	return obstacles
	


cv2.namedWindow('get rectangle')
cv2.setMouseCallback('get rectangle',draw_rectangle)


gl=np.array([ 58.32762133,  87.85200046,  28.7195858 ]) #color anexo
gu=np.array([  95.13517359,  146.22341797,   64.02411252])

yl=np.array([  80.3520097,   174.51407643,  191.33034903])
yu=np.array([ 125.59920982,  219.38139395,  233.45850114])

'''
gl=np.array([  71.49535277,  150.41099537,    2.82631499])
gu=np.array([ 144.98700017,  229.38312228,   86.85799873])

yl=np.array([   0,          185.84549612,  214.80200567])
yu=np.array([  40.74302368,  247.40295108,  259.97206265])
'''
bl=np.array([ 78.12765314,  26.00777318,   0.        ])
bu=np.array([ 148.10418077,   80.51817838,   53.99514731])

rl=np.array([   0,            0,          115.39777469])
ru=np.array([  43.71792393,   47.60779081,  239.44837916])

nl=np.array([   0,            0,          0])
nu=np.array([  20,   20,  20])

hsblue=np.array([ 107.19552311,  184.64772921,  102.44292567])
hsblue=np.array([ 109.66161975,  218.94410753,  164.98564576])

primera=True
#path='/home/ubuntu/RoboBoat_2017_Main/Jetson/fotos/'
#files=os.listdir(path)



	
	
def get_obstacles(image,colors='rgby',return_centroid=False,buoy='A0'):
	#image=cv2.imread(path+image_file)
	
	#image=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)	
	global_image=image
	
	azul=cv2.inRange(image,bl, bu)
	rojo=cv2.inRange(image,rl, ru)
	amarillo=cv2.inRange(image,yl, yu)
	verde=cv2.inRange(image,gl, gu)
	negro=cv2.inRange(image,nl, nu)

	
	epsy=30
	size=20
	#cv2.imshow('get rectangle',image)
	#cv2.imshow('amarillo',amarillo)
	#cv2.imshow('verde',verde)
	#cv2.imshow('azul',azul)
	##cv2.imshow('rojo',rojo)
	h,w,c=image.shape
	yellow=np.zeros((h,w),dtype=np.uint8)
	green=yellow.copy()	
	blue=green.copy()
	red=blue.copy()
	ne=blue.copy()

	'''
	#Circle detection
	minVal=0
	maxVal=47
	gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	canny=cv2.Canny(gray,minVal,maxVal,True)
	contours,_=cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contour_list=[]
	for contour in contours:
		area=cv2.contourArea(contour)
		#print(area)
		if (area>50):
			approx=cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
			#print len(approx)
			if len(approx)>14:
				contour_list.append(contour)
				#np.save('circle',contour)

	value=np.load('circle.npy')
	image3=np.full(image.shape,255,dtype=np.uint8)
	circulos=[]
	for contorno in contour_list:
		parecido=cv2.matchShapes(value,contorno,1,0.0)
		#print(parecido)
		if parecido<0.1:
			cv2.drawContours(image3,contorno,-1,(255,0,0),2)
			circulos.append(contorno)

	dentroCircle=np.zeros(image.shape,dtype=np.uint8)
	bindex=np.nonzero(azul)
	if(len(bindex[0])>1):
		tamano=len(circulos)
		blue_obstacle=np.argwhere(azul==255)
		if tamano==1:
			for punto in blue_obstacle:
				#print(circulos[0][0][0])
				#print punto
				dist=cv2.pointPolygonTest(circulos[0],(punto[1],punto[0]),True)
				if dist>=0:
					cv2.drawContours(dentroCircle,circulos,-1,(255,255,255),2)
		elif tamano>1:
			for circulo in circulos: 
				for punto in blue_obstacle:
					dist=cv2.pointPolygonTest(circulo,punto,True)
					if dist>=0:
						cv2.drawContours(dentroCircle,contorno,-1,(0,0,0),2)
	cont=np.zeros(image.shape,dtype=np.uint8)
	cont=cv2.bitwise_or(cont,dentroCircle)
	#cv2.imshow('Boyas',cont)
	'''

	#Here ends circle detection and starts color detection

	obstacles=np.zeros((h,w),dtype=np.uint8)

	if 'y' in colors:
		yindex=np.argwhere(amarillo==255)
		#print(yindex.shape)
		if (len(yindex[0])>1):
			yellow=DBSCAN(amarillo,epsy,size,False)
			if yellow is not None:
				obstacles=np.bitwise_or(obstacles,yellow)

	if 'g' in colors:
		gindex=np.argwhere(verde==255)
		if (len(gindex[0])>1):
			green=DBSCAN(verde,epsy,size,False)
			if green is not None:
				obstacles=np.bitwise_or(obstacles,green)

	if 'r' in colors:	
		rindex=np.argwhere(rojo==255)
		if (len(rindex[0])>1):
			red=DBSCAN(rojo,epsy,size,False)
			obstacles=np.bitwise_or(obstacles,red)


	image3=np.zeros(image.shape,dtype=np.uint8)
	dentroCircle=np.zeros(image.shape,dtype=np.uint8)

	if 'b' in colors:
		bindex=np.nonzero(azul)
		if (len(bindex[0]>1)):
			blue=DBSCAN(azul,epsy,size,True)
			if blue is not None:
				#obstacles=np.bitwise_or(obstacles,blue)
				pass
		
	if 'n' in colors:
		nindex=np.nonzero(negro)
		if (len(bindex[0]>1)):
			ne=DBSCAN(azul,epsy,size,True)
				if ne is not None:
				#obstacles=np.bitwise_or(obstacles,ne)
				pass
	
	
	
	#cv2.imshow('obstacles',obstacles)
	#cv2.waitKey(0)
	contours=cv2.findContours(obstacles,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	#print len(contours)

	obstacles_centroid=[0,0]
	found_obstacles=[]

	if buoy=='A0':
		buoy_diameter=20.32
	elif buoy=='A2':
		buoy_diameter=36.86

	for contorno in contours[1]:
		M1 = cv2.moments(contorno)
		if (M1['m00']==0):
			M1['m00']=1
		cx1 = int(M1['m10']/M1['m00'])
		cy1 = int(M1['m01']/M1['m00'])

		obstacles_centroid[0]+=cy1
		obstacles_centroid[1]+=cx1		
		rect=cv2.boundingRect(contorno)
		x=int(rect[0])
		y=int(rect[1])
		dx=int(rect[2])
		dy=int(rect[3])
		copia=image.copy()
		cv2.rectangle(image,(x,y),(x+dx,y+dy),(0,0,255),2,8)
	
		#print h,w		
		dpp=float(69)/h
		
		if cx1>w/2:
			pixels=cx1-w/2
		else:
			pixels=-(w/2-cx1)

		degrees=dpp*pixels
		
		pixel_width=dx	#Pixel
		W=buoy_diameter	#Real Width
		F=697.34		#Focal length
		distance=(W*F)/pixel_width
		'''
		print('Centroid: ',cx1,cy1)	
		print("Degrees: ",degrees)
		print ('Distance to buoy (cm): ',distance)
		'''

		found_obstacles.append([distance,-1*degrees])

	size=len(contours[1])
	if return_centroid and size>=1:
		distance=0
		degrees=0
		for obsta in found_obstacles:
			distance+=obsta[0]
			degrees+=obsta[1]
		centroid_values=[distance/size,degrees/size]
		return obstacles,centroid_values 
	else:	
		return obstacles,found_obstacles;


'''
while key==-1:
	ret,global_image=capture.read()
	#if ret:
	cv2.imshow('frame',global_image)
	key=cv2.waitKey(10)
	#print('Key:',key)
	obstaculos=get_obstacles(global_image,'rg',True,'A0')
	print(obstaculos[1])
'''

