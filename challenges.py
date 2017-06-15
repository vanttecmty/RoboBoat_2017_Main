import Jetson.dbscan_contours
import math


class autonomous_navigation():

	def __init__(self):
		self.set_camera()

	def get_destination(self,image):
		centroid=dbscan_contours.get_obstacles(image,'rg',True) #Get a centroid of all red and green obstacles	
		x=int(centroid[0]*math.cos(centroid[1]))
		y=int(centroid[0]*math.sin(centroid[1]))
		return [centroid[0],centroid[1],(x,y)] #return distance, degrees and pixels for map image
 
class speed_challenge():

	def get_entrance(self,image):
		centroid=dbscan_contours.get_obstacles(image,'rg',True) #Get a centroid of all red and green obstacles	
		x=int(centroid[0]*math.cos(centroid[1]))
		y=int(centroid[0]*math.sin(centroid[1]))
		return [centroid[0],centroid[1],(x,y)] #return distance, degrees and pixels for map image

	def get_blue_buoy(self,image):
		centroid=dbscan_contours.get_obstacles(image,'b',False) #Get a centroid of all red and green obstacles	
		x=int(centroid[0]*math.cos(centroid[1]))
		y=int(centroid[0]*math.sin(centroid[1]))
		return [centroid[0],centroid[1],(x,y)] #return distance, degrees and pixels for map image

class find_the_path():

	def __init__(self):
		a

	#Ask the jetson to use frcnn.
	def ask_image(self):
		b

	def return_path(self,):
		return 0



