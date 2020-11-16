#Imports sys module required for input arguments.
import sys

#Argument containing filename to be used.
filename = sys.argv[1]


#Each entry of domainstore is a domain name that will be plotted on the x-axis of the plot.
domainstore = [[ 'NTS', []], [ 'DBLa', []], [ 'CIDRa', []], [ 'DBLd', []], [ 'CIDRd', []], [ 'DBLb', []], [ 'CIDRb', []], [ 'DBLg', []], [ 'CIDRg', []], [ 'DBLe', []], [ 'DBLz', []], [ 'DBLpam', []], [ 'CIDRpam', []], [ 'ATS', []]]

#Set of colours to add to each row of bars on the plot row 1 beind first colour and so on.
colours = ['red','blue','green','yellow','orange','purple']

#Stores each line of the input file.
linestore = []

plotpoint = []
plotlab = []

#Opens input file and extracts the subdomain structure from each line and adds it to linestore.
n = 0
file = open(filename,"r")
for line in file:
	line = line[0:(len(line) -1)]
	line = line.split('\t')
	length = (len(line) - 1)
	domains = line[length]
	domains = domains.split(' ')
	domains = domains[1:(len(domains))]
	#Only adds lines with a subdomain prediction, "n/a" entries are not counted.
	if len(domains) != 0:
		linestore.append(domains)
	n = n + 1
file.close()

#Fullline contains all subdomains stored in linestore as a 1D array.
fullline = []
n = 0

#Adds all subdomains to fullline.
while n < len(linestore):
	c = 0
	while c < len(linestore[n]):
		fullline.append(linestore[n][c])
		c = c + 1
	n = n + 1

n = 0
count = 0

#For each domain in domainstore the fullline array is searched.
while n < len(fullline):
	c = 0
	while c < len(domainstore):
		#If the name of the domainstore entry is in the name of the subdomain,
		#e.g. DBLe is in DBLe10 and DBLe5 but not DBLa 5, then it is considered a match.
		if domainstore[c][0] in fullline[n]:
			t = 0
			#If the subdomain matches a subdomain name already entered then 1 is
			#added to that subdomains counter.
			match = False
			while t < len(domainstore[c][1]):
				if fullline[n] == domainstore[c][1][t][0]:
					domainstore[c][1][t][1] = domainstore[c][1][t][1] + 1
					match = True
				t = t + 1
			#If no matche is found, a new subdomain count is started and 1 is added.
			if match == False:				 
				domainstore[c][1].append([fullline[n], 1])
			count = count + 1
		c = c + 1
	n = n + 1

#Finds the largest number of subdomains assigned to 1 domain and sets len_max to that number.
n = 0
len_max = 0
while n < len(domainstore):
	if len_max < len(domainstore[n][1]):
		len_max = len(domainstore[n][1])
	n = n + 1

#Bar plots are generated using the matplotlib module, which requires that each row of bars in
#a stacked bar plot b stored as an array. len_max sets how many rows are needed by the plot and
#therefore how many arrays need to be made.

#Stores the counts and names of subdomains.
domstore = []
#Stores just the counts of subdomains.
countstore = []
#Stores the counts of subdomains as a percentage of total domain counts.
percentstore = []
#Stores just the names of subdomains.
labelstore=  []

#Adds a number of empty arrays to percent, count and labelstore equal to the value of len_max.
n = 0
while n < len_max:
	countstore.append([])
	labelstore.append([])
	percentstore.append([])
	n = n + 1


#For each array in labelstore and countstore:
n = 0
while n < len(countstore):
	c = 0
	#The subdomain names and counts of the corresponding domainstore are copied into the
	#countstore and labelstore arrays respectively.
	while c < len(domainstore) :
		current_len = len(domainstore[c][1])
		if n < current_len:
			labelstore[n].append(domainstore[c][1][n][0])
			countstore[n].append(domainstore[c][1][n][1])
		else:
		#If the domainstore is not as long as the max_len value, blank placeholder 			#entries are added to countstore and labelstore. This is done so each array in 			#in the stores is the same length, which ensures all counts and labels are in 			#the correct positions on the plot.
			labelstore[n].append('')
			countstore[n].append(0)
		c = c + 1
	n = n + 1
 
 
#Maxstore contains an array entry for each domain to be plotted.
maxstore = []
n = 0
while n < len(countstore[0]):
	maxstore.append(0)
	n = n + 1

#The counts of each subdomain are totalled up based on their domain grouping.
#This gives us the total number of counts held for each domain to be plotted.
n = 0
while n < len(maxstore):
	c = 0
	while c < len(countstore):
		maxstore[n] = maxstore[n] + countstore[c][n]
		c = c + 1
	n = n + 1

#Calculates the percentage form of the countstore counts, using maxstore entries as the total #domain count.
n = 0
while n < len(maxstore):
	c = 0
	while c < len(countstore):
		if maxstore[n] != 0:
			percentstore[c].append(round(((countstore[c][n] / maxstore[n]) * 100),1))
		else:
			#If maxstore entry for domain = 0 adds an entry that = 0 to percentstore.
			#This prevents divisions by 0. 
			percentstore[c].append(0)
		c = c + 1
	n = n + 1

