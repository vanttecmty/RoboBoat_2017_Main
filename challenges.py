import Jetson.dbscan_contours
import math
import pathfindingv2 as pathfinding
from pathfinding import closest_node
from scipy import spatial
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import cv2

red_low=np.array([   0,            0,          115.39777469])
red_upper=np.array([  43.71792393,   47.60779081,  239.44837916])

green_low=np.array([  71.49535277,  150.41099537,    2.82631499])
green_upper=np.array([ 144.98700017,  229.38312228,   86.85799873])

class Autonomous_Navigation:

	def __init__(self):
		self.set_camera()

	def get_destination(self,image):

		red=cv2.inRange(image,red_low,red_upper)
		green=cv2.inRange(image,green_low,green_upper)
		binary=np.bitwise_or(red,green)
		contornos=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		


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
		foundRed=np.argwhere(red==255)
		foundGreen=np.argwhere(green==255)
		if len(contornos)>=1:

			area_max1=0
			area_max2=0
			#Find 2 biggest areas
			biggest1=None
			biggest2=None
			First=False
			Second=False
			for contorno in contornos:
				area=cv2.contourArea(contorno)
				print('Area:',area)
				if area>area_max:
					area_max=area
					biggest1=contorno
					First=True
				elif area>area_max2:
					area_max2=area
					biggest2=contorno
					Second=True



			if biggest1!=None:
				x1,y1,dx1,dy1 = cv2.boundingRect(biggest1)
				alto1=x1+dx1
				ancho1=y1+dy1
				cv2.rectangle(image,(x1,y1),(x1+dx1,y1+dy1),(0,0,255),2,8)
				
			if biggest2!=None:
				x2,y2,dx2,dy2=cv2.boundingRect(biggest2)
				alto2=x2+dx2
				ancho2=y2+dy2
				cv2.rectangle(image,(x2,y2),(x2+dx2,y2+dy2),(0,0,255),2,8)

			cv2.imshow('Can buoys',image)
			if First:
				if Second:
					x=(x1+alto1+x2+alto2)/2
					y=(y1+y2+ancho2)/2
					if len(foundRed)>=1:
						boolRed=True
					else:
						boolRed=False

					if len(foundGreen)>=1:
						boolGreen=True
					else:
						boolGreen=False

					return boolRed,boolGreen,x,y
				else
					x=x1+alto1
					y=(y1+ancho2)/2

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
