#README FILE
#Authors: Daniel Bonnin, Kevin Parks, Alex Thomas
#Group: 11
#Class: CS235 Spring 2015
#Assgn: Project 2

Our project consists of the following components:
	1. coin.py - primary project executable, does CoinChange work
	2. README - this file
	3. Report_Project2_Group11.pdf - documentation required for project
	
To run the program:
	1. Ensure all components are located in the same directory
	2. Run 'coin.py -f filename' from the command line. 'filename' should be the path to a valid input file.
		2a. Note: we expect the input file to be sorted, and well formed as this example shows:
			[1, 2, 3, 4]
			15
			
			Note that the coin denominations are presented first, the amount in question second. The
			file is ended with a blank line return.
		2b. If python is not in your path, then run 'path/to/python coin.py -f filename'
		3b. ***ATTENTION***: if the Amount value > 31, algorithm 1 will not be run. This algorithm is
			too inefficient for values beyond 31.
	3. The program should output a file named '[filename]change.txt', where [filename] is the prefix of
	   the input file selected in #2 above. This file contains solutions for each algorithm the project
	   requires. It outputs in the following order:
		- slowchange solutions
		- changegreedy solutions
		- changedp solutions
