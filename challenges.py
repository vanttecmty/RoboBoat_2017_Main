import Jetson.dbscan_contours
import math
import pathfindingv2 as pathfinding
from pathfinding import closest_node
from scipy import spatial
import numpy as np
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import cv2

class Autonomous_Navigation:

	def __init__(self):
		self.red_lower_bounds=[]
		self.red_upper_bounds=[]
		with open('red_bounds.txt', 'r') as f:
			content = f.readlines()
		content = [x.strip('\n') for x in content]	
		for line in content:
			split=line.split(',')
			#print(split)
			if (len(split)>1):
				self.red_lower_bounds.append(np.array([float(split[0]),float(split[1]),float(split[2])]))
				self.red_upper_bounds.append(np.array([float(split[3]),float(split[4]),float(split[5])]))
		

		self.green_lower_bounds=[]
		self.green_upper_bounds=[]
		with open('green_bounds.txt', 'r') as f:
			content = f.readlines()
		content = [x.strip('\n') for x in content]	
		for line in content:
			split=line.split(',')
			if (len(split)>1):
				self.green_lower_bounds.append(np.array([float(split[0]),float(split[1]),float(split[2])]))
				self.green_upper_bounds.append(np.array([float(split[3]),float(split[4]),float(split[5])]))

	def get_destination(self,image):
		h,w,c=image.shape
		red_binary=np.zeros((h,w),dtype=np.uint8)
		green_binary=np.zeros((h,w),dtype=np.uint8)
		image2=image.copy()
		hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
		kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
		for i,lower in enumerate(self.green_lower_bounds):
			green_hsv_filtered=cv2.inRange(hsv,lower,self.green_upper_bounds[i])
			#print(lower)
			#print(self.green_upper_bounds[i])
			green1 = cv2.morphologyEx(green_hsv_filtered, cv2.MORPH_OPEN, kernel)
			green_binary=np.bitwise_or(green_binary,green1)


		for i,lower in enumerate(self.red_lower_bounds):
			#print(lower)
			#print(self.red_upper_bounds[i])
			red_hsv_filtered=cv2.inRange(image,lower,self.red_upper_bounds[i])
			red1 = cv2.morphologyEx(red_hsv_filtered, cv2.MORPH_OPEN, kernel)
			red_binary=np.bitwise_or(red_binary,red1)

		red_contours=cv2.findContours(red_binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		green_contours=cv2.findContours(green_binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		binary=np.bitwise_or(green_binary,red_binary)
		foundRed=False
		foundGreen=False
		if len(red_contours[1])>=1:

			red_area_max=0
			#Find 2 biggest areas
			biggest_red=None
			for contorno in red_contours[1]:
				#print('Contour len:',len(contorno))
				area=cv2.contourArea(contorno)
				x1,y1,dx1,dy1 = cv2.boundingRect(contorno)
				#print('Area:',area)
				if area>2 and y1>120:
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
				if area>20:
					if area>green_area_max:
						green_area_max=area
						biggest_green=contorno
						foundGreen=True
					

		if foundRed:
			x1,y1,dx1,dy1 = cv2.boundingRect(biggest_red)
			if  float(dy1)/dx1<1.2:
				foundRed=False
			#print(x1+dx1,y1+dy1)
			cv2.rectangle(image2,(x1,y1),(x1+dx1,y1+dy1),(0,0,255),-1,8)
			
		if foundGreen:
			x2,y2,dx2,dy2=cv2.boundingRect(biggest_green)
			if  float(dy2)/dx2<1.2:
				foundGreen=False
			#print(x2+dx2,y2+dy2)
			cv2.rectangle(image2,(x2,y2),(x2+dx2,y2+dy2),(0,255,0),-1,8)

		#cv2.waitKey(0)
		if foundRed and foundGreen:
			x=int((x1+x2)/2)
			y=int((y1+y2)/2)
			cv2.circle(image2,(x,y),10,(255,255,255),-1,8)
			cv2.imshow('image2',image2)
			return foundRed,foundGreen,x,y,image2
		else:
			if foundRed:
				x=x1
				y=y1
				cv2.circle(image2,(x,y),10,(255,255,255),-1,8)
				cv2.imshow('image2',image2)
				return foundRed,foundGreen,x,y,image2
			elif foundGreen:
				x=x2
				y=y2
				cv2.circle(image2,(x,y),10,(255,255,255),-1,8)
				cv2.imshow('image2',image2)
				return foundRed,foundGreen,x,y,image2

				

		return False,False,0,0,image2
		
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

class Automated_Docking:


	def __init__(self):
		#Load the hu moments of the numbers.
		self.number1=[]
		self.number2=[]
		self.number3=[]
		self.white_image=np.array(255)

	def search_number(self,image,number):
		gauss_blur = cv2.GaussianBlur(image,(5,5),0)
		median_blur = cv2.medianBlur(image,5)
		gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		gray_gauss=cv2.cvtColor(gauss_blur,cv2.COLOR_BGR2GRAY)
		gray_median=cv2.cvtColor(median_blur,cv2.COLOR_BGR2GRAY)
		minVal=50
		maxVal=100
		canny=cv2.Canny(gray,minVal,maxVal,True)
		canny_gauss=cv2.Canny(gray_gauss,minVal,maxVal,True)
		canny_median=cv2.Canny(gray_median,minVal,maxVal,True)
		cv2.imshow('Canny',canny)
		cv2.imshow('Canny gauss',canny_gauss)
		cv2.imshow('Canny median',canny_median)
		contours=cv2.findContours(canny,cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
		#print(contours[1])
		if len(contours[1])>1:
			for contorno in contours[1]:
				epsilon = 0.1*cv2.arcLength(contorno,True)
				approx = cv2.approxPolyDP(contorno,epsilon,True)
				#print(len(approx))
				area=cv2.contourArea(contorno)
				if area>50:
					copy=np.full(image.shape,255,dtype=np.uint8)
					cv2.drawContours(copy, contorno, -1, (0,0,255), 3)
					cv2.imshow('copy',copy)
					#cv2.waitKey(0)


		cv2.imshow('image',image)
		#cv2.waitKey(0)


