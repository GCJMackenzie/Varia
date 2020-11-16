import sys
'takes in name used in Varia script for current sample'
name = sys.argv[1]
n = 0
store = []
linkstore = []
chromstore = []
bigstore = []
'opens the link file and stores contents in linkstore array'
filename = "./" + name + ".link.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    linkstore.append([])
    store = line.split('\t')
    linkstore[n] = store[0:3]
    n = n + 1

file.close()

'opens the chromosome file to store clusters ("chromosomes") in the chromstore array'
n = 0

filename = "./" + name + ".chromosome.txt"

file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    chromstore.append([])
    store = line.split('\t')
    chromstore[n].append(store[2])
    chromstore[n].append(store[5])
    n = n + 1

file.close()

'for each cluster:'
n = 0
while(n < len(chromstore)):
    bigstore = []
    c = 0

    'new array is created and an entry is added for every base in current cluster sequence'
    while(c <= int(chromstore[n][1])):
        bigstore.append(1)
        c = c + 1

    'for each linkstore entry which matches to current cluster, 1 is added to each base covered by the link entry and stored in the current bigstore'
    c = 0
    while(c < len(linkstore)):
        if(linkstore[c][0] == chromstore[n][0]):
            s = int(linkstore[c][1])
            e = int(linkstore[c][2])
            while(s <= e):
                bigstore[s] = bigstore[s] + 1
                s = s + 1
        c = c + 1

    c = 0
    'a file is generated containing the contents of current bigstore array meaning one file per cluster is generated'
    filename = "./depth." + chromstore[n][0] + ".plot"

    file = open(filename,"w")
    while(c < len(bigstore)):
        writeline = chromstore[n][0] + '\t' + str(c) + '\t' + str(bigstore[c]) + '\n'
        file.write(writeline)
        c = c + 1
    file.close()
    n = n + 1

'a list of cluster names is generated and added to file for use later in Varia script'
n = 0
filename = name + ".plotlist.txt"

file = open(filename,"w")
while(n < len(chromstore)):
    writeline = chromstore[n][0] + '\n'
    file.write(writeline)
    n = n + 1

file.close()
    
