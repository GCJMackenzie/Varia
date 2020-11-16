import sys
'takes in name used in Varia script for current sample'
name = sys.argv[1]
n = 0
store = []
colorstore = []

'link file is opened and stored in the store array'
filename = "./" + name + ".linked.txt"
file = open(filename,"r")
for line in file:
    line = line[0:(len(line) -1)]
    store.append([line])

file.close()

'rewrites the entries in store array, adding the to colorstore array and adding a color value of red/blue/green based on remainder of n divided by 3'
while(n < len(store)):
    colorstore.append([])
    if(n % 3 == 0):
        colorstore[n] = store[n][0] + "\tcolor=red_a3\n"
    if(n % 3 == 1):
        colorstore[n] = store[n][0] + "\tcolor=blue_a3\n"
    if(n % 3 == 2):
        colorstore[n] = store[n][0] + "\tcolor=green_a3\n"
    n = n + 1

'colorstore contents written to new link file'
n = 0
filename = name + ".link.txt"

file = open(filename,"w")
while(n < len(colorstore)):
    writeline = colorstore[n]
    file.write(writeline)
    n = n + 1

file.close()
