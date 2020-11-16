import sys
'takes in name used in Varia script for current sample and the path to the varia directory'
name = sys.argv[1]
Dir = sys.argv[2]
n = 0
'distribstore contains list of countries and their matching letters used in sample labelling'
Distribstore = [['PA',"Gambia"],['PC',"Kenya"],['PD','Thailand'],['PF','Ghana'],['PH','Cambodia'],['PM','Mali'],['PS','Senegal'],['PT','Malawi'],['PU','Guinea'],['PV','Vietnam'],['QE','Laos'],['QG','Congo']]
clustore = []
seqstore = ['placeholder']
domainstore = []
writestore1 = []
'opens the cluster file and stores each cluster as an array entry and each sequence in that cluster as an array within the array of clusters'
filename = "./" + name + ".clusters.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]    
    line = line.split('\t')
    clustore.append([])
    c = 0
    while(c < len(line)):
        clustore[n].append([line[c]])
        c = c + 1
    n = n + 1
file.close()


n = 0
'adds the contents of subdomains file to array'    
filename = Dir + "/domains/vardb_domains.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]    
    line = line.split('\t')
    domainstore.append([line])
    n = n + 1
file.close()

'stores sequences found in genes.fasta as an array'
n = 0
filename = "./" + name + ".genes.fasta"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    if(line[0] == '>'):
        n = n + 1
        seqstore.append([line[1:len(line)]])
        seqstore[n].append("")
    else:
        temp = str(seqstore[n][1]) + line
        seqstore[n][1] = temp
file.close()


n = 0
'for each entry in each cluster matching sequence and length of that sequence is added to clustore' 
while(n < len(clustore)):
    c = 0
    while(c < len(clustore[n])):
        t = 0
        while(t < len(seqstore)):
            if(seqstore[t][0] == clustore[n][c][0] and len(clustore[n][c]) == 1):
                clustore[n][c].append(seqstore[t][1])
                clustore[n][c].append(len(seqstore[t][1]))
            t = t + 1
        c = c + 1
    n = n + 1

n = 0

'adds the country distribution to the clustore, n/a if sample id does not contain -C or Reference if no match is found'
while(n < len(clustore)):
    c = 0
    while(c < len(clustore[n])):
        clustore[n][c].append('n/a')
        if('-C' in clustore[n][c][0]):
            t = 0
            while(t < len(Distribstore)):
                if(Distribstore[t][0] == clustore[n][c][0][0:2]):
                    clustore[n][c][3] = Distribstore[t][1]
                t = t + 1
        else:
            clustore[n][c][3] = "Reference"
        
        c = c + 1
    n = n + 1


n = 0
'adds subdomain structure to each cluster entry or n/a if no match found'
while(n < len(clustore)):
    c = 0
    while(c < len(clustore[n])):
        t = 0
        subdomain = ""
        while(t < len(domainstore)):
            if(domainstore[t][0][0] == clustore[n][c][0]):
                subdomain = subdomain + " " + domainstore[t][0][3]
            t = t + 1
        clustore[n][c].append(subdomain)
        if(clustore[n][c][4] == ""):
            clustore[n][c][4] = "n/a"
        c = c + 1
    n = n + 1
n = 0
'adds header to array of output to cluster summary'
line = "Cluster_ID\tSeq_ID\tSeq_length\tCountry_Distribution\tSubdomains\n"
writestore1.append(line)

'adds each cluster and their samples to the cluster summary output array'
while(n< len(clustore)):

    c = 0
    while(c < len(clustore[n])):
        line = str(n + 1) + '\t' + clustore[n][c][0] + '\t' + str(clustore[n][c][2]) + '\t' + clustore[n][c][3] + '\t' + clustore[n][c][4] + '\n'
        writestore1.append(line)
        c = c + 1
    n = n + 1

n = 0
'writes contents of writestore to cluster summary file'
filename = name + ".cluster_summary.txt"

file = open(filename,"w")
while(n < len(writestore1)):
    file.write(writestore1[n])
    n = n + 1

file.close()


writestore2 = []
n = 0
'for each cluster:'
while(n < len(clustore)):
    Max = 0
    c = 1
    'largest sample in cluster is found'
    while(c < len(clustore[n])):
        if(int(clustore[n][c][2]) > int(clustore[n][Max][2])):
            Max = c
        c = c + 1
    'largest sample is added to new file to be used as a query for blast'
    writestore2.append(clustore[n][Max][0])
    filename = clustore[n][Max][0] + ".query_seq.txt"
    file = open(filename,"w")
    writeline = '>' + clustore[n][Max][0] + '\n'
    file.write(writeline)
    writeline = clustore[n][Max][1] + '\n'
    file.write(writeline)
    file.close()

    'all sequences in cluster are added to new file to act as a subject of a blast search'
    filename = clustore[n][Max][0] + ".db_seq.txt"
    file = open(filename,"w")    
    c = 0
    while(c < len(clustore[n])):
        writeline = '>' + clustore[n][c][0] + '\n'
        file.write(writeline)
        writeline = clustore[n][c][1] + '\n'
        file.write(writeline)
        c = c + 1

    file.close()    
    n = n + 1

'list of the names of the largest cluster are written to file for later use by Varia'
n = 0
filename = "./" + name + ".listclust.txt"
file = open(filename,"w")   
while(n < len(writestore2)):    
    writeline = writestore2[n] + '\n'
    file.write(writeline)
    n = n + 1

file.close()
    

    
    

