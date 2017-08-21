'''
	@author Gabriel Sahagún
'''

import numpy as np
import math
import cv2
import time
import random

def euclidean(nodeA,nodeB):
	distance=math.sqrt(pow(abs(nodeA[0]-nodeB[0]),2)+pow(abs(nodeA[1]-nodeB[1]),2))
	return distance

def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)


def a_star(start, goal, boat_map):
	
	mapa=cv2.cvtColor(boat_map, cv2.COLOR_BGR2GRAY)


	path_start=time.time()
	#Create open and closed nodes.
	closedNodes=[]
	openNodes=[start]

	#create path

	path=[]

	#obtain shape of map
	h,w=mapa.shape
	
	if (mapa[goal[0]][goal[1]]==255):
		print('Finding new goal')
		free=np.argwhere(mapa==0)
		destino=closest_node(goal,free)
		print(free[destino])
		goal[0]=free[destino][0]
		goal[1]=free[destino][1]

	#cv2.circle(mapa,(start[1],start[0]),15,0,-1,8)
	
	#nombre=str(goal[0])+','+str(goal[1])
	#cv2.imshow(nombre,mapa)
	#cv2.waitKey(0)
	#cost for going from start to node
	nodes=[start]
	g_evaluations=[euclidean(start,start)]

	currentNode=start
	
	parentNode=[start]

	mapa2=mapa.copy()
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
				mapa2[currentNode[0]][currentNode[0]]=255
				#cv2.imshow('search',mapa2)
				#cv2.waitKey(1)
		
	
		#print 'Open:', openNodes
		#print 'Closed:',closedNodes
		#print 'Nodes:',nodes
		#print 'g_evaluations:',g_evaluations
		#print 'f_evaluations:',f_evaluations
		#print 'Current node:',currentNode
		#print 'Evaluation:',minimum
		#print ('Open len:',len(openNodes));

		#time.sleep(0.5)
		if currentNode == goal:
			#print ("Found path");
			break

		succesors=[]
		#Add neighbors of current node.
		print
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

		#print(succesors)
		if (len(succesors)>=1):
			for node_succesor in succesors:	
				currentNode_cost=g_evaluations[nodes.index(currentNode)]
				current_succesor_cost=currentNode_cost+euclidean(currentNode,node_succesor)
				
				if (node_succesor in openNodes):
					if (g_evaluations[nodes.index(node_succesor)]<=current_succesor_cost): 
						continue

						index=nodes.index(node_succesor)
						g_evaluations[index]=current_succesor_cost
				elif node_succesor in closedNodes:
					if (g_evaluations[nodes.index(node_succesor)]<=current_succesor_cost):
						continue
					openNodes.append(node_succesor)
					closedNodes.remove(node_succesor)
					index=nodes.index(node_succesor)
					g_evaluations[index]=current_succesor_cost
				else:
					openNodes.append(node_succesor)
					nodes.append(node_succesor)
					parentNode.append(currentNode)
					g_evaluations.append(current_succesor_cost)

				#print index
				#print 'len:',len(parentNode)
				#print 'len g:',len(g_evaluations)
				#parentNode[index]=currentNode
		
		closedNodes.append(currentNode)	
		openNodes.remove(currentNode)	
	

	

	last = path[-1];
	
	myparentparent=None
	result=[last]
	while(last!=start):
		boat_map[last[0]][last[1]]=[0,0,255]
		##cv2.imshow('boat_map',boat_map)
		parent_index=nodes.index(last)
		parent=parentNode[parent_index]
		#print ''
		#print 'Last:',last
		#print 'Parent:',parent
		last=parent
		result.append(last)

	print ('Pathv1 found in ',time.time()-path_start)
	return(result);

