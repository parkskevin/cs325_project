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

def outputResults(cities, cityOrder, outFile):
	dist = 0
	for i in range(1, len(cityOrder), 1):
		dist += distance(cities[i], cities[i - 1])
	outFile.write(str(dist) + "\n")
	for i in cityOrder:
		outFile.write(str(i) + "\n")

def calcTsp(cities, outFile):
	#Input: an array of x, y cartesian coordinates
	#Output: an approximate shortest path between input coordinates
	cityOrder = [0, 1, 2, 3, 4] #test
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
