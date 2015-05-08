#!/usr/bin/python

V = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
amount = 2000
increment = 1
f = open("Amount#.txt", 'w')

while amount <= 2200:
	f.write("%s\n" % V)
	f.write("%s\n" % amount)
	amount += increment

f.close()
