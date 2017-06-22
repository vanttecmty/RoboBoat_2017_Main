import Jetson.dbscan_contours
import math
import pathfindingv2 as pathfinding
from pathfinding import closest_node
from scipy import spatial
import numpy as np
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import cv2


red_low=np.array([  0,         3.12572092,  85.37949534]) #red buoy cans
red_upper=np.array([  32.33085987,   43.29067253,  181.69263581])

green_low_close=np.array([ 93.87969614,  86.42179145,  33.96279703])  #green buoy cans
green_upper_close=np.array([ 137.11582457,  127.58940676,   66.06295885])

green_low_far=np.array([ 55.95902545,  59.10921768,  32.3839107 ])  #green buoy cans
green_upper_far=np.array([ 65.69097455,  68.92411565,  45.13275597])




class Autonomous_Navigation:

	def get_destination(self,image):

		red=cv2.inRange(image,red_low,red_upper)
		

		green_close=cv2.inRange(image,green_low_close,green_upper_close)
		green_far=cv2.inRange(image,green_low_far,green_upper_far)
		binary=np.bitwise_or(green_close,green_far)

		red_contours=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		green_contours=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		if len(red_contours[1])>=1:

			red_area_max=0
			#Find 2 biggest areas
			biggest_red=None
			foundRed=False
			for contorno in red_contours[1]:
				print('Contour len:',len(contorno))
				area=cv2.contourArea(contorno)
				print('Area:',area)
				if area>red_area_max:
					red_area_max=area
					biggest_red=contorno
					foundRed=True

		if len(green_contours[1])>=1:

			green_area_max=0
			#Find 2 biggest areas
			biggest_green=None
			foundGreen=False
			for contorno in red_contours[1]:
				print('Contour len:',len(contorno))
				area=cv2.contourArea(contorno)
				print('Area:',area)
				if area>red_area_max:
					red_area_max=area
					biggest_red=contorno
					foundRed=True
					

			if First:
				x1,y1,dx1,dy1 = cv2.boundingRect(biggest1)

				cv2.rectangle(image,(x1,y1),(x1+dx1,y1+dy1),(0,0,255),2,8)
				
			if Second:
				x2,y2,dx2,dy2=cv2.boundingRect(biggest2)
				alto2=x2+dx2
				ancho2=y2+dy2
				cv2.rectangle(image,(x2,y2),(x2+dx2,y2+dy2),(0,0,255),2,8)

			cv2.imshow('Can buoys',image)
			cv2.waitKey(0)
			if First:
				if Second:
					x=int((x1+x2)/2)
					y=int((y1+y2)/2)
					cv2.circle(binary,(x,y),10,255,-1,8)
					cv2.imshow('binary',binary)
					if len(foundRed)>=1:
						boolRed=True
					else:
						boolRed=False

					if len(foundGreen)>=1:
						boolGreen=True
					else:
						boolGreen=False

					return boolRed,boolGreen,x,y
				else:
					x=x1
					y=y1
					cv2.circle(binary,(x,y),10,255,-1,8)
					cv2.imshow('binary',binary)

					if len(foundRed)>=1:
						boolRed=True
					else:
						boolRed=False

					if len(foundGreen)>=1:
						boolGreen=True
					else:
						boolGreen=False

					return boolRed,boolGreen,x,y

			return False,False,0,0

			'''
			In case finding the 2 biggest area does not work, use polyApprox to search for squares:
			epsilon = 0.1*cv2.arcLength(cnt,True)
	    	approx = cv2.approxPolyDP(cnt,epsilon*perimeter,True)
			if len(approx) == 4:
				# compute the bounding box of the contour and use the
				# bounding box to compute the aspect ratio
				(x, y, w, h) = cv2.boundingRect(approx)
				ar = w / float(h)
	 
				# a square will have an aspect ratio that is approximately
				# equal to one, otherwise, the shape is a rectangle
				shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"





			'''
		
class Speed_Challenge:

	def get_entrance(self,image):
		obstacles,centroid=dbscan_contours.get_obstacles(image,'rg',True,'A2') #Get a centroid of all red and green obstacles	
		x=int(centroid[0]*math.cos(centroid[1]))
		y=int(centroid[0]*math.sin(centroid[1]))
		return [centroid[0],centroid[1],(x,y)] #return distance, degrees and pixels for map image

	def get_blue_buoy(self,image):
		obstacles,centroid=dbscan_contours.get_obstacles(image,'b',False,'A2') #Get a centroid of all red and green obstacles	
		x=int(centroid[0]*math.cos(centroid[1]))
		y=int(centroid[0]*math.sin(centroid[1]))
		return [centroid[0],centroid[1],(x,y)] #return distance, degrees and pixels for map image

class Find_The_Path:
	
	def get_route_from_obstacles(self,boat_map):
		mapa=cv2.cvtColor(boat_map, cv2.COLOR_BGR2GRAY)
		contornos=cv2.findContours(array,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		distance_matrix=np.zeros((len(contours),len(contours)),dtype=np.float32)
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
					dist=spatial.distance.chebyshev(pointA, pointB)
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
				cv2.line(mapa,(pointA[0],pointA[1]),(pointA[0],pointA[1]),255,2,8)


			destination=np.average(centroids,0)

			if (mapa[destination[0]][destination[1]]==255):
				free=np.argwhere(mapa==0)
				destination=closest_node(destination,free)

			h,w=mapa.shape
			ruta=pathfinding.a_star([int(h/2),int(w/2)],destination,mapa)

			return ruta

class Follow_the_Leader:

	def __init__(self):
		#Load the hu moments of the numbers.
		self.number1=[]
		self.number2=[]
		self.number3=[]
		self.number4=[]

	def find_challenge(self,image):
		#Filter by color to find white pixels.
		white_pixels==cv2.inrange(image,[240,240,240],[255,255,255])

	def find_number(self,image,numero1,numbero2):
		#Filter by color to find black pixels.
		black_pixels==cv2.inrange(image,[0,0,0],[10,10,10])
		#Find contours in image.
		contornos=cv2.findContours(array,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		#
		#Compare contours
		for contorno in contornos:
			pass
			match=cv2.matchshape(contorno,self.number1,1,0.0)
			if (match<0.1):
				print('Found number 1')
			match=cv2.matchshape(contorno,self.number2,1,0.0)
			if (match<0.1):
				print('Found number 1')
			match=cv2.matchshape(contorno,self.number3,1,0.0)
			if (match<0.1):
				print('Found number 1')
			match=cv2.matchshape(contorno,self.number4,1,0.0)
			if (match<0.1):
				print('Found number 1')
