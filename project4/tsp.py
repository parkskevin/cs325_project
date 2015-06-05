#!/usr/bin/python

#Author: Daniel Bonnin, Kevin Parks, Alex Thomas
#email:  bonnind@onid.oregonstate.edu
#class:  CS325
#Assgn:  Project 4
#Descr:  This program calculates a tour of minimum distance between points on
# 		 Cartesion plane. 
#
#Input:  This program takes a text file as input.
#
#Usage:  Without arguments, the program returns an error on usage
#
#        Usage: python tsp.py (<input filepath>)

import sys #for maxint
import timeit #for timings
import math #for sqrt and round
import argparse #for parsing args
import re #for regex
import math
#Source: tsp-verifier.py from supplied project files
def distance(a,b):
	# a and b are integer pairs (each representing a point in a 2D, integer grid)
	# Euclidean distance rounded to the nearest integer:
	dx = a[0]-b[0]
	dy = a[1]-b[1]
	if dx == 0 and dy == 0:
		return sys.maxint
	#return int(math.sqrt(dx*dx + dy*dy)+0.5) # equivalent to the next line
	return int(round(math.sqrt(dx*dx + dy*dy)))
	
#Source: tsp-verifier.py from supplied project files
def readinstance(filename):
	# each line of input file represents a city given by three integers:
	# identifier x-coordinate y-coordinate (space separated)
	# city identifiers are always consecutive integers starting with 0
	# (although this is not assumed here explicitly,
	#    it will be a requirement to match up with the solution file)
	f = open(filename,'r')
	line = f.readline()
	cities = []
	while len(line) > 1:
		lineparse = re.findall(r'[^,;\s]+', line)
		cities.append([int(lineparse[1]),int(lineparse[2])])
		line = f.readline()
	f.close()
	return cities

def adjList(cities):
	# generate adjacency list from cities list.
	# input: list of coordinate pairs lists
	# output: 2d list of distances. 
	# adj[i][j] where i is the city id and j is neighbor city id
	n = len(cities)
	adj = [[0 for i in range(n)] for j in range(n)]
	for i in range(n):
		if not (i % 1000):
			print "calculating adjList" + str(i) + "/" + str(n)
		for j in range(i, n, 1):
			adj[i][j] = adj[j][i] = distance(cities[i], cities[j])
	return adj

def prims(adj):
	#generate minimum spanning tree of coordinates in cities
	treeV = []
	treeE = []
	treeV.append(0) 
	totalMaxDistance = max([max(x) for x in adj])
	shortestEdges = [] 
	#Tuple of shortest edges in V: (Idx into V, idx of nearest neighbor, dist)
	shortestEdges.append([0, adj[0].index(min(adj[0])), min(adj[0])])
	while len(treeV) < len(adj):
		print "lenth of treeV: " + str(len(treeV))
		#Check for shortest of each vertex's shortest edges
		for i, j in enumerate(shortestEdges): 
			counter = 0
			while j[1] in treeV and counter < len(adj):  #neighbor is in treeV
				counter += 1
				adj[j[0]][j[1]] = sys.maxint #Set dist to neighbor to maxint
				newMinEdge = min(adj[j[0]])  #dist to new closest neighbor
				#Reset shortest edge for member of treeV
				if newMinEdge > totalMaxDistance / 4:
					shortestEdges.pop(i)
				else:	
					shortestEdges[i][1] = adj[j[0]].index(newMinEdge)
					shortestEdges[i][2] = newMinEdge

		#list of distances in shortestEdges
		distanceList = [i[2] for i in shortestEdges]
		#origin vertex for min edge 
		edgeOut = shortestEdges[distanceList.index(min(distanceList))][0]
		#destination vertex for min edge; newest member of treeV
		edgeIn = shortestEdges[distanceList.index(min(distanceList))][1]
		#calculate shortest edge from new vertex; add to shortestEdges
		shortestEdges.append([edgeIn, adj[edgeIn].index(min(adj[edgeIn])), min(adj[edgeIn])])
		#Add newest vertex
		treeV.append(edgeIn)
		for i, j in enumerate(shortestEdges):
			if j[1] == edgeIn:
				adj[j[0]][j[1]] = sys.maxint #Set dist to neighbor to maxint
				newMinEdge = min(adj[j[0]])  #dist to new closest neighbor
				#Reset shortest edge for member of treeV
				shortestEdges[i][1] = adj[j[0]].index(newMinEdge)
				shortestEdges[i][2] = newMinEdge


		#Add newest edge
		treeE.append((edgeOut, edgeIn))
	
	return (treeV, treeE)

def preOrderWalk(mst):
	#build new adj list from tree data
	adj = [[]for i in mst[0]]
	outV = [i[0] for i in mst[1]]
	inV = [i[1] for i in mst[1]]
	for i, j in enumerate(mst[0]):
		adj[mst[0][i]] = ([inV[k] for k, x in enumerate(outV) if x == j])

	# #get the walk order
	order = []
	order = findAdj(adj, 0)
	order.append(0)
	return order

