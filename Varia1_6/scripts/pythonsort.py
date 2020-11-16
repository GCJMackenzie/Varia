import sys

'takes in name used in Varia script for current sample'
name = sys.argv[1]


n = -1
finalstore = []
store = []

'opens the clusters file and stores the groups as one array with the members of the group being an array within the array'
filename = "./" + name + ".clusters.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    n = n + 1
    store.append([])
    store[n] = line.split('\t')
    
file.close()


'stores the name and length of each entry in self.blast.length as an item in an array'
n = 0
filename = "./" + name + ".Self.blast.length"

file = open(filename, "r")
filestore = ""

for line in file:
    filestore = filestore + line

filestore = filestore.split('\n')
filestore = filestore[0:(len(filestore) -1)]
linestore = ""
while(n< len(filestore)):
      linestore = filestore[n].split('\t')
      filestore[n] = ["",""]
      filestore[n][0] = linestore[0]
      filestore[n][1] = int(linestore[12])
      n = n + 1
      
file.close()
n = 0

'matches names in the store array to those in the filestore to find the matching lengths'
while (n < len(store)):
    c = 0

    while (c < len(store[n])):
        l = 0
        match = False
        while (match == False):
            if( store[n][c] == filestore[l][0]):
                store[n][c] = filestore[l]
                match = True
            else:
                l = l + 1

                
        c = c + 1    

    'finds the maximum length in each group and stores the name and length of that maximum in finalstore array'

    c = 0
    max = store[n][c]
    while (c < len(store[n])):
        if(max[1] < store[n][c][1]):
            max = store[n][c]
        c = c + 1
    finalstore.append(max)
    n = n + 1

'creates the chromosome.txt file for the current sample using name in finalstore for chromosome and the length for the end of the chromosome'
filename = "./"+name+".chromosome.txt"
file = open(filename, 'w')
n = 0
'writeline = "chr\tstart\tend\n"'
'file.write(writeline)'
while(n< len(finalstore)):
    writeline = "chr\t-\t" + finalstore[n][0] + "\t" + "Cluster_" + str(n + 1) + "\t0\t" + str(finalstore[n][1]) + "\tlgrey\n"
    file.write(writeline)
    n = n + 1

file.close()

'opens the genes.fasta file and overwrites the lengths in finalstore array with the fasta file entry for the matching names stored in finalstore'
filename = "./"+name+".genes.fasta"
n = 0
check = False
while(n < len(finalstore)):
    finalstore[n][1] = ""
    file = open(filename, 'r')
    for line in file:
        if(line[0] == '>'):
            check = False
        if(line[1:(len(line) - 1)] == finalstore[n][0]):
            check = True
        if(check == True):
            finalstore[n][1] = finalstore[n][1] + line
    file.close()
    n = n + 1

'writes the finalstore fasta entries to forblast.fasta file'
filename = "./"+name+".forblast.fasta"
file = open(filename, 'w')
n = 0
while(n < len(finalstore)):
    writeline = finalstore[n][1]
    file.write(writeline)
    n = n + 1

