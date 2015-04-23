#Author: Daniel Bonnin, Kevin Parks, Alex Thomas
#email:  bonnind@onid.oregonstate.edu, parkske@onid.oregonstate.edu
#class:  CS325
#Assgn:  Project 1
#Descr:  This program creates a random output to file for testing purposes. 
#
#Input:  The program takes an integer as an argument. The program creates
#		 this number of arrays in the same format as MSS_Problems.txt
#
#Usage:  The argument -n followed by an integer will cause 'n' arrays
#        to be generated, each increasing in length from 1 to n-1

import random
import sys

#********************Daniel modified this for testing. Original is commented out below**********************

def make_rand(arrays):
	#max and min values to generate random values between
	MAXVAL = 100
	MINVAL = -100
	#max size of arrays to be generated
	ARRSIZE = arrays

	#name of rand file
	FILENAME = "rnums.txt"

	#some sanitizing
	arrays = int(arrays)
	if(not isinstance(arrays, int)):
		sys.exit("Value not supported")
	if(arrays > sys.maxint or arrays < 0):
		sys.exit("Value not supported.")
	
	#create the random values
	randoms = []
	for i in range(0, arrays):
		randoms.append([])
		for j in range(0, i):								
			randoms[i].append(random.randint(MINVAL, MAXVAL))

	#make sure there's at least 1 positive value
	# flag = 0
	# for index, i in enumerate(randoms):
	# 	for j in i:
	# 		if(j > 0):
	# 			flag = 1
	# 	if(flag == 0):
	# 		randoms[index][random.randint(0, ARRSIZE - 1)] *= -1

	#write to file
	num_string = ""
	for i in randoms:
		for index, item in enumerate(i):
			if(len(i) == 1):
				num_string += "[%d]\n" % item
				break
			if(index == 0):
				num_string += "[%d, " % item
			elif(index < len(i) - 1):
				num_string += "%d, " % item
			else:
				num_string += "%d]\n" % item
	f = open(FILENAME, 'w')
	f.write(num_string)
	f.close()

	# def make_rand(arrays):
	# #max and min values to generate random values between
	# MAXVAL = 100
	# MINVAL = -100
	# #size of each array to be generated
	# ARRSIZE = random.randint(0, 10)

	# #name of rand file
	# FILENAME = "rnums.txt"

	# #some sanitizing
	# arrays = int(arrays)
	# if(not isinstance(arrays, int)):
	# 	sys.exit("Value not supported")
	# if(arrays > sys.maxint or arrays < 0):
	# 	sys.exit("Value not supported.")
	
	# #create the random values
	# randoms = []
	# for i in range(0, arrays):
	# 	randoms.append([])
	# 	for j in range(0, ARRSIZE):								
	# 		randoms[i].append(random.randint(MINVAL, MAXVAL))

	# #make sure there's at least 1 positive value
	# flag = 0
	# for index, i in enumerate(randoms):
	# 	for j in i:
	# 		if(j > 0):
	# 			flag = 1
	# 	if(flag == 0):
	# 		randoms[index][random.randint(0, ARRSIZE - 1)] *= -1

	# #write to file
	# num_string = ""
	# for i in randoms:
	# 	for index, item in enumerate(i):
	# 		if(len(i) == 1):
	# 			num_string += "[%d]\n" % item
	# 			break
	# 		if(index == 0):
	# 			num_string += "[%d, " % item
	# 		elif(index < ARRSIZE - 1):
	# 			num_string += "%d, " % item
	# 		else:
	# 			num_string += "%d]\n" % item
	# f = open(FILENAME, 'w')
	# f.write(num_string)
	# f.close()