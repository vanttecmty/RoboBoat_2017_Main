'''
	@author Gabriel
'''
import numpy as np
import cv2
import random
from scipy import misc
from scipy.ndimage import rotate

pixel_buoy=6
alto=58
ancho=34


def new_map(x,y):
	mapa=np.full((x,y,3),0,dtype=np.uint8)
	return mapa
	
def plot_map(mapa):
	copia=mapa.copy()
	h,w,c=mapa.shape
	x1=int(h/2-(ancho/2));
	y1=int(w/2-(alto/2));
	x2=int(h/2+(ancho/2));
	y2=int(w/2+(alto/2));
	cx=int(h/2)
	cy=int(w/2)
	cv2.rectangle(copia,(x1,y1),(x2,y2),(0,255,0),1,8)
	cv2.line(copia,(cx,cy),(cx,cy-25),(0,0,255),1,8)
	cv2.imshow('mapa',copia)
	cv2.waitKey(0)

def rotate_map(mapa, angle):
	#mapa=misc.imrotate(mapa,angle,interp='nearest')
	mapa = rotate(mapa, angle, mode = 'constant',reshape=False)	
	return mapa

def translate_map(mapa,dx,dy):
	cols,rows,ch=mapa.shape
	M=np.float32([[1,0,dx],[0,1,dy]])
	mapa=cv2.warpAffine(mapa,M,(cols,rows))
	return mapa

def add_buoy(mapa,x,y):
	cv2.circle(mapa,(x,y),pixel_buoy,255,-1,8)

def add_lidar(mapa,points):
	for point in points:
		mapa[point[0]][point[1]]=[0,255,0]
	return mapa


#Nuevo mapa
boat_map=new_map(400,400)

#Dibujar boya
add_buoy(boat_map,100,150)
add_buoy(boat_map,100,150)

#Mostrar mapa
plot_map(boat_map)

#Rotar mapa
for angulo in range(0,180,10):
	boat_map=rotate_map(boat_map,5)
	plot_map(boat_map)

#Trasladar mapa 1 en x
for x in range(0,10):
	boat_map=translate_map(boat_map,5,0)
	plot_map(boat_map)

#Trasladar mapa -1 en y 
for y in range(0,30):
	boat_map=translate_map(boat_map,0,-5)
	plot_map(boat_map)

