'''
	@author Gabriel
'''
import pathfinding as path
import pathfindingv2 as pathv2
import pathfindingv3 as pathv3
import numpy as np
import math
import cv2
import time
import random
from scipy import spatial

x=200
y=200
start=[int(x/2),int(y/2)]
a=random.randint(1,x-1)
b=random.randint(1,y-1)
goal=[a,b]

mapa=np.full((x,y,3),0,dtype=np.uint8)

for a in range(30):
	a=random.randint(1,x-1)
	b=random.randint(1,y-1)
	cv2.circle(mapa,(a,b),15,(255,255,255),-1,8)

cv2.circle(mapa,(start[0],start[1]),15,(0,0,0),-1,8)

mapa1=mapa.copy()
mapa2=mapa.copy()
mapa3=mapa.copy()

'''
ruta1=path.a_star(start,goal,mapa1)
for punto in ruta1:
	mapa1[punto[0]][punto[1]]=[0,0,255]
cv2.imshow('Pathfinding v1',mapa1)
'''
ruta2=pathv2.a_star(start,goal,mapa)

for punto in ruta2:
	mapa2[punto[0]][punto[1]]=[0,0,255]
cv2.imshow('Pathfinding v2',mapa2)


ruta3=pathv3.a_star(start,goal,mapa,2)

for punto in ruta3:
	mapa3[punto[0]][punto[1]]=[0,0,255]
cv2.imshow('Pathfinding v3 (theads)',mapa3)

cv2.waitKey(0)