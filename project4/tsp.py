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
import operator #for prim sorting
import signal #for stopping


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
	n = len(cities)
	adj = []
	for i in range(n):
		adj.append([])
		for j in range(n):
			if i == j:
				adj[i].append((j, sys.maxint))
			else:
				adj[i].append((j, distance(cities[i], cities[j])))
	#greedy sorting, move shortest distances in general to front
	for i in range(len(adj)):
		adj[i].sort(key = operator.itemgetter(1))
	return adj	
		
def prims(adj):
	#generate minimum spanning tree of coordinates in cities
	treeV = []
	treeE = []
	treeV.append(0)
	uniqueV = set()
	uniqueV.add(0)
	while len(treeV) < len(adj):
		minEdge = sys.maxint
		minIndexOut = 0 #in treeV
		minIndexIn = 0  #to add to treeV
		#Find shortest outgoing edge from current tree
		#Iterate through treeV
		for i in range(len(treeV)):
			#grab the first matching vertex that meets the criteria, then break, we're done because they are sorted
			for index, value in adj[treeV[i]]:
				if (index not in uniqueV):
					adj[treeV[i]] = [x for x in adj[treeV[i]] if  adj[treeV[i]][0] == index]
					minEdge = value
					minIndexIn = index
					minIndexOut = treeV[i]
					break
		treeV.append(minIndexIn)
		uniqueV.add(minIndexIn)
		treeE.append((minIndexOut, minIndexIn))
	return (treeV, treeE)
	
def outputResults(cities, cityOrder, outFile):
	dist = 0
	for i in range(1, len(cityOrder), 1):
		dist += distance(cities[cityOrder[i]], cities[cityOrder[i - 1]])
	#need route to root added since can't be in cityOrder list for verifier
	dist += distance(cities[cityOrder[i]], cities[cityOrder[0]])
	outFile.write(str(dist) + "\n")

	for i in cityOrder:
		outFile.write(str(i) + "\n")

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
def triangleFunc(cities, order):
	for i in range(len(order) - 3):
		#if distance i->i+2->i+1->i+3 < i->i+1->i+2->i+3,
		#swap i+1, i+2 
		if distance(cities[order[i]], cities[order[i + 2]]) + \
		   distance(cities[order[i + 2]], cities[order[i + 1]]) + \
		   distance(cities[order[i + 1]], cities[order[i + 3]]) < \
		   distance(cities[order[i]], cities[order[i + 1]]) + \
		   distance(cities[order[i + 1]], cities[order[i + 2]]) + \
		   distance(cities[order[i + 2]], cities[order[i + 3]]):
		   swap = order[i + 1]
		   order[i + 1] = order[i + 2]
		   order[i + 2] = swap
	return order

def totalDist(cities, inOrder):
	pathLength = 0
	for i in range(1, len(inOrder), 1):
		pathLength += distance(cities[inOrder[i]], cities[inOrder[i - 1]])
	pathLength += distance(cities[inOrder[0]], cities[inOrder[len(inOrder)-1]])
	return pathLength

def findLastStop(cities, inOrder):
	minDist = totalDist(cities, inOrder)
	minOrder = inOrder
	for i in range(1, len(inOrder) - 2, 1):
		curOrder = [x for x in inOrder]
		swap = curOrder[i]
		curOrder[i] = curOrder[len(curOrder) - 1]
		curOrder[len(curOrder) - 1] = swap
		curDist = totalDist(cities, curOrder)
		if curDist < minDist:
			minDist = curDist
			minOrder = [x for x in curOrder]
	return minOrder

#does essentially the same as outputResults, but used as global handler for SIGTERM
#not sure what happens if we invoke SIGTERM before these globals are allocated...
def handler(signum, frame):
	dist = 0
	for i in range(1, len(lastGoodOrder), 1):
		dist += distance(lastCities[lastGoodOrder[i]], cities[lastGoodOrder[i - 1]])
	#need route to root added since can't be in cityOrder list for verifier
	dist += distance(lastCities[lastGoodOrder[i]], lastCities[lastGoodOrder[0]])
	lastFileOut.write(str(dist) + "\n")

	for i in lastGoodOrder:
		lastFileOut.write(str(i) + "\n")
	sys.exit()
	
def calcTsp(cities, outFile):
	#Input: an array of x, y cartesian coordinates
	#Output: an approximate shortest path between input coordinates
	adj = adjList(cities)
	mst = prims(adj)
	
	#prepare for the optimization loop by setting locals to compare against,
	#each time we improve, overwrite global so it may be used
	#in signal handler of SIGTERM
	inOrder = mst[0]
	minDist = totalDist(cities, inOrder)
	stopFlag = 0
	#print str(minDist)
	global lastGoodOrder
	global lastCities
	global lastFileOut
	lastGoodOrder = inOrder
	lastCities = cities
	lastFileOut = outFile
	#configure signal handler
	signal.signal(signal.SIGTERM, handler)
	
	#remove curly q's, optimizing routine
	while (1):
		inOrder = triangleFunc(cities, inOrder)
		inOrder = findLastStop(cities, inOrder)
		newDist = totalDist(cities, inOrder)
		if(newDist < minDist):
			minDist = newDist
			lastGoodOrder = inOrder
			#print minDist
		else:
			break
			#print "stopped at: ", minDist
	#matlabGraph(cities, inOrder)
	outputResults(cities, lastGoodOrder, outFile)

#cmd line args parser setup
parser = argparse.ArgumentParser(description="Enter an input file path")
parser.add_argument("inputFile", type=str, help="Path to input file")
args = parser.parse_args()

#setup output file
outFileName = args.inputFile + ".tour"
out = open(outFileName, 'w')

#parse cities into a list of lists.
cities = readinstance(args.inputFile)

#print(str(timeit.timeit(lambda:calcTsp(cities, out),number=1)))
calcTsp(cities, out)

if (out):
	out.close()
