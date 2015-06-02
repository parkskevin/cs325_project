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

#Source: tsp-verifier.py from supplied project files
def distance(a,b):
	# a and b are integer pairs (each representing a point in a 2D, integer grid)
	# Euclidean distance rounded to the nearest integer:
	dx = a[0]-b[0]
	dy = a[1]-b[1]
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
	adj = []
	for i in range(n):
		adj.append([])
		for j in range(n):
			if i == j:
				adj[i].append(sys.maxint)
			else:
				adj[i].append(distance(cities[i], cities[j]))
	return adj

def prims(adj):
	#generate minimum spanning tree of coordinates in cities
	treeV = []
	treeE = []
	treeV.append(0) 
	while len(treeV) < len(adj):
		minEdge = sys.maxint
		minIndexOut = 0
		minIndexIn = 0
		#Find shortest outgoing edge from current tree
		for i in range(len(treeV)):
			for j in range(len(adj[treeV[i]])):
				curEdge = adj[treeV[i]][j]
				curIndex = j
				if (curIndex not in treeV and curEdge < minEdge and curEdge != 0):
					minEdge = curEdge
					minIndexIn = curIndex
					minIndexOut = i
		treeV.append(minIndexIn)
		treeE.append((minIndexOut, minIndexIn))
	return (treeV, treeE)

def preOrderWalk(mst):
	#build new adj list from tree data
	adj = []
	for i in range(len(mst[0])):
		adj.append([])
		for j in range(len(mst[1])):
			inV, outV = mst[1][j]
			if (inV == i):
				adj[i].append(outV)
	#get the walk order
	order = []
	findAdj(adj, 0, order)
	#append the route back to the route to complete tour
	order.append(0)
	return order

#base case: if the node is a leaf, add it, return
#recursive case: recursively add each child (similar to left-child, then right-child, etc)	
def findAdj(adj, start, order):
	if (len(adj[start]) == 0):
		order.append(start)
		return
	order.append(start)
	for i in range(len(adj[start])):
		findAdj(adj, adj[start][i], order)
	return order
	
def outputResults(cities, cityOrder, outFile):
	dist = 0
	for i in range(1, len(cityOrder), 1):
		dist += distance(cities[cityOrder[i]], cities[cityOrder[i - 1]])
	outFile.write(str(dist) + "\n")

	for i in cityOrder:
		outFile.write(str(i) + "\n")

def matlabGraph(cities, mst):
	graphFile = open("matlabGraph.txt", 'w')
	graphFile.write("x=[")
	for i in range(len(cities)):
		graphFile.write(str(cities[mst[0][i]][0]) + " ")
	graphFile.write("];\n")
	graphFile.write("y=[")
	for i in range(len(cities)):
		graphFile.write(str(cities[mst[0][i]][1]) + " ")
	graphFile.write("];\n")
	graphFile.write("hold on;\n")
	graphFile.write("scatter(x, y)\n")
	x = []
	y = []
	for i in range(len(mst[1])):
		x.append([cities[mst[1][i][0]][0],cities[mst[1][i][1]][0]])
		y.append([cities[mst[1][i][0]][1],cities[mst[1][i][1]][1]])

	for i in range(len(mst[1])):
		graphFile.write("plot([" + str(x[i][0]) + " " + str(x[i][1]) + \
			"],[" + str(y[i][0]) + " " + str(y[i][1]) + "]);\n")

	graphFile.close()

def calcTsp(cities, outFile):
	#Input: an array of x, y cartesian coordinates
	#Output: an approximate shortest path between input coordinates
	adj = adjList(cities)
	mst = prims(adj)
	matlabGraph(cities, mst)
	cityOrder = preOrderWalk(mst)
	outputResults(cities, cityOrder, outFile)

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
