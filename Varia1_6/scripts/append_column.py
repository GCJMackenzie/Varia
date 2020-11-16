import sys
from pathlib import Path

'script used in conjunction with Make_master.sh to add new columns to the master table'
'file 1 should be the file you want to add the column to, with first column being an ID'
'file 2 should be the new column with first column being an ID and second being the column to be added'
file1 = sys.argv[1]
file2 = name = sys.argv[2]
'filebuild is the arguement for the output file name'
filebuild = sys.argv[3]

store1 = []
store2 = []

n = 0

filename = Path(file1)
'file 1 opened and stored in store1'
file = open(filename, "r")
for line in file:
    line = line[0:(len(line) - 1)]
    line = line.split('\t')
    store1.append(line)
    drop = ""
    drop = store1[n][0].split('.')
    store1[n][0] = drop[0]
    n = n + 1
file.close()
n = 0

filename = Path(file2)
'file 2 opened and stored'
file = open(filename, "r")
for line in file:
    line = line[0:(len(line) - 1)]
    line = line.split('\t')
    store2.append(line)
    drop = ""
    drop = store2[n][0].split('.')
    store2[n][0] = drop[0]
    n = n + 1
file.close()

n = 0

'matches the column 1 of store1 to column 2 of store2 and adds the new columns'
while (n < len(store1)):
    c = 0
    while(c < len(store2)):
        if (store1[n][0] == store2[c][0]):
            store1[n].append(store2[c][1])
        c = c + 1
    n = n + 1

n = 0
filename = Path(filebuild)
'writes stored array to new file.'
file = open(filename, "w")
while(n < len(store1)):
	writeline = store1[n][0]
	c = 1
	while(c < len(store1[n])):
		writeline = writeline + '\t'
		writeline = writeline + store1[n][c]
		c = c + 1
	writeline = writeline + '\n'
	file.write(writeline)
	n = n + 1
file.close()
