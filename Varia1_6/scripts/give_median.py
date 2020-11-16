import sys
'takes in name used in Varia script for current sample'
name = sys.argv[1]
n = 0
store = []
coveragestore = []
'opens the coverage file'
filename = name
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    store.append(line.split('\t'))
    n = n + 1

file.close()  
n = 0
start = 0
c = 99

'for each 100 bases in coverage file the median is found and is stored in correct format for Circos to use'
while(c < len(store)):
    med1 = int(store[n + 49][2])
    med2 = int(store[n + 50][2])
    med = (med1 + med2) / 2
    med = store[n][0] + '\t' + str(n) + '\t' + str(c) + '\t' + str(med)
    coveragestore.append(med)
    c = c + 100
    n = n + 100

'median is calculated for last set of base pairs that are less than 100 long'
c = (len(store) - 1)
if(n < len(store)):
    mid = c - n
    if(mid % 2 == 1):
        med1 = store[n + int(mid / 2)][2]
        med2 = store[n + int(mid / 2) + 1][2]
        med = int((int(med1) + int(med2)) / 2)
        med = store[n][0] + '\t' + str(n) + '\t' + str(c) + '\t' + str(med)
        coveragestore.append(med)

    else:
        med1 = int(((mid / 2)))
        med = store[n + med1][2]
        med = store[n][0] + '\t' + str(n) + '\t' + str(c) + '\t' + str(med)
        coveragestore.append(med)
 


n = 0
'entries stored in coveragestore array are written to plotme file'
filename = "plotme.txt"

file = open(filename,"w")
while(n < len(coveragestore)):
    writeline = coveragestore[n] + '\n'
    file.write(writeline)
    n = n + 1

file.close()
