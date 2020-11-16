import sys

'takes in name used in Varia script for current sample'
name = sys.argv[1]
'takes in path to the Varia directory used in Varia script'
path = sys.argv[2]

n = 0
store = []
labelstore = []
tempstore = ""
'opens the chromosome file and stores the clusters ("chromosomes") as store array'
filename = "./" + name + ".chromosome.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    store.append([])
    store[n] = line.split('\t')
    store[n] = store[n][2]
    n = n + 1


file.close()


'opens the domain annotation file and finds entries that have matching names to the names in chromosome array and puts them in labelstore array'
filename = path + "/domains/vardb_domains.txt"
n = 0
c = 0
while(n < len(store)):
    file = open(filename,"r")
    for line in file:
        line = line.split('\t')
        if(store[n] == line[0]):
            labelstore.append([])
            labelstore[c] = line
            labelstore[c][3] = labelstore[c][3][:(len(labelstore[c][3]) - 1)]
            c = c + 1
    file.close()
    n = n + 1

'opens the domain color map adding a color entry to labelstore where the domain names match'
filename = path + "/domains/domain_color_map.txt"
n = 0
while(n < len(labelstore)):
    file = open(filename,"r")
    for line in file:
        line = line.split('\t')

        if(line[0] in labelstore[n][3][:(len(labelstore[n][3]) - 1)] or line[0] == labelstore[n][3][:(len(labelstore[n][3]) - 1)] or labelstore[n][3][:(len(labelstore[n][3]) - 1)] in line[0]):
            labelstore[n].append(line[1])
    file.close()
    n = n + 1


n = 0
'writes chromosome name, start and end positions of annotations, a "value" and colour to the domains file for circos plot'
'domains file allows us to add highlighted regions to better separate the domains visually, "value" is included to generate a bar graph.'


filename = "./"+name+".domains.txt"
file = open(filename, 'w')

while(n < len(labelstore)):
    writeline = labelstore[n][0] + '\t' + labelstore[n][1] + '\t' + labelstore[n][2] + '\t' + "1" + '\t' + labelstore[n][4] + '\n'
    file.write(writeline)
    n = n + 1
file.close()

'adds contents of subdomains file to array where the identifier matches the cluster ID'
subdomainstore = []
filename = path + "/domains/vardb_domains.txt"
n = 0
c = 0
while(n < len(store)):
    file = open(filename,"r")
    for line in file:
        line = line.split('\t')
        if(store[n] == line[0]):
            subdomainstore.append([])
            subdomainstore[c] = line
            c = c + 1
    file.close()
    n = n + 1

'writes contents of subdomainstore to file containing the labels for the circos plot'
filename = "./"+name+".domain_label.txt"
file = open(filename, 'w')
n = 0
while(n < len(labelstore)):
    writeline = subdomainstore[n][0] + '\t' + subdomainstore[n][1] + '\t' + subdomainstore[n][2] + '\t' + subdomainstore[n][3] + '\n'
    file.write(writeline)
    n = n + 1
file.close()
