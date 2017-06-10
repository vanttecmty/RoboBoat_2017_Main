import cv2
import numpy as np
import os
import math
import time
tecla=-1

def DBSCAN(array, epsylon, minPts):
	start_time = time.time()
	contours,_=cv2.findContours(array,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	obstacles=np.zeros(array.shape,dtype=np.uint8)
	print 'Contornos en la imagen: ',len(contours)
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

		print(distance_matrix)

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
				cv2.circle(obstacles,center,radius,255,2)
		

	elapsed_time = time.time() - start_time
	print 'Elapsed Time ',elapsed_time
	return obstacles
	


gl=np.array([  71.49535277,  150.41099537,    2.82631499])
gu=np.array([ 144.98700017,  229.38312228,   86.85799873])

yl=np.array([   0,          185.84549612,  214.80200567])
yu=np.array([  40.74302368,  247.40295108,  259.97206265])

bl=np.array([ 78.12765314,  26.00777318,   0.        ])
bu=np.array([ 148.10418077,   80.51817838,   53.99514731])

rl=np.array([   0,            0,          115.39777469])
ru=np.array([  43.71792393,   47.60779081,  239.44837916])



hsblue=np.array([ 107.19552311,  184.64772921,  102.44292567])
hsblue=np.array([ 109.66161975,  218.94410753,  164.98564576])


path='/home/ubuntu/Roboboat/fotos/'
files=os.listdir(path)

for image_file in files:
	image=cv2.imread(path+image_file)
	cv2.imshow("image",image)
		
	
	azul=cv2.inRange(image,bl, bu)
	rojo=cv2.inRange(image,rl, ru)
	amarillo=cv2.inRange(image,yl, yu)
	verde=cv2.inRange(image,gl, gu)


	epsy=30
	size=20


	h,w,c=image.shape
	yellow=np.zeros((h,w),dtype=np.uint8)
	green=yellow.copy()	
	blue=green.copy()
	red=blue.copy()

	yindex=np.nonzero(amarillo)
	if (len(yindex[0])>1):
		yellow=DBSCAN(amarillo,epsy,size)
	
	gindex=np.nonzero(verde)
	if (len(gindex[0])>1):
		green=DBSCAN(verde,epsy,size)

	bindex=np.nonzero(azul)
	if (len(bindex[0]>1)):
		ok=DBSCAN(azul,epsy,size)
	
	
	rindex=np.nonzero(rojo)
	if (len(rindex[0])>1):
		red=DBSCAN(rojo,epsy,size)
	
	obstacles=np.bitwise_or(yellow,green)
	obstacles=np.bitwise_or(obstacles,blue)
	obstacles=np.bitwise_or(obstacles,red)
	cv2.imshow('obstacles',obstacles)
	
	contours,_=cv2.findContours(obstacles,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	for contorno in contours:
		rect=cv2.boundingRect(contorno)
		print rect
		copia=image.copy()
		cv2.drawContours(image,[box],0,(0,0,255),2)



	tecla=cv2.waitKey(0)
	
	if tecla==1048689:
		break
