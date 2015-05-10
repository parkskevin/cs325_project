import random
out = open('a2Problem8.txt', 'w')
testArr = []
curV = 1
for i in range(10, 110, 10):
    for j in range(i):
        testArr.append(curV)
        inc = random.randint(1, 5)
        curV += inc
    testArr.sort()
    for k in range(5):
        out.write(str(testArr) + "\n")
        out.write(str(30) + "\n")
    testArr = []
    curV = 1