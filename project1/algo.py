#!/usr/bin/python

#Author: Daniel Bonnin, Kevin Parks, Alex Thomas
#email:  bonnind@onid.oregonstate.edu
#class:  CS325
#Assgn:  Project 1
#Descr:  This program calculates a maximum sum array using 1 of 4 algorithms. 
#
#Input:  The program takes a text file as an argument. The program reads
#        Each line in the input file as a separate input. If no input file 
#        is specified, the program will attempt to open MSS_Problems.txt
#
#Usage:  The argument -a followed by a number 1-4 indicates an algorithm
#        to use to calculate the maximum sum array. 
#
#        The argument -f followed by a file name indicates the input text
#        file to use. 
#
#		 The argument -r following by an integer > 0 indicated to use
#		 a randomly generated file containing 'value' arrays as input.
#
#        Usage: python fib.py -a <1-4> [-f <filepath> XOR -r <arrays>] 
import sys #for maxint
import timeit
def a1(arr):
	curMaxSubArray = -sys.maxint
	curMaxStart = -1
	curMaxEnd = -1
	for i in range(len(arr)):
	    for j in range(i, len(arr)):
	        curSum = sum(arr[i : j + 1])
	        if (curSum > curMaxSubArray):
	            curMaxSubArray = curSum
	            curMaxStart = i
	            curMaxEnd = j
	# print "array: " + str(arr)
	# print "selected indices i:" + str(curMaxStart) + "j: " + str(curMaxEnd)
	return arr[curMaxStart:curMaxEnd + 1]

def a2(arr):
	fakeSubArrLen = int(len(arr)/2)
	if (fakeSubArrLen == 0):
		fakeSubArrLen = 1
	returnArr = []
	for i in range(0, fakeSubArrLen):
		returnArr.append(arr[i]);
	return returnArr

def a3(arr):
	fakeSubArrLen = int(len(arr)/2)
	if (fakeSubArrLen == 0):
		fakeSubArrLen = 1
	returnArr = []
	for i in range(0, fakeSubArrLen):
		returnArr.append(arr[i]);
	return returnArr

def a4(arr):
	fakeSubArrLen = int(len(arr)/2)
	if (fakeSubArrLen == 0):
		fakeSubArrLen = 1
	returnArr = []
	for i in range(0, fakeSubArrLen):
		returnArr.append(arr[i]);
	return returnArr
	
def printResults(arr, subArr, maxSum):
	print("Original Array: %s" % arr)
	if (maxSum > 0):
		print("Subarray: %s" % subArr)
		print("Max Sum: %d" % maxSum) 
	else: 
		print "Subarray: (empty)"
		print "Max Sum: 0   ****  Note at least one value in the" + \
		       " array must be positive"
	
import argparse #cmd line arg parsing
import rand #random file generator
import time #calculate function times

#constants
RANDFILE = "rnums.txt"
MSSFILE = "MSS_Problems.txt"
OUTPUTFILE = "MSS_Results.txt"

#cmd line args parser setup
parser = argparse.ArgumentParser(description="Find maximum sum sub-array")
parser.add_argument("-a", "--algo", type=int, help="The choice of algorithm(1-4)")
parser.add_argument("-f", "--file", help="Path to input file")
parser.add_argument("-r", "--rand", help="Randomly generated")
parser.add_argument("-t", "--timing", help="record timings", action="store_true")
args = parser.parse_args()

#cmd line args logic
if not (args.algo):
	parser.error("No algorithm specified")
elif (args.algo > 4 or args.algo < 1):
	parser.error("Choose an algorithm 1-4")
if (args.file and args.rand):
	parser.error("Cannot do create random and open existing file. Choose one.")
elif (not args.file):
	#no file, so random is an option
	if(args.rand):
		args.file = RANDFILE
	else:
		args.file = MSSFILE

#debug
print "Input file: " + args.file
print "Selected algorithm: " + str(args.algo)

#if args.rand is used, make the file first
if(args.rand):
	#needs some sanitizing funcs here
	rand.make_rand(args.rand)

#open whichever file as input
f = open(args.file, 'r')

#create the master list to hold each array as another list (2D array)
#append each array as new list of ints for each line of text read from file
testArr = []
for i, line in enumerate(f):
	testArr.append([])
	testArr[i].append(map(int, line.replace("[", "").replace("]", "").replace("\n", "").split(',')))
f.close()

#for each algorithm, find the subarray, calculate the sum, then print
#for loop obviously not implemented yet
if (args.algo == 1):
	for i in testArr:
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a1(j),number=1)))
			else:
				subArray = a1(j)
				totalSum = sum(subArray)
				printResults(j, subArray, totalSum)
				print("")

elif (args.algo == 2):
	for i in testArr:
		for j in i:
			subArray = a1(j)
			totalSum = sum(subArray)
			printResults(j, subArray, totalSum)
			print("")

elif (args.algo == 3):
	for i in testArr:
		for j in i:
			subArray = a1(j)
			totalSum = sum(subArray)
			printResults(j, subArray, totalSum)
			print("")

elif (args.algo == 4):
	for i in testArr:
		for j in i:
			subArray = a1(j)
			totalSum = sum(subArray)
			printResults(j, subArray, totalSum)
			print("")