#base case: if the node is a leaf, add it, return
#recursive case: recursively add each child (similar to left-child, then right-child, etc)	
def findAdj(adj, start):
	suborder = []
	suborder.append(start)
	while adj[start]:
		suborder += findAdj(adj, adj[start].pop(0))
	return suborder
	
def outputResults(cities, cityOrder, outFile):

	dist = 0
	for i in range(1, len(cityOrder), 1):
		dist += distance(cities[cityOrder[i]], cities[cityOrder[i - 1]])

	#need route to root added since can't be in cityOrder list for verifier
	# dist += distance(cities[cityOrder[len(cityOrder)-1]], cities[cityOrder[0]])
	outFile.write(str(dist) + "\n")

	for i in range(len(cityOrder)-1):
		outFile.write(str(cityOrder[i]) + "\n")

# def matlabGraph(cities, mst):
# 	graphFile = open("matlabGraph.txt", 'w')
# 	graphFile.write("x=[")
# 	for i in range(len(cities)):
# 		graphFile.write(str(cities[mst[0][i]][0]) + " ")
# 	graphFile.write("];\n")
# 	graphFile.write("y=[")
# 	for i in range(len(cities)):
# 		graphFile.write(str(cities[mst[0][i]][1]) + " ")
# 	graphFile.write("];\n")
# 	graphFile.write("hold on;\n")
# 	graphFile.write("scatter(x, y)\n")
# 	x = []
# 	y = []
# 	for i in range(len(mst[1])):
# 		x.append([cities[mst[1][i][0]][0],cities[mst[1][i][1]][0]])
# 		y.append([cities[mst[1][i][0]][1],cities[mst[1][i][1]][1]])

# 	for i in range(len(mst[1])):
# 		graphFile.write("plot([" + str(x[i][0]) + " " + str(x[i][1]) + \
# 			"],[" + str(y[i][0]) + " " + str(y[i][1]) + "]);\n")

# 	graphFile.close()

def matlabGraph(cities, cityOrder):
	graphFile = open("matlabGraph.txt", 'w')
	graphFile.write("x=[")
	for i in range(len(cities)):
		graphFile.write(str(cities[i][0]) + " ")
	graphFile.write("];\n")
	graphFile.write("y=[")
	for i in range(len(cities)):
		graphFile.write(str(cities[i][1]) + " ")
	graphFile.write("];\n")
	graphFile.write("hold on;\n")
	graphFile.write("scatter(x, y)\n")
	x = []
	y = []
	for i in range(1, len(cityOrder), 1):
		x.append([cities[cityOrder[i-1]][0],cities[cityOrder[i]][0]])
		y.append([cities[cityOrder[i-1]][1],cities[cityOrder[i]][1]])
	for i in range(len(x)):
		graphFile.write("plot([" + str(x[i][0]) + " " + str(x[i][1]) + \
			"],[" + str(y[i][0]) + " " + str(y[i][1]) + "]);\n")

	graphFile.close()

def calcTspLarge(cities):
	x = [i[0] for i in cities]
	y = [i[1] for i in cities]
	midX = (max(x) + min(x)) / 3
	midY = (max(y) + min(y)) / 3
	sections = [[] for i in range(9)]
	adjLists = [[] for i in range(9)]
	msts = [[] for i in range(9)]
	print "splitting graph"
	for i in range(len(cities)):
		if x[i] < midX and y[i] < midY:
			sections[0].append(cities[i])
		elif x[i] < midX and y[i] < 2 * midY:
			sections[1].append(cities[i])
		elif x[i] < midX:
			sections[2].append(cities[i])
		elif x[i] < 2 * midX and y[i] < midY:
			sections[3].append(cities[i])
		elif x[i] < 2 * midX and y[i] < 2 * midY:
			sections[4].append(cities[i])
		elif x[i] < 2 * midX:
			sections[5].append(cities[i])
		elif y[i] < midY:
			sections[6].append(cities[i])
		elif y[i] < 2 * midY:
			sections[7].append(cities[i])
		else:
			sections[8].append(cities[i])		
	for i in range(len(sections)):
		adjLists[i] = adjList(sections[i])
		msts[i] = prims(adjLists[i])



def calcTsp(cities, outFile):
	#Input: an array of x, y cartesian coordinates
	#Output: an approximate shortest path between input coordinates
	# if len(cities) > 5000:
	# 	mst = calcTspLarge(cities)
	# else:

	adj = adjList(cities)
	mst = prims(adj)
	cityOrder = preOrderWalk(mst)
	outputResults(cities, cityOrder, outFile)
	matlabGraph(cities, cityOrder)

#cmd line args parser setup
parser = argparse.ArgumentParser(description="Enter an input file path")
parser.add_argument("inputFile", type=str, help="Path to input file")
args = parser.parse_args()

#setup output file
outFileName = args.inputFile + ".tour"
out = open(outFileName, 'w')

#parse cities into a list of lists.
cities = readinstance(args.inputFile)
print(str(timeit.timeit(lambda:calcTsp(cities, out),number=1)))
if (out):
	out.close()
