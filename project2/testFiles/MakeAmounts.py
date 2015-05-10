#!/usr/bin/python

V = [1, 5, 10, 25, 50]
amount = 1
increment = 2
f = open("Amount4_Small.txt", 'w')

while amount <= 31:
	f.write("%s\n" % V)
	f.write("%s\n" % amount)
	amount += increment

f.close()
