import sys

'takes in name used in Varia script for current sample'
name = sys.argv[1]

n = 0
store = []
coveragestore = []
labelstore = []
axisstore = []
max = 0

'opens the chromosome file and stores the "chromosomes" (clusters) as an array'
filename = "./" + name + ".chromosome.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    store.append([])
    store[n] = line.split('\t')
    store[n] = [store[n][2]]
    store[n].append(0)
    n = n + 1
file.close()

'opens the coverage file for current sample and stores contents as an array'
filename = "./" + name + ".Plot.median.coverage.plot"
c = 0
temp = ''
file = open(filename,"r")
for line in file:
    line = line.split('\t')
    coveragestore.append([line[0]])
    coveragestore[c].append(int(float(line[3][0:(len(line) -1)])))
    c = c + 1
file.close()

'finds the largest coverage value stored in the coverage array'
n = 0
c = 0
while(n < len(coveragestore)):
    if(coveragestore[n][1] > max):
        max = coveragestore[n][1]
    n = n + 1

'for each cluster, a line is generated as a y-axis for the coverage plot and added to the file'
n = 0
while(n < len(store)):
    store[n][1] = max
    n = n + 1
filename = "./"+name+".axis_line.txt"
file = open(filename, 'w')
n = 0
while(n < len(store)):
    writeline = store[n][0] + '\t0\t0\t0' + '\n'
    file.write(writeline)
    writeline = store[n][0] + '\t0\t0\t' + str(store[n][1]) + '\n'
    file.write(writeline)
    n = n + 1
file.close()

'for each cluster, a label is added to bottom of y-axis of the coverage plot with a value of 0'
filename = "./"+name+".axis_label_min.txt"
file = open(filename, 'w')
n = 0
while(n < len(store)):
    writeline = store[n][0] + '\t0\t100\t0\tr0=1.145r,r1=1.155r\n'
    file.write(writeline)

    n = n + 1
file.close()

'for each cluster, a label is made with the maximum value added to the top of the y-axis'
filename = "./"+name+".axis_label_max.txt"
file = open(filename, 'w')
n = 0
while(n < len(store)):
    writeline = store[n][0] + '\t0\t100\t' + str(max) + '\tr0=1.225r,r1=1.245r\n'
    file.write(writeline)
    n = n + 1
file.close()
    
