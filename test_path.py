import pathfinding as path
import pathfindingv2 as pathv2

x=400
y=400
start=[200,200]
a=random.randint(1,x-1)
b=random.randint(1,y-1)
goal=[99,0]
mapa=np.full((x,y,3),0,dtype=np.uint8)

for a in range(30):
	a=random.randint(1,x-1)
	b=random.randint(1,y-1)
	cv2.circle(mapa,(a,b),15,(255,255,255),-1,8)
cv2.circle(mapa,(goal[1],goal[0]),15,(255,255,255),-1,8)
ruta=path.a_star(start,goal,mapa)
ruta2=pathv2.a_star(start,goal,mapa)
for punto in ruta:
	mapa[punto[0]][punto[1]]=[0,0,255]

cv2.imshow('ruta',mapa)
cv2.waitKey(0)
