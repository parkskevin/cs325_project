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

#helper
def makeChange(V, a):
	print a
	SolutionArray = [0 for i in range(len(V))]
	for i in range(len(V)):
		if a == V[i]:
			SolutionArray[i] += 1
			return SolutionArray

	bestSolution = []
	curMin = sys.maxint
	for i in range(1, a):
		subSolution = []
		sub1 = makeChange(V, i)
		sub2 = makeChange(V, a - i)
		for j in range(len(V)):
			subSolution.append(sub1[j] + sub2[j])
		if (curMin > sum(subSolution)):
			curMin = sum(subSolution)
			bestSolution = subSolution
	return bestSolution		





	return SolutionArray

#slowchange recursive
def a1(arr, value):
	return makeChange(arr, value)

#slowchange iterative version
# def a1(arr, value):
# 	SolutionArray = [0 for i in range(len(arr))]
# 	count = sys.maxint #track min coins overall
# 	for o_idx in range(len(arr) - 1, -1, -1): #count from end of array, backwards to start
# 		TempArray = [0 for i in range(len(arr))]
# 		m_value = value
# 		m_count = 0 #track internal count
# 		#for each coin index, find max # of coins, keep going until m_value <= 0
# 		for i_idx in range(o_idx, -1, -1):
# 			while(m_value >= arr[i_idx]):
# 				m_value -= arr[i_idx]
# 				m_count += 1
# 				TempArray[i_idx] += 1 #keep track of # of coins used
# 		#only care about exact change
# 		if(m_value == 0):
# 			#new count check
# 			if(m_count < count):
# 				count = m_count
# 				#assign this solution to our SolutionArray
# 				SolutionArray = list(TempArray)
# 	return SolutionArray

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
	#SolutionArray[len(arr)] = Table[value]
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
		valueArr[i / 2].append(int(line.replace("\n", "")))
f.close()

#for each algorithm, find the min coin per denomination value, calculate the sum, then print
if (args.algo == 1):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changeslow ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a1(j, valueArr[k][0]),number=1)))
			else:
				subArray = a1(j, valueArr[k][0])
				print subArray
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					out.write("")

if (args.algo == 2):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changegreedy ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a2(j, valueArr[k][0]),number=1)))
			else:
				subArray = a2(j, valueArr[k][0])
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					out.write("")

if (args.algo == 3):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** changedp ********************\n")
	for k, i in enumerate(testArr):
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a3(j, valueArr[k][0]),number=1)))
			else:
				subArray = a3(j, valueArr[k][0])
				minCoins = sum(subArray)
				printResults(subArray, minCoins, outputDebug, out)
				if not (outputDebug):
					out.write("")

if (out):
	out.close()