#Stores position of each domain entry on plot.
xposition = []
#Stores each domains label for the x axis.
xlab = []
n = 0

#Adds an entry to xposition and xlab for each domain.
while n < len(domainstore):
	xposition.append(n)
	xlab.append(domainstore[n][0])
	n = n + 1

n = 0
#Contains the y coordinates for starting position of each bar of the counts plot.
heightstore = []
while n < len(countstore):
	heightstore.append([])
	c = 0
	while c < len(countstore[n]):
		if n == 0:
		#If first row of entries in heightstore: value is set to 0
			heightstore[n].append(0)
		#Otherwise: value is set to starting position of bar below current one plus the 		#count value of bar below current one.

		#e.g. counts data: [5,10,15,20]	gives height data: [0,0,0,0]
		#		   [4,8,12,16]			   [5,10,15,20]
		#		   [3,6,9,12]			   [9,18,27,36]
		else:
			heightstore[n].append(countstore[n - 1][c] + heightstore[n - 1][c])
		c = c + 1
	n = n + 1

n = 0
#Contains the y coordinates for starting position of each bar of the percentage plot.
perheightstore = []
while n < len(percentstore):
	perheightstore.append([])
	c = 0
	while c < len(percentstore[n]):
		#If first row of entries in perheightstore: value is set to 0
		if n == 0:
			perheightstore[n].append(0)
		#Otherwise: value is set to starting position of bar below current one plus the 		#count value of bar below current one.

		#e.g. counts data: [5,10,15,20]	gives height data: [0,0,0,0]
		#		   [4,8,12,16]			   [5,10,15,20]
		#		   [3,6,9,12]			   [9,18,27,36]
		else:
			perheightstore[n].append(percentstore[n - 1][c] + perheightstore[n - 1][c])
		c = c + 1
	n = n + 1

#Stores basename of the input file to be used for output file name.
fstore = filename.split('.txt')
fname = fstore[0]

#Begins writing information to counts version of plotting script.
writefile = "Make_plot_" + fname + "_counts.py"
file = open(writefile,"w")

#Lines loading in dependencies.
writeline ="#Loads in necessary python modules.\nimport sys\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom matplotlib import rc\nimport pandas as pd\nfrom matplotlib.pyplot import figure\n"
file.write(writeline)

#Name of input file, font settings and image size.
writeline = "\n#Name of input file.\nname = '" + fname + "'\n\n#Font size and style settings for text, axes and title.\nrc('font', weight='bold')\nplt.rc('axes', titlesize=10)\nplt.rc('axes', labelsize=6)\n" + "plt.rcParams.update({'font.size': 4})\n\n#Sets the size of plot image.\nfigure(num=None, figsize=(8, 6), dpi=640, facecolor='w', edgecolor='k')\n\n"
file.write(writeline)

n = 0

#Arrays of counts data to be used.
writeline = "#Subdomain counts taken from the input file, each array entry contains the counts for\n#each domain plotted and the arrays stack up ontop of each other, bar1 at the base and moving up.\n"
file.write(writeline) 
while n < len(countstore):
	writeline = "bars" + str(n + 1) + " = " + str(countstore[n]) + "\n"
	file.write(writeline)
	n = n + 1

#Starting positions for each bar.
writeline = "\n#Barheight contains the y axis position for the start of each bar,\n#this allows them to be stacked on top of each other.\n"
file.write(writeline)

n = 0

while n < len(heightstore):
	writeline = "barheight" + str(n + 1) + " = " + str(heightstore[n]) + "\n"
	file.write(writeline)
	n = n + 1

#Arrays countaining the xpositions of domains and their label for the x axis respectively.

writeline = "\n\n#Creates a position on the x-axis for each domain.\nr = " + str(xposition) + "\n"
file.write(writeline)
writeline = "\n#Name of each position on the axis to be used in labelling.\nnames = " + str(xlab) + "\n"
file.write(writeline)

#Spacing between domains.
writeline = "\n#Sets the spacing between each domain on the x-axis.\nbarWidth = 1\n\n"
file.write(writeline)

#Lines to add the bars to the plot.
n = 0
writeline = "#Adds each array of bars to the plot.\n"
file.write(writeline)
while n < len(countstore):
	writeline = "plt.bar(r, bars" + str(n + 1) + ", bottom=barheight" + str(n + 1) + ", color='" + colours[n % 6] + "', edgecolor='black', width=barWidth)\n"
	file.write(writeline)
	n = n + 1

#Adds domain names to x axis.
writeline = "\n\n#Adds name of domains to each position on the x-axis.\nplt.xticks(r, names, fontweight='bold')"
file.write(writeline)

#X axis, yaxis and plot title labels added.
writeline = "\n#Adds labels to the x and y axis.\nplt.xlabel('Domain', fontweight='bold')"
file.write(writeline)
writeline = "\nplt.ylabel('Number of Hits', fontweight='bold')"
file.write(writeline)
writeline = "\n#Adds a title to the plot.\nplt.title(name + '_counts', fontweight='bold')\n\n"
file.write(writeline)

