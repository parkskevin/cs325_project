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

#constants
INPUTFILE = "Amount.txt"
OUTPUTFILE = "change.txt"
SLOWMAX = 31 #maximum amount we allow for slowchange

#Source: tsp-verifier.py from supplied project files
def distance(a,b):
    # a and b are integer pairs (each representing a point in a 2D, integer grid)
    # Euclidean distance rounded to the nearest integer:
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    #return int(math.sqrt(dx*dx + dy*dy)+0.5) # equivalent to the next line
    return int(round(math.sqrt(dx*dx + dy*dy)))
	
	
#cmd line args parser setup
parser = argparse.ArgumentParser(description="Find minimum coins")
parser.add_argument("-a", "--algo", type=int, help="The choice of algorithm(1-3)")
parser.add_argument("-f", "--file", help="Path to input file")
parser.add_argument("-t", "--timing", help="record timings", action="store_true")
parser.add_argument("-d", "--debug", help="turn debug messages on", action="store_true")
args = parser.parse_args()

#cmd line args logic
outputDebug = True #whether we're printing debug
out = False #file handle to change.txt
coinTest = False #whether this is a test of all algos
canDoSlow = True #whether we can perform slowchange algo

#handle cmd line args
if not (len(sys.argv) > 2):
	parser.error("Too few arguments")
elif not (args.algo):
	coinTest = True #do all the algorithms then
elif (args.algo and args.algo > 3 or args.algo < 1):
	parser.error("Choose an algorithm 1-3")
elif (not args.file):
	parser.error("Missing file argument")
if (not args.debug):
	outputDebug = False

#setup output file
outFileName = args.file.replace(".txt", "") + OUTPUTFILE
out = open(outFileName, 'w')
	
if(outputDebug):
	#debug
	print "Input file: " + args.file
	print "Selected algorithm: " + str(args.algo)

#open whichever file as input
f = open(args.file, 'r')

#create the master list to hold each array as another list (2D array)
#append each array as new list of ints for each line of text read from file
#append the value we're interested in realizing to another array, the
#same index matching the demonination array and value
testArr = []
valueArr = []
for i, line in enumerate(f):
	if(i % 2 is 0):
		testArr.append([])
		testArr[i / 2].append(map(int, line.replace("[", "").replace("]", "").replace("\n", "").split(',')))
	else:
		valueArr.append([])
		valueArr[i / 2].append(int(line.replace("\n", "")))
f.close()

#for each algorithm, find the min coin per denomination value, calculate the sum, then print
if (args.algo == 1 or coinTest == True):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changeslow ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (valueArr[k][0] > SLOWMAX):
				if(outputDebug):
					print "Output %d too large" % valueArr[k][0]
				if(file):
					out.write("Output %d too large\n" % valueArr[k][0])
				continue
			if (args.timing):
				print(str(valueArr[k][0])+", "+str(len(j))+", "+str(timeit.timeit(lambda:a1(j, valueArr[k][0]),number=1)))
			else:
				subArray = a1(j, valueArr[k][0])
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					out.write("")

if (args.algo == 2 or coinTest == True):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changegreedy ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (args.timing):
				print(str(valueArr[k][0])+", "+str(len(j))+", "+str(timeit.timeit(lambda:a2(j, valueArr[k][0]),number=1)))
			else:
				subArray = a2(j, valueArr[k][0])
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					out.write("")

if (args.algo == 3 or coinTest == True):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changedp ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (args.timing):
				print(str(valueArr[k][0])+", "+str(len(j))+", "+str(timeit.timeit(lambda:a3(j, valueArr[k][0]),number=1)))
			else:
				subArray = a3(j, valueArr[k][0])
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					out.write("")

if (out):
	out.close()
