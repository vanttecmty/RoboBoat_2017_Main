import cv2
import numpy as np
import os
import math
import time
tecla=-1
minVal=0
maxVal=47

def DBSCAN(array, epsylon, minPts):
	start_time = time.time()
	puntos=np.argwhere(array==255)
	distance_matrix_eu=np.zeros((len(puntos),len(puntos)),dtype=np.float32)
	distance_matrix_man=np.zeros((len(puntos),len(puntos)),dtype=np.int32)
	#print(len(puntos))
	#print puntos
	for a in range(0,len(puntos)):
		distance_matrix_eu[a][a]=9999
		distance_matrix_man[a][a]=9999
		for b in range(a+1,len(puntos)):
			#print puntos[a][0],puntos[a][1]
			#print puntos[b][0],puntos[b][1]
			#distancia euclidiana
			y=pow((puntos[a][0]-puntos[b][0]),2)
			x=pow((puntos[a][1]-puntos[b][1]),2)
			dist=math.sqrt(x+y)
			distance_matrix_eu[a][b]=dist
			distance_matrix_eu[b][a]=dist

			#distancia manhattan
			dist=abs(puntos[a][0]-puntos[b][0])+abs(puntos[a][1]-puntos[b][1])
			distance_matrix_man[a][b]=dist
			distance_matrix_man[b][a]=dist



	
	#print(distance_matrix_eu)



	links=np.argwhere(distance_matrix_eu<epsylon)
	
	segmentation_vector=np.zeros(len(puntos),dtype=np.uint8)

	counter=1
	for i,link in enumerate(links):
		#print 'iteration ', i
		point1=puntos[link[0]]
		point2=puntos[link[1]]
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
	print(num_objetos)

	contornos=[]

	print segmentation_vector

	obstacles=np.zeros(array.shape,dtype=np.uint8)
	for i in range(1,num_objetos):
		print 'Iteracion ',i
		indexes=np.argwhere(segmentation_vector==i)
		#print indexes
		contor=puntos[indexes]

		#print contor
		#print ' '
		
		if len(contor)>minPts:
			(x,y),radius = cv2.minEnclosingCircle(contor)
			center = (int(y),int(x))
			radius = int(radius)
			cv2.circle(obstacles,center,radius,255,2)
		

	elapsed_time = time.time() - start_time
	print 'Elapsed Time ',elapsed_time
	cv2.imshow('obstacles',obstacles)
	


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


	cv2.imshow('rojo',rojo)
	
	yindex=np.nonzero(amarillo)

	'''
	#print(yindex)
	if (len(yindex[0])>1):
		DBSCAN(amarillo,20,10)

	

	gindex=np.nonzero(verde)
	#print(gindex)
	if (len(gindex[0])>1):
		DBSCAN(verde,20,10)


	bindex=np.nonzero(azul)
	if (len(bindex[0]>1)):
		DBSCAN(azul,20,10)
	
	'''
	rindex=np.nonzero(rojo)
	#print(rindex)
	if (len(rindex[0])>1):
		DBSCAN(rojo,20,10)
	
	
	tecla=cv2.waitKey(0)
	
	if tecla==1048689:
		break
