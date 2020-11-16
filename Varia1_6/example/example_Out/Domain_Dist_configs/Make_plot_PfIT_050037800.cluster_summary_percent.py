#Loads in necessary python modules.
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
from matplotlib.pyplot import figure

#Name of input file.
name = 'PfIT_050037800.cluster_summary'

#Font size and style settings for text, axes and title.
rc('font', weight='bold')
plt.rc('axes', titlesize=10)
plt.rc('axes', labelsize=6)
plt.rcParams.update({'font.size': 4})

#Sets the size of plot image.
figure(num=None, figsize=(8, 6), dpi=640, facecolor='w', edgecolor='k')

#Subdomain counts taken from the input file, each array entry contains the counts, shown as a 
#percentage, for each domain plotted and the arrays stack up ontop of each other, bar1 at the 
#base and moving up.
bars1 = [0, 94.1, 100.0, 0, 0, 100.0, 0, 41.4, 0, 50.0, 64.3, 0, 0, 100.0]
bars2 = [0, 5.9, 0.0, 0, 0, 0.0, 0, 48.3, 0, 45.8, 35.7, 0, 0, 0.0]
bars3 = [0, 0.0, 0.0, 0, 0, 0.0, 0, 3.4, 0, 4.2, 0.0, 0, 0, 0.0]
bars4 = [0, 0.0, 0.0, 0, 0, 0.0, 0, 6.9, 0, 0.0, 0.0, 0, 0, 0.0]

#Perbarheight contains the y axis position for the start of each bar,
#this allows them to be stacked on top of each other.
barheight1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
barheight2 = [0, 94.1, 100.0, 0, 0, 100.0, 0, 41.4, 0, 50.0, 64.3, 0, 0, 100.0]
barheight3 = [0, 100.0, 100.0, 0, 0, 100.0, 0, 89.69999999999999, 0, 95.8, 100.0, 0, 0, 100.0]
barheight4 = [0, 100.0, 100.0, 0, 0, 100.0, 0, 93.1, 0, 100.0, 100.0, 0, 0, 100.0]


#Creates a position on the x-axis for each domain.
r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

#Name of each position on the axis to be used in labelling.
names = ['NTS', 'DBLa', 'CIDRa', 'DBLd', 'CIDRd', 'DBLb', 'CIDRb', 'DBLg', 'CIDRg', 'DBLe', 'DBLz', 'DBLpam', 'CIDRpam', 'ATS']

#sets the spacing between each domain entry on the x-axis
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
plt.ylabel(' Percentage of Hits', fontweight='bold')
#Adds a title to the plot.
plt.title(name + '_percent', fontweight='bold')


#Adds a label to each bar on the plot.
plt.annotate('DBLa1.1', (1,47.05), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('CIDRa1.2', (2,50.0), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLb11', (5,50.0), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLg1', (7,20.7), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLe1', (9,25.0), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLz1', (10,32.15), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('ATSvar1', (13,50.0), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLa0.13', (1,97.05), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLg8', (7,65.55), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLe5', (9,72.9), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLz2', (10,82.15), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLg18', (7,91.39999999999999), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLe14', (9,97.89999999999999), textcoords='offset points', xytext=(0,-2), ha='center')
plt.annotate('DBLg10', (7,96.55), textcoords='offset points', xytext=(0,-2), ha='center')

#Saves plot to output image.
plt.savefig('PfIT_050037800.cluster_summary_percent.png')