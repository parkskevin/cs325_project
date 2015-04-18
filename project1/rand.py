#Author: Daniel Bonnin, Kevin Parks, Alex Thomas
#email:  bonnind@onid.oregonstate.edu, parkske@onid.oregonstate.edu
#class:  CS325
#Assgn:  Project 1
#Descr:  This program creates a random output to file for testing purposes. 
#
#Input:  The program takes an integer as an argument. The program creates
#		 this number of values in the same format as MSS_Problems.txt
#
#Usage:  The argument -n followed by an integer will cause a random array
#        to be generated to file

import random
import sys

def make_rand(num):
	#max and min values to generate random values between
	MAXVAL = 100
	MINVAL = -100

	#name of rand file
	FILENAME = "rnums.txt"

	#some sanitizing
	num = int(num)
	if(not isinstance(num, int)):
		sys.exit("Value not supported")
	if(num > sys.maxint or num < 0):
		sys.exit("Value not supported.")
	
	#create the random values
	randoms = []
	for i in range(0, num):
		randoms.append(random.randint(MINVAL, MAXVAL))

	#make sure there's at least 1 positive value
	flag = 0
	for i in randoms:
		if(i > 0):
			flag = 1
	if(flag == 0):
		randoms[random.randint(0, num - 1)] *= -1

	#write to file
	num_string = ""
	for index, item in enumerate(randoms):
		if(index == 0):
			num_string += "[%d, " % item
		elif(index < num - 1):
			num_string += "%d, " % item
		else:
			num_string += "%d]\n" % item
	f = open(FILENAME, 'w')
	f.write(num_string)
	f.close()