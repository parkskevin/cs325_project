#!/usr/bin/python

#Author: Daniel Bonnin, Kevin Parks, Alex Thomas
#email:  bonnind@onid.oregonstate.edu
#class:  CS325
#Assgn:  Project 2
#Descr:  This program calculates the least amount of coins necessary
#	     to fulfill a given integer value currency. 
#
#Input:  This program takes a text file as input. The program reads
#		 each pair of lines in the file as a separate input. If no
#		 input file is specified, an error will be generated. The
#		 program outputs its results in a file named [inputfile]change.txt.
#		 The [inputfile] prefix is set equal to the input filename provided.
#
#Usage:  Without arguments, the program returns an error on usage
#
#        The argument -a followed by a number 1-3 indicates an algorithm
#        to use to calculate the minimum coins. 
#
#        The argument -f followed by a file name indicates the input text
#        file to use. 
#
#		 The argument -t performs timing output to stdout 
#
#		 The argument -d prints output to stdout instead of to a file
#
#        Usage: python coin.py (-f <filepath>) [-a <1-3>] [-t] [-d]

import sys #for maxint
import timeit #for timings
import argparse #cmd line arg parsing

#constants
INPUTFILE = "Amount.txt"
OUTPUTFILE = "change.txt"
SLOWMAX = 31 #maximum amount we allow for slowchange

#slowchange helper
def a1(arr, value):
	SolutionArray = [0 for i in range(len(arr))]
	#apply the same principle as we use in changedp for TempArray
	TempArray = [0 for i in range(value + 1)]
	mysum = makeChange(arr, value, TempArray);

	coins = value
	while(coins):
		SolutionArray[TempArray[coins]] += 1
		coins = coins - arr[TempArray[coins]]
	return SolutionArray
	
#slowchange recursive
def makeChange(V, a, TempArray):
	#amount is 0, base case
	if(a <= 0):
		return 0
		
	#set count to max, helps checks for min
	count = sys.maxint
	
	#check every coin value
	for i in range(len(V)):
		if(V[i] <= a):
			tmpCount = makeChange(V, a-V[i], TempArray) + 1
			if (tmpCount < count):
				count = tmpCount
				#add the coin index to TempArray when this occurs
				TempArray[a] = i
	
	return count

#changegreedy
def a2(arr, value):
	arrlength = len(arr)
	SolutionArray = [0 for i in range(len(arr))]
	while value > 0:
		for i in range(arrlength, 0, -1):
			if(arr[i-1] <= value):
				SolutionArray[i-1] += 1
				value -= arr[i-1]
				break
	return SolutionArray

#changedp
def a3(arr, value):
	Table = [0 for i in range(value + 1)] #tracks subsolutions
	Array = [0 for i in range(value + 1)] #tracks coins used
	#if we do an object method, replace SolutionArray and pass in Obj
	SolutionArray = [0 for i in range(len(arr))]

	Table[0] = 0 #amount 0 requires 0 coins
	
	#In an array of length Amount+1, set each index to a maxint
	# value, then when index >= coin value, check if the
	# index - coin_value < current value. If so, set current
	# value to index-coin_value. Also add the CoinArray index
	# to another array to track coins used.
	for i in range(1, value+1):
		Table[i] = sys.maxint
		for j in range(len(arr)):
			if(i >= arr[j]):
				if(Table[i - arr[j]] + 1 < Table[i]):
					Table[i] = Table[i - arr[j]] + 1
					Array[i] = j
	coins = value
	while(coins):
		SolutionArray[Array[coins]] += 1
		coins = coins - arr[Array[coins]]
		
	return SolutionArray

#rough rewrite, will probably need update
def printResults(arr, minCoins, outputDebug, file):
	if(file):
		file.write("Coins: %s\n" % arr)
	if(outputDebug):
		print("Coins: %s" % arr)
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
