import sys
'takes in name used in Varia script for current sample'
name = sys.argv[1]
n = 0
clustore = []
clustore2 = []
blaststore = []
liststore = []
'opens the list of cluster names file and stores names as an array'
filename = "./" + name + ".listclust.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    liststore.append(line)
file.close()

n = 0
'opens cluster summary and stores entries in clustore based on their matching cluster names'
filename = "./" + name + ".cluster_summary.txt"
file = open(filename,"r")
n = 0
for line in file:
    line = line[0:(len(line) -1)]
    if(line[0] != 'C'):
        line = line.split('\t')
        if(int(line[0]) > n):
            clustore.append([])
            n = n + 1
            clustore[(int(line[0]) - 1)].append(line)
        else:
            clustore[(int(line[0]) - 1)].append(line)
file.close()

n = 0

'largest sequence in clusters found and added to clustore2, removing their cluster ID entry and adding the length of their respective clusters'
while(n < len(clustore)):
    c = 0
    while(c < len(clustore[n])):
        t = 0
        while(t < len(liststore)):
            if(clustore[n][c][1] == liststore[t]):
                transfer = clustore[n][c][1:]
                transfer.append(len(clustore[n]))
                clustore2.append(transfer)
            t = t + 1
        c = c + 1
        
    n = n + 1

n = 0
'calculates how many sequences in cluster are 80% the length of the largest sequence using blast file and adds count to end of clustore2'
while(n < len(clustore2)):
    length = float(clustore2[n][1])
    length = (length * 0.8)
    counter = 0
    filename = "./" + clustore2[n][0] + ".80.blast"
    file = open(filename,"r")
    for line in file:
        line = line[0:(len(line) -1)]
        line = line.split('\t')
        if(int(line[3]) > length and float(line[2]) > 99 and line[0] != line[1]):
            counter = counter + 1
    clustore2[n].append(str(counter))
    n = n + 1

n = 0
'goes through each cluster, adds all unique country distributions in that cluster to the countrystore taht are not reference of n/a, then length of countrystore is added to respective clustore2 entry'
while(n < len(clustore2)):
    countrystore = []
    c = 0
    while(c < len(clustore[n])):
        t = 0
        check = True
        while(t < len(countrystore)):
            if(countrystore[t] == clustore[n][c][3]):
                check = False
            t = t + 1
        if(check == True):
            if(clustore[n][c][3] != "n/a" and clustore[n][c][3] != "Reference"):
                countrystore.append(clustore[n][c][3])
        c = c + 1
    clustore2[n][2] = str(len(countrystore))
    n = n + 1
                
          
n = 0
'writes contents of clustore2 to final_summary file in the correct format'
filename = "./" + name + ".final_summary.txt"
file = open(filename,"w")
writeline = "Cluster_name\tCluster_size\tLongest_seq\tlength\t80%_matches\tCoutry_distrib\tSubdomains\n"
file.write(writeline)
while(n < len(clustore2)):
    writeline = "Cluster " + str(n + 1) + '\t' + str(clustore2[n][4]) + '\t' + clustore2[n][0] + '\t' + clustore2[n][1] + '\t' + clustore2[n][5] + '\t' + clustore2[n][2] + '\t' + clustore2[n][3] + '\n'
    file.write(writeline)
    n = n + 1

file.close()
    
