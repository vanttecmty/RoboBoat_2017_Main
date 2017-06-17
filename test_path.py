import pathfinding as path
import pathfindingv2 as pathv2
import numpy as np
import math
import cv2
import time
import random
from scipy import spatial

x=400
y=400
start=[int(x/2),int(y/2)]
a=random.randint(1,x-1)
b=random.randint(1,y-1)
goal=[0,200]
'''
mapa=np.full((x,y,3),0,dtype=np.uint8)

for a in range(30):
	a=random.randint(1,x-1)
	b=random.randint(1,y-1)
	cv2.circle(mapa,(a,b),15,(255,255,255),-1,8)

cv2.circle(mapa,(start[0],start[1]),15,(0,0,0),-1,8)
'''


'''
ruta1=path.a_star(start,goal,mapa1)
for punto in ruta1:
	mapa1[punto[0]][punto[1]]=[0,0,255]
cv2.imshow('Pathfinding v1',mapa1)
'''
mapa=cv2.imread('obstacles.jpeg')
ruta2=pathv2.a_star(start,goal,mapa)

for punto in ruta2:
	mapa[punto[0]][punto[1]]=[0,0,255]
cv2.imshow('Pathfinding v2',mapa)
cv2.waitKey(0)
