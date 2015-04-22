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
#		 The argument -t turns off printing, and outputs Excel format of
#	     2 columns: array size and timing result. 
#
#        Usage: python fib.py -a <1-4> [-f <filepath> XOR -r <arrays>]  [-t]

import sys #for maxint
import timeit #for timings

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
	return arr[curMaxStart:curMaxEnd + 1]

def a2(arr):
	curMaxSubArray = -sys.maxint
	curMaxStart = -1
	curMaxEnd = -1
	for i in range(len(arr)):
		curSum = 0
		for j in range(i, len(arr)):
			curSum += arr[j]
			if (curSum > curMaxSubArray):
				curMaxSubArray = curSum
				curMaxStart = i
				curMaxEnd = j
	return arr[curMaxStart:curMaxEnd + 1]

def a3(arr):
	def recSubArr(arr, low, high):
		if high == low:
			return (low, high, arr[low])
		else: 
			mid = (low + high) / 2  
			(lLow, lHigh, lSum) = recSubArr(arr, low, mid)
			(rLow,rHigh,rSum) = recSubArr(arr, mid + 1, high)
			(cLow,cHigh,cSum) = crossSub(arr,low,mid,high)
		if lSum >= rSum and lSum >= cSum:
			return (lLow, lHigh, lSum)
		elif rSum >= lSum and rSum >= cSum:
			return (rLow, rHigh, rSum)
		else:
			return (cLow, cHigh, cSum)
	
	def crossSub(arr, low, mid, high):
		lSum = -sys.maxint
		rSum = -sys.maxint
		curSum = 0
		maxLeft = -sys.maxint
		maxRight = -sys.maxint
		for i in range(mid, low -1, -1):
				curSum = curSum + arr[i]
				if (curSum > lSum):
					lSum = curSum
					maxLeft = i
		curSum = 0
		for j in range(mid + 1, high + 1):
			curSum = curSum + arr[j]
			if curSum > rSum:
				rSum = curSum
				maxRight = j
		return (maxLeft, maxRight, lSum + rSum)
	result = recSubArr(arr, 0, len(arr) - 1)
	return arr[result[0] : result[1] + 1]

def a4(arr):
	temp_sum = 0
	max_sum = -sys.maxint
	temp_start = 0#holds the start index of intermediate sum
	max_start = 0#holds the start index of max sum
	max_end = 0 #holds the end index of max sum
	
	for x in xrange(0,len(arr)):
		temp_sum = temp_sum + arr[x]
		
		if temp_sum > max_sum:
			max_sum = temp_sum
			max_start = temp_start
			max_end = x
		if temp_sum < 0:
			temp_sum = 0
			temp_start = x+1

	return arr[max_start:max_end + 1]
	
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
parser.add_argument("-r", "--rand", type=int, help="Randomly generated")
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
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a2(j),number=1)))
			else:
				subArray = a2(j)
				totalSum = sum(subArray)
				printResults(j, subArray, totalSum)
				print("")

elif (args.algo == 3):
	for i in testArr:
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a3(j),number=1)))
			else:
				subArray = a3(j)
				totalSum = sum(subArray)
				printResults(j, subArray, totalSum)
				print("")

elif (args.algo == 4):
	for i in testArr:
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a4(j),number=1)))
			else:
				subArray = a4(j)
				totalSum = sum(subArray)
				printResults(j, subArray, totalSum)
				print("")


