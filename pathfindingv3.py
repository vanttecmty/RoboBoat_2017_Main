import numpy as np
import math
import cv2
import time
import random
from scipy import spatial
import threading

lock=threading.Lock()
p=1.5

nodesThread1=[]
nodesThread2=[]

startRoute=[]
goalRoute=[]
intersection_node=[]
reachedGoal=False
threadNumber=0

def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)


def explore_nodes(boat_map,start,goal,p,number):
	global nodesThread1, nodesThread2
	global startRoute, goalRoute
	global reachedGoal, threadNumber
	mapa=cv2.cvtColor(boat_map, cv2.COLOR_BGR2GRAY)
	mapa2=boat_map.copy()
	

	openNodes=[start]
	closedNodes=[]
	parentNode=[start]
	nodes=[start]
	dist2startOpen=np.zeros(1)
	dist2startAll=np.zeros(1)
	dist2goal=np.array(spatial.distance.chebyshev(start, goal))
	total_dist=np.add(dist2startOpen,dist2goal)

	h,w=mapa.shape
	while len(openNodes)>0:
		#print('OpenNodes:',openNodes)
		#Calculate distances
		total_dist=np.add(dist2startOpen,dist2goal)
		#Get node closest to goal.
		#print('Dist2start:',dist2startOpen)
		#print('Dist2goal:',dist2goal)
		#print('Heuristics:',total_dist)
		index=np.argmin(total_dist)
		currentNode=openNodes[index]
		#print('Thread:',number,'currentNode:',currentNode)
		#time.sleep(1)
		#mapa2[currentNode[0]][currentNode[1]]=[0,0,255]
		#cv2.imshow('search',mapa2)
		#cv2.waitKey(1)
		
		with lock:
			if (number==1):
				nodesThread1=nodes
			else:
				nodesThread2=nodes
			if currentNode == goal:
				reachedGoal=True
				threadNumber=number
				break

			else:
				if currentNode in nodesThread1 and currentNode in nodesThread2:
					break

		succesors=[]
		if (currentNode[0]-1>=0 and mapa[currentNode[0]-1][currentNode[1]]==0):			
			succesors.append([currentNode[0]-1,currentNode[1]])

		if (currentNode[1]-1>=0 and mapa[currentNode[0]][currentNode[1]-1]==0):	
			succesors.append([currentNode[0],currentNode[1]-1])

		if (currentNode[0]+1<=h-1 and mapa[currentNode[0]+1][currentNode[1]]==0):	
			succesors.append([currentNode[0]+1,currentNode[1]])

		if (currentNode[1]+1<=w-1 and mapa[currentNode[0]][currentNode[1]+1]==0):	
			succesors.append([currentNode[0],currentNode[1]+1])

		if (currentNode[0]-1>=0 and currentNode[1]-1>=0 and mapa[currentNode[0]-1][currentNode[1]-1]==0):	
			succesors.append([currentNode[0]-1,currentNode[1]-1])

		if (currentNode[0]+1<=h-1 and currentNode[1]+1<=w-1 and mapa[currentNode[0]+1][currentNode[1]+1]==0):	
			succesors.append([currentNode[0]+1,currentNode[1]+1])

		if (currentNode[0]+1<=h-1 and currentNode[1]-1>=0 and mapa[currentNode[0]+1][currentNode[1]-1]==0):	
			succesors.append([currentNode[0]+1,currentNode[1]-1])

		if (currentNode[0]-1>=0 and currentNode[1]+1<=w-1 and mapa[currentNode[0]-1][currentNode[1]+1]==0):	
			succesors.append([currentNode[0]-1,currentNode[1]+1])


		if (len(succesors)>=1):
			current_index=nodes.index(currentNode)
			#print('Nodes:',nodes)
			#print('Index:',current_index)
			distCurrent=dist2startAll[current_index]
			#print('Distance of parent to start',dist)
			for node_succesor in succesors:
				#print('Dist',distCurrent)
				current_succesor_cost=distCurrent+1
				#print('Current distance',current_succesor_cost)				
				if (node_succesor in openNodes):
					if (dist2startAll[nodes.index(node_succesor)]<=current_succesor_cost): 
						continue

					index=openNodes.index(node_succesor)
					dist2startOpen[index]=current_succesor_cost
					index=nodes.index(node_succesor)
					dist2startAll[index]=current_succesor_cost
					parentNode[index]=currentNode


				elif node_succesor in closedNodes:
					if (dist2startAll[nodes.index(node_succesor)]<=current_succesor_cost):
						continue
					openNodes.append(node_succesor)
					index=nodes.index(node_succesor)
					dist2startAll[index]=current_succesor_cost
					dist2startOpen=np.append(dist2startOpen,current_succesor_cost)
					dist=np.linalg.norm(np.asarray(node_succesor)-np.asarray(goal))
					dist2goal=np.append(dist2goal,dist)
					closedNodes.remove(node_succesor)
					parentNode[index]=currentNode
				else:
					openNodes.append(node_succesor)
					nodes.append(node_succesor)
					#parentNode.append(currentNode)
					dist2startOpen=np.append(dist2startOpen,current_succesor_cost)
					dist=spatial.distance.chebyshev(node_succesor, goal)*(1.0+p)
					dist2goal=np.append(dist2goal,dist)
					dist2startAll=np.append(dist2startAll,current_succesor_cost)
					parentNode.append(currentNode)
		
		closedNodes.append(currentNode)	
		index=openNodes.index(currentNode)
		dist2startOpen=np.delete(dist2startOpen,index)
		dist2goal=np.delete(dist2goal,index)
		openNodes.remove(currentNode)
	
	#print(parentNode)
	route=[]
	last=parentNode[-1]
	while last!=start:
		index=nodes.index(last)
		route.append(last)
		parent=parentNode[index]
		#print('Last:',last)
		#print('New:',parent)
		last=parent
		
	if number==1:
		startRoute=route
	else:
		goalRoute=route
	

def a_star(start, goal, boat_map,p):
	mapa=cv2.cvtColor(boat_map, cv2.COLOR_BGR2GRAY)

	mapa2=boat_map.copy()
	path_start=time.time()
	
	if (mapa[goal[0]][goal[1]]==255):
		print('Finding new goal')
		free=np.argwhere(mapa==0)
		destino=closest_node(goal,free)
		print(free[destino])
		goal[0]=free[destino][0]
		goal[1]=free[destino][1]
	
	
	#Create threads here
	startThread=threading.Thread(target=explore_nodes,args=(boat_map,start,goal,p,1))
	goalThread=threading.Thread(target=explore_nodes,args=(boat_map,goal,start,p,2))

	startThread.start()
	goalThread.start()

	startThread.join()
	goalThread.join()
		
	#print(startRoute)
	#print(goalRoute)

	if reachedGoal:
		print('Path found with threads')
		ruta=startRoute+goalRoute
	else:
		print('One thread',threadNumber,' found the path')
		if threadNumber==1:
			ruta=startRoute
		else:
			ruta=goalRoute
	
	print('Pathv3 found in:',time.time()-path_start)
	return ruta
