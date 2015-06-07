#README FILE
#Authors: Daniel Bonnin, Kevin Parks, Alex Thomas
#Group: 11
#Class: CS235 Spring 2015
#Assgn: Project 4

Our project consists of the following components:
	1. tsp.py - primary project executable
	2. README - this file
	3. Report_Project4_Group11.pdf - documentation required for project
	4. *.tour files - files generated from our code for verification of our minimum tour lengths computed
	
To run the program:
	1. Ensure all components are located in the same directory
	2. Run 'tsp.py filename' from the command line. 'filename' should be the path to a valid input file.
		2b. If python is not in your path, then run 'path/to/python tsp.py filename'
	3. The program should output a file named '[filename].tours', where [filename] is the entire name of
	   the input file selected in #2 above. This file contains a solution tour for the input file
	   and can be verified via tsp-verifier.