#Adds the subdomain labels to their respective bars.
writeline = "\n#Adds a label to each bar on the plot.\n"
file.write(writeline)
n = 0
while n < len(labelstore):
	c = 0
	while c < len(labelstore[n]):
		#Only adds lebels for bars with a non-empty labelstore entry.
		if labelstore[n][c] != '':
			#Y-coordinate set to middle of the bar.
			yposit = str(heightstore[n][c] + (countstore[n][c] / 2))
			xposit = str(c)
			writeline = "plt.annotate('" + labelstore[n][c] + "', (" + xposit + "," + yposit + "), textcoords='offset points', xytext=(0,-2), ha='center')\n"
			file.write(writeline)
		c = c + 1
	n = n + 1

#Save plot to file line.
writeline = "\n#Saves plot to output image.\nplt.savefig('" + fname + "_counts.png')"
file.write(writeline)

file.close()

#Begins writing information to percentage version of plotting script.
writefile = "Make_plot_" + fname + "_percent.py"
file = open(writefile,"w")

#Lines loading in dependencies.
writeline ="#Loads in necessary python modules.\nimport sys\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom matplotlib import rc\nimport pandas as pd\nfrom matplotlib.pyplot import figure\n"
file.write(writeline)

#Name of input file, font settings and image size.
writeline = "\n#Name of input file.\nname = '" + fname + "'\n\n#Font size and style settings for text, axes and title.\nrc('font', weight='bold')\nplt.rc('axes', titlesize=10)\nplt.rc('axes', labelsize=6)\n" + "plt.rcParams.update({'font.size': 4})\n\n#Sets the size of plot image.\nfigure(num=None, figsize=(8, 6), dpi=640, facecolor='w', edgecolor='k')\n\n"
file.write(writeline)

n = 0

#Arrays of counts data to be used.
writeline = "#Subdomain counts taken from the input file, each array entry contains the counts, shown as a \n#percentage, for each domain plotted and the arrays stack up ontop of each other, bar1 at the \n#base and moving up.\n"
file.write(writeline) 
while n < len(percentstore):
	writeline = "bars" + str(n + 1) + " = " + str(percentstore[n]) + "\n"
	file.write(writeline)
	n = n + 1

#Starting positions for each bar.
writeline = "\n#Perbarheight contains the y axis position for the start of each bar,\n#this allows them to be stacked on top of each other.\n"
file.write(writeline)
n = 0

while n < len(perheightstore):
	writeline = "barheight" + str(n + 1) + " = " + str(perheightstore[n]) + "\n"
	file.write(writeline)
	n = n + 1
n = 0

#Arrays countaining the xpositions of domains and their label for the x axis respectively.

writeline = "\n\n#Creates a position on the x-axis for each domain.\nr = " + str(xposition) + "\n"
file.write(writeline)
writeline = "\n#Name of each position on the axis to be used in labelling.\nnames = " + str(xlab) + "\n"
file.write(writeline)

#Spacing between domains.
writeline = "\n#sets the spacing between each domain entry on the x-axis\nbarWidth = 1\n\n"
file.write(writeline)

#Lines to add the bars to the plot.
n = 0
writeline = "#Adds each array of bars to the plot.\n"
file.write(writeline)

while n < len(countstore):
	writeline = "plt.bar(r, bars" + str(n + 1) + ", bottom=barheight" + str(n + 1) + ", color='" + colours[n % 6] + "', edgecolor='black', width=barWidth)\n"
	file.write(writeline)
	n = n + 1

#Adds domain names to x axis.
writeline = "\n\n#Adds name of domains to each position on the x-axis.\nplt.xticks(r, names, fontweight='bold')"
file.write(writeline)

#X axis, yaxis and plot title labels added.
writeline = "\n#Adds labels to the x and y axis.\nplt.xlabel('Domain', fontweight='bold')"
file.write(writeline)
writeline = "\nplt.ylabel(' Percentage of Hits', fontweight='bold')"
file.write(writeline)
writeline = "\n#Adds a title to the plot.\nplt.title(name + '_percent', fontweight='bold')\n\n"
file.write(writeline)

#Adds the subdomain labels to their respective bars.
n = 0
writeline = "\n#Adds a label to each bar on the plot.\n"
file.write(writeline)
while n < len(labelstore):
	c = 0
	while c < len(labelstore[n]):
		#Only adds lebels for bars with a non-empty labelstore entry.
		if labelstore[n][c] != '':
			#Y-coordinate set to middle of the bar.
			yposit = str(perheightstore[n][c] + (percentstore[n][c] / 2))
			xposit = str(c)
			writeline = "plt.annotate('" + labelstore[n][c] + "', (" + xposit + "," + yposit + "), textcoords='offset points', xytext=(0,-2), ha='center')\n"
			file.write(writeline)
		c = c + 1
	n = n + 1

#Save plot to file line.
writeline = "\n#Saves plot to output image.\nplt.savefig('" + fname + "_percent.png')"
file.write(writeline)

file.close()
