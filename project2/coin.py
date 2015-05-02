#!/usr/bin/python

#Author: Daniel Bonnin, Kevin Parks, Alex Thomas
#email:  bonnind@onid.oregonstate.edu
#class:  CS325
#Assgn:  Project 2
#Descr:  This program calculates the least amount of coins necessary
#	 to fulfill a given integer value currency. 
#
#Input:  //TODO
#
#Usage:  //TODO

import sys #for maxint
import timeit #for timings
import argparse #cmd line arg parsing
import rand #random file generator

#constants
INPUTFILE = "input.txt"
OUTPUTFILE = "Results.txt"

def a1(arr):
#TODO changeslow
def a2(arr):
#TODO greedy
def a3(arr):
#TODO dynamicp
	
def printResults(arr, subArr, maxSum, mssTest, file):
	if not(mssTest):
		if(file):
			file.write("Original Array: %s\n" % arr)
		else:
			print("Original Array: %s" % arr)
	if (maxSum > 0):
		if(file):
			file.write("Subarray: %s\n" % subArr)
			file.write("Max Sum: %d\n" % maxSum)
		else:
			print("Subarray: %s" % subArr)
			print("Max Sum: %d" % maxSum) 
	else: 
		if(file):
			file.write("Subarray: (empty)\n")
			file.write("Max Sum: 0   ****  Note at least one value in the" + \
				   " array must be positive\n")
		else:
			print "Subarray: (empty)"
			print "Max Sum: 0   ****  Note at least one value in the" + \
				   " array must be positive"
	
#cmd line args parser setup
parser = argparse.ArgumentParser(description="Find maximum sum sub-array. No args does MSS_Results.txt test")
parser.add_argument("-a", "--algo", type=int, help="The choice of algorithm(1-4)")
parser.add_argument("-f", "--file", help="Path to input file")
parser.add_argument("-r", "--rand", type=int, help="Randomly generated")
parser.add_argument("-t", "--timing", help="record timings", action="store_true")
args = parser.parse_args()

#cmd line args logic
mssTest = False #whether we're printing to the MSS_Results.txt
out = False #file handle to MSS_Results.txt

#if not cmd line args, do MSS_Results.txt action
if not (len(sys.argv) > 1):
	mssTest = True
	out = file(OUTPUTFILE, 'w')
elif not (args.algo):
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

if not (mssTest):
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
if (args.algo == 1 or mssTest):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** Algorithm 1 ********************\n")
	for i in testArr:
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a1(j),number=1)))
			else:
				subArray = a1(j)
				totalSum = sum(subArray)
				printResults(j, subArray, totalSum, mssTest, out)
				if not (mssTest):
					print("")

if (args.algo == 2 or mssTest):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** Algorithm 2 ********************\n")
	for i in testArr:
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a2(j),number=1)))
			else:
				subArray = a2(j)
				totalSum = sum(subArray)
				printResults(j, subArray, totalSum, mssTest, out)
				if not (mssTest):
					print("")

if (args.algo == 3 or mssTest):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** Algorithm 3 ********************\n")
	for i in testArr:
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a3(j),number=1)))
			else:
				subArray = a3(j)
				totalSum = sum(subArray)
				printResults(j, subArray, totalSum, mssTest, out)
				if not (mssTest):
					print("")

if (args.algo == 4 or mssTest):
	if not (args.timing or isinstance(out, bool)):
		out.write("******************** Algorithm 4 ********************\n")
	for i in testArr:
		for j in i:
			if (args.timing):
				print(str(len(j))+", "+str(timeit.timeit(lambda:a4(j),number=1)))
			else:
				subArray = a4(j)
				totalSum = sum(subArray)
				printResults(j, subArray, totalSum, mssTest, out)
				if not (mssTest):
					print("")

if (out):
	out.close()
