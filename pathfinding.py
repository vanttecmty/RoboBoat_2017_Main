import numpy as np
import math
import cv2
import time
import random

def euclidean(nodeA,nodeB):
	distance=math.sqrt(pow(abs(nodeA[0]-nodeB[0]),2)+pow(abs(nodeA[1]-nodeB[1]),2))
	return distance

def Astar(start, goal, boat_map):
	
	mapa=cv2.cvtColor(boat_map, cv2.COLOR_BGR2GRAY)

	#Create open and closed nodes.
	closedNodes=[]
	openNodes=[start]

	#create path

	path=[]

	#obtain shape of map
	h,w=mapa.shape

	cv2.circle(mapa,(start[1],start[0]),15,0,-1,8)
	cv2.circle(mapa,(goal[1],goal[0]),15,0,-1,8)
	nombre=str(goal[0])+','+str(goal[1])
	cv2.imshow(nombre,mapa)
	cv2.waitKey(0)
	#cost for going from start to node
	nodes=[start]
	g_evaluations=[euclidean(start,start)]

	currentNode=start
	
	parentNode=[start]
	while len(openNodes)>0:
		
		
		minimum=99999
		f_evaluations=[]
		for node in openNodes:
			if node != start:
				f_eval=g_evaluations[nodes.index(node)]+euclidean(node,goal)
			else:
				f_eval=minimum			
			f_evaluations.append(f_eval)
			if f_eval<minimum:
				minimum=f_eval
				currentNode=node
				path.append(currentNode)
		
	
		#print 'Open:', openNodes
		#print 'Closed:',closedNodes
		#print 'Nodes:',nodes
		#print 'g_evaluations:',g_evaluations
		#print 'f_evaluations:',f_evaluations
		#print 'Current node:',currentNode
		#print 'Evaluation:',minimum
		print 'Open len:',len(openNodes)

		#time.sleep(0.5)
		if currentNode == goal:
			print "Found path"
			break

		succesors=[]
		#Add neighbors of current node.
		if (currentNode[0]-1>0 and mapa[currentNode[0]-1][currentNode[1]]==0):	
			succesors.append([currentNode[0]-1,currentNode[1]])
		if (currentNode[1]-1>0 and mapa[currentNode[0]][currentNode[1]-1]==0):	
			succesors.append([currentNode[0],currentNode[1]-1])
		if (currentNode[0]+1<h-1 and mapa[currentNode[0]+1][currentNode[1]]==0):	
			succesors.append([currentNode[0]+1,currentNode[1]])
		if (currentNode[1]+1<w-1 and mapa[currentNode[0]][currentNode[1]+1]==0):	
			succesors.append([currentNode[0],currentNode[1]+1])
	

		if (currentNode[0]-1>0 and currentNode[1]-1>0 and mapa[currentNode[0]-1][currentNode[1]-1]==0):	
				succesors.append([currentNode[0]-1,currentNode[1]-1])
		if (currentNode[0]+1<h-1 and currentNode[1]+1<w-1 and mapa[currentNode[0]+1][currentNode[1]+1]==0):	
				succesors.append([currentNode[0]+1,currentNode[1]+1])
		if (currentNode[0]+1<h-1 and currentNode[1]-1>0 and mapa[currentNode[0]+1][currentNode[1]-1]==0):	
				succesors.append([currentNode[0]+1,currentNode[1]-1])
		if (currentNode[0]-1>0 and currentNode[1]+1<w-1 and mapa[currentNode[0]-1][currentNode[1]+1]==0):	
				succesors.append([currentNode[0]-1,currentNode[1]+1])

		#print(succesors)
		if (len(succesors)>=1):
			for node_succesor in succesors:
				current_succesor_cost=g_evaluations[0]+euclidean(currentNode,node_succesor)
				
				if (node_succesor in openNodes):
					if (g_evaluations[nodes.index(node_succesor)]<=current_succesor_cost): 
						continue
				elif node_succesor in closedNodes:
					if (g_evaluations[nodes.index(node_succesor)]<=current_succesor_cost):
						continue
					openNodes.append(node_succesor)
					closedNodes.remove(node_succesor)
				else:
					openNodes.append(node_succesor)
					nodes.append(node_succesor)
					parentNode.append(currentNode)
					g_evaluations.append(current_succesor_cost)

				index=nodes.index(node_succesor)
				#print index
				#print 'len:',len(parentNode)
				#print 'len g:',len(g_evaluations)
				g_evaluations[index]=current_succesor_cost
				#parentNode[index]=currentNode
		
		closedNodes.append(currentNode)	
		openNodes.remove(currentNode)	


	
	try:
		last=path[-1]
	except IndexError: 
			print path
			cv2.circle(boat_map,(h/2,w/2),5,(0,255,0),-1,8)
			cv2.imshow('map',boat_map)
			cv2.waitKey(0)
	myparentparent=None
	result=[last]
	while(last!=start):
		boat_map[last[0]][last[1]]=[0,0,255]
		#cv2.imshow('boat_map',boat_map)
		parent_index=nodes.index(last)
		parent=parentNode[parent_index]
		#print ''
		#print 'Last:',last
		#print 'Parent:',parent
		last=parent
		result.append(last)
	return result
		
x=400
y=400
start=[x/2,y/2]
a=random.randint(1,x-1)
b=random.randint(1,y-1)
goal=[a,b]
mapa=np.full((x,y,3),0,dtype=np.uint8)
for a in range(0,50):
	x1=random.randint(0,x-1)
	y1=random.randint(0,y-1)
	cv2.circle(mapa,(x1,y1),15,(255,255,255),-1,8)
cv2.line(mapa,(100,150),(300,150),(255,255,255),1,8)
start_time=time.time()
ruta=Astar(start,goal,mapa)
#print ruta
print start, goal
print time.time() - start_time
mapa[start[0]][start[1]]=[255,255,255]
mapa[goal[0]][goal[1]]=[255,255,255]
cv2.circle(mapa,(start[0],start[1]),15,(0,255,0),-1,8)
cv2.circle(mapa,(goal[1],goal[0]),15,(0,255,255),-1,8)
for punto in ruta:
	mapa[punto[0]][punto[1]]=[0,0,255]
cv2.imshow('mapa',mapa)
cv2.waitKey(0)



