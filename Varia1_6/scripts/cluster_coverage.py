import sys
'takes in name used in Varia script for current sample'
name = sys.argv[1]

'opens coverage file and stores content as an array'
filestore = []
store = []
n=0
filename = "./" + name + ".cover.txt"
file = open(filename,"r")
for line in file:
	line = line[0:(len(line) -1)]
	filestore.append([])
	store = line.split('\t')
	filestore[n] = store[0:4]
	n = n + 1
file.close()

'adds an entry to cov_store array for each base in the longest sequence'
cov_store = []
n = 0
while(n < int(filestore[0][3])):
	cov_store.append(1)
	n = n + 1

'for all entries that are not self hits, 1 is added to cov_store for the bases that blast has aligned between the sequences'
n = 0
while(n < len(filestore)):
	start = 0
	if(filestore[n][0] != filestore[n][1]):
		start = int(filestore[n][2]) - 1
		while(start < int(filestore[n][3])):
			cov_store[start] = int(cov_store[start]) + 1
			start = start + 1
	n = n + 1

'writes results to a new file'
n = 0
filename = name + ".plotcov.txt"

file = open(filename,"w")
while(n < len(cov_store)):
    writeline = filestore[0][0] + "\t" + str(n) + "\t" + str(cov_store[n]) + "\n"
    file.write(writeline)
    n = n + 1

file.close()
