import sys

'takes in name used in Varia script for current sample'
name = sys.argv[1]

n = 0
store = []
untwinstore = []

'opens the links file and stores values as array'
filename = "./" + name + ".link.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    store.append([])
    store[n] = line.split('\t')
    n = n + 1
file.close()
n = 0

'adds entries in store to the untwinstore'
'checks that each new entry is not a mirror of any entry already in untwinstore which are generated during a self blast search'
while(n < len(store)):
    c = 0
    check = True
    while(c < len(untwinstore)):
        if(store[n][0] == untwinstore[c][3] and store[n][1] == untwinstore[c][4] and store[n][2] == untwinstore[c][5] and store[n][3] == untwinstore[c][0] and store[n][4] == untwinstore[c][1] and store[n][5] == untwinstore[c][2]):
            check = False
        c = c + 1
    if( check == True):
        untwinstore.append(store[n])
    n = n + 1

'untwinstore array written to new link file'
filename = "./"+name+".untwin_link.txt"
file = open(filename, 'w')
n = 0
while(n < len(untwinstore)):
    writeline = untwinstore[n][0] + '\t' + untwinstore[n][1] + '\t' + untwinstore[n][2] + '\t' + untwinstore[n][3] + '\t' + untwinstore[n][4] + '\t' + untwinstore[n][5] + '\t' + untwinstore[n][6] + '\n'
    file.write(writeline)
    n = n + 1
file.close()
