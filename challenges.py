import Jetson.dbscan_contours
import math
import pathfindingv2 as pathfinding
from pathfinding import closest_node
from scipy import spatial
import numpy as np
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import cv2

red_low=np.array([  0,         3.12572092,  85.37949534]) #red buoy cans bgr
red_upper=np.array([  32.33085987,   43.29067253,  181.69263581])

green_low_close=np.array([ 93.87969614,  86.42179145,  33.96279703])  #green buoy cans bgr
green_upper_close=np.array([ 137.11582457,  127.58940676,   66.06295885])

green_low_far=np.array([ 53.95902545,  55.10921768,  31.3839107 ])  #green buoy cans bgr
green_upper_far=np.array([ 70.69097455,  75.92411565,  47.13275597])


'''
red_low=np.array([  98.47434486,  164.69852521,   81.62388293]) #red buoy cans hsv
red_upper=np.array([ 210.56366683,  247.74299526,  164.24161415])

green_low_close=np.array([  92.28906994,  131.67216667,   93.69534632])  #green buoy cans hsv
green_upper_close=np.array([  95.14966524,  157.14700329,  137.13864577])

green_low_far=np.array([  75.15769883,  114.19952355,  103.50299968])  #green buoy cans hsv
green_upper_far=np.array([  82.4705063,   130.97996363,  111.25341058])
'''

def nothing(x):
	pass

minVal=0
maxVal=254
cv2.namedWindow('Canny')
cv2.createTrackbar('minVal','Canny',167,255,nothing)
cv2.createTrackbar('maxVal','Canny',170,255,nothing)


class Autonomous_Navigation:

	def get_destination(self,image):

		hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
		gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		canny=cv2.Canny(gray,minVal,maxVal,True)
		cv2.imshow('Canny',canny)
		cv2.waitKey(500)
		red=cv2.inRange(image,red_low,red_upper)
		green_close=cv2.inRange(image,green_low_close,green_upper_close)
		green_far=cv2.inRange(image,green_low_far,green_upper_far)
		


		kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
		'''
		red=cv2.inRange(hsv,red_low,red_upper)
		green_close=cv2.inRange(hsv,green_low_close,green_upper_close)
		green_far=cv2.inRange(hsv,green_low_far,green_upper_far)
		
		'''

		red = cv2.morphologyEx(red, cv2.MORPH_CLOSE, kernel)
		green_close = cv2.morphologyEx(green_close, cv2.MORPH_CLOSE, kernel)
		green_far = cv2.morphologyEx(green_far, cv2.MORPH_CLOSE, kernel)
		binary=np.bitwise_or(green_close,green_far)



		red_contours=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		green_contours=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		binary=np.bitwise_or(binary,red)
		foundRed=False
		foundGreen=False
		if len(red_contours[1])>=1:

			red_area_max=0
			#Find 2 biggest areas
			biggest_red=None
			for contorno in red_contours[1]:
				#print('Contour len:',len(contorno))
				area=cv2.contourArea(contorno)
				#print('Area:',area)
				if area>100:
					if area>red_area_max:
						red_area_max=area
						biggest_red=contorno
						foundRed=True

		if len(green_contours[1])>=1:

			green_area_max=0
			#Find 2 biggest areas
			biggest_green=None
			for contorno in green_contours[1]:
				#print('Contour len:',len(contorno))
				area=cv2.contourArea(contorno)
				#print('Area:',area)
				if area>100:
					if area>green_area_max:
						green_area_max=area
						biggest_green=contorno
						foundGreen=True
					

		if foundRed:
			x1,y1,dx1,dy1 = cv2.boundingRect(biggest_red)
			print(x1+dx1,y1+dy1)
			cv2.rectangle(image,(x1,y1),(x1+dx1,y1+dy1),(0,0,255),-1,8)
			
		if foundGreen:
			x2,y2,dx2,dy2=cv2.boundingRect(biggest_green)
			print(x2+dx2,y2+dy2)
			cv2.rectangle(image,(x2,y2),(x2+dx2,y2+dy2),(0,255,0),-1,8)

		cv2.imshow('Can buoys',image)
		#cv2.waitKey(0)
		if foundRed and foundGreen:
			x=int((x1+x2)/2)
			y=int((y1+y2)/2)
			cv2.circle(image,(x,y),10,(255,255,255),-1,8)
			cv2.imshow('image',image)
			return foundRed,foundGreen,x,y
		else:
			if foundRed:
				x=x1
				y=y1
				cv2.circle(image,(x,y),10,(255,255,255),-1,8)
				cv2.imshow('image',image)
			elif foundGreen:
				x=x2
				y=y2
				cv2.circle(image,(x,y),10,(255,255,255),-1,8)
				cv2.imshow('image',image)
				return foundRed,foundGreen,x,y

				

		return False,False,0,0
		
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
