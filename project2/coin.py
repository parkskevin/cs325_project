#!/usr/bin/python

#Author: Daniel Bonnin, Kevin Parks, Alex Thomas
#email:  bonnind@onid.oregonstate.edu
#class:  CS325
#Assgn:  Project 2
#Descr:  This program calculates the least amount of coins necessary
#	     to fulfill a given integer value currency. 
#
#Input:  //TODO
#
#Usage:  //TODO

import sys #for maxint
import timeit #for timings
import argparse #cmd line arg parsing

#constants
INPUTFILE = "Amount.txt"
OUTPUTFILE = "change.txt"

def a1(arr, value):
#TODO changeslow
	return arr
def a2(arr, value):
#TODO greedy
	return arr
def a3(arr, value):
#TODO dynamicp
	return arr

#rough rewrite, will probably need update
def printResults(arr, minCoins, outputDebug, file):
	if(file):
		file.write("Coin Array: %s\n" % arr)
	if(outputDebug):
		print("Coin Array: %s" % arr)
	if (minCoins > 0):
		if(file):
			file.write("Min Coins: %d\n" % minCoins)
		if(outputDebug):
			print("Min Coins: %d" % minCoins) 
	else: 
		if(file):
			file.write("Min Coins: 0   **** Value less than min coin");
		if(outputDebug):
			print "Min Coins: 0   **** Value less than min coin"
	
#TODO: reuse most of this, rename as necessary
#cmd line args parser setup
parser = argparse.ArgumentParser(description="Find minimum coins")
parser.add_argument("-a", "--algo", type=int, help="The choice of algorithm(1-3)")
parser.add_argument("-f", "--file", help="Path to input file")
parser.add_argument("-t", "--timing", help="record timings", action="store_true")
parser.add_argument("-d", "--debug", help="turn debug messages on")
args = parser.parse_args()

#cmd line args logic
outputDebug = True #whether we're printing debug
out = False #file handle to change.txt

#handle cmd line args
if not (len(sys.argv) > 2):
	parser.error("No input file and/or algorithm specified")
elif not (args.algo):
	parser.error("No algorithm specified")
elif (args.algo > 3 or args.algo < 1):
	parser.error("Choose an algorithm 1-3")
elif (not args.file):
	args.file = INPUTFILE
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
#same inde matching the demonination array and value
testArr = []
valueArr = []
for i, line in enumerate(f):
	if(i % 2 is 0):
		testArr.append([])
		testArr[i / 2].append(map(int, line.replace("[", "").replace("]", "").replace("\n", "").split(',')))
	else:
		valueArr.append([])
		line.replace("\n", "")
		valueArr[i / 2].append(line)
f.close()

#for each algorithm, find the min coin per denomination value, calculate the sum, then print
if (args.algo == 1):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changeslow ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a1(j, valueArr[k]),number=1)))
			else:
				subArray = a1(j, valueArr[k])
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					print("")

if (args.algo == 2):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changegreedy ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a2(j, valueArr[k]),number=1)))
			else:
				subArray = a2(j, valueArr[k])
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					print("")

if (args.algo == 3):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changedp ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a3(j, valueArr[k]),number=1)))
			else:
				subArray = a3(j, valueArr[k])
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					print("")

if (out):
	out.close()
