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
#        Usage: python fib.py -a <1-4> [-f <filepath>] 

def a1(arr):
    return arr

def a2(arr):
    return arr

def a3(arr):
    return arr

def a4(arr):
    return arr

import argparse
import rand #random file generator

RANDFILE = "rnums.txt"
MSSFILE = "MSS_Problems.txt"

parser = argparse.ArgumentParser(description="Find maximum sum sub-array")

parser.add_argument("-a", "--algo", type=int, help="The choice of algorithm(1-4)")
parser.add_argument("-f", "--file", help="Path to input file")
parser.add_argument("-r", "--rand", help="Randomly generated")
args = parser.parse_args()

if not (args.algo):
    parser.error("No algorithm specified")

elif (args.algo > 4 or args.algo < 1):
    parser.error("Choose an algorithm 1-4")
elif (not args.file):
	#no file, so random is an option
	if(args.rand):
		args.file = RANDFILE
	else:
		args.file = MSSFILS
print "Input file: " + args.file
print "Selected algorithm: " + str(args.algo)

#if args.rand is used, make the file first, then read it in
if(args.rand):
	#needs some sanitizing funcs here
	rand.make_rand(args.rand)
	f = open(args.file, 'r')
	input = f.read()
	f.close()
else:
	input = '[1,2,3]'
testArr = map(int, input.replace("[", "").replace("]", "").split(','))

if (args.algo == 1):
    print(a1(testArr))

elif (args.algo == 2):
    a2(testArr)

elif (args.algo == 3):
    a3(testArr)

elif (args.algo == 4):
    a4(testArr)


