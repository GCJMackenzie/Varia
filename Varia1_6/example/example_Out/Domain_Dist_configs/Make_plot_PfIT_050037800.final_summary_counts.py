#Loads in necessary python modules.
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
from matplotlib.pyplot import figure

#Name of input file.
name = 'PfIT_050037800.final_summary'

#Font size and style settings for text, axes and title.
rc('font', weight='bold')
plt.rc('axes', titlesize=10)
plt.rc('axes', labelsize=6)
plt.rcParams.update({'font.size': 4})

#Sets the size of plot image.
figure(num=None, figsize=(8, 6), dpi=640, facecolor='w', edgecolor='k')

#Subdomain counts taken from the input file, each array entry contains the counts for
#each domain plotted and the arrays stack up ontop of each other, bar1 at the base and moving up.
bars1 = [0, 7, 7, 0, 0, 7, 0, 1, 0, 6, 3, 0, 0, 2]
bars2 = [0, 0, 0, 0, 0, 0, 0, 7, 0, 5, 4, 0, 0, 0]
bars3 = [0, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0, 0, 0, 0]
bars4 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

#Barheight contains the y axis position for the start of each bar,
#this allows them to be stacked on top of each other.
barheight1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
barheight2 = [0, 7, 7, 0, 0, 7, 0, 1, 0, 6, 3, 0, 0, 2]
barheight3 = [0, 7, 7, 0, 0, 7, 0, 8, 0, 11, 7, 0, 0, 2]
barheight4 = [0, 7, 7, 0, 0, 7, 0, 13, 0, 12, 7, 0, 0, 2]


#Creates a position on the x-axis for each domain.
r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

#Name of each position on the axis to be used in labelling.
names = ['NTS', 'DBLa', 'CIDRa', 'DBLd', 'CIDRd', 'DBLb', 'CIDRb', 'DBLg', 'CIDRg', 'DBLe', 'DBLz', 'DBLpam', 'CIDRpam', 'ATS']

#Sets the spacing between each domain on the x-axis.
barWidth = 1

#Adds each array of bars to the plot.
plt.bar(r, bars1, bottom=barheight1, color='red', edgecolor='black', width=barWidth)
plt.bar(r, bars2, bottom=barheight2, color='blue', edgecolor='black', width=barWidth)
plt.bar(r, bars3, bottom=barheight3, color='green', edgecolor='black', width=barWidth)
plt.bar(r, bars4, bottom=barheight4, color='yellow', edgecolor='black', width=barWidth)


#Adds name of domains to each position on the x-axis.
plt.xticks(r, names, fontweight='bold')
#Adds labels to the x and y axis.
plt.xlabel('Domain', fontweight='bold')
plt.ylabel('Number of Hits', fontweight='bold')
#Adds a title to the plot.
plt.title(name + '_counts', fontweight='bold')


#Adds a label to each bar on the plot.
plt.annotate('DBLa1.1', (1,3.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('CIDRa1.2', (2,3.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLb11', (5,3.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLg18', (7,0.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLe1', (9,3.0), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLz1', (10,1.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('ATSvar1', (13,1.0), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLg8', (7,4.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLe5', (9,8.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLz2', (10,5.0), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLg1', (7,10.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLe14', (9,11.5), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLg10', (7,13.5), textcoords='offset points', xytext=(0,-2), ha='center')

#Saves plot to output image.
plt.savefig('PfIT_050037800.final_summary_counts.png')