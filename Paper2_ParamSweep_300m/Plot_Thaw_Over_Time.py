#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import math
from scipy import stats
import sys,os
sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools', 'utils'))
import parse_xmf, parse_ats
import column_data, transect_data
import colors
import mesh
from datetime import datetime
from matplotlib import colorbar
import csv
from numpy import genfromtxt

runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runDate = '18Dec18'

nruns = 32
t1 = (9*12) + 6 # starting month (March of year 9)
t2 = (9*12) + 12 # ending month (Dec of year 9)
trange = range(t1,t2)
xPos = 29 # position on the hillslope where measurement is taken
# My visdumps spit out every 30 days; however, years are 365 days, meaning months are actually 365/12 = 30.416 days long.  Thus, we need to do 2 things:
# 1) Every 6th year, we need to add one to the visdump index to assure we're looking at the right times.
# 2) We can only look at visdumps every 6th year to truly compare apples to apples

fig, axes = plt.subplots(4,2,sharex=True,sharey=True)

for i in range(len(runPrefixList)):
	# Structure of y: 
	# 1) There is a separate file for each classification type
	# 2) Rows increase with the number of runs
	# 3) Columns increase with months, starting from May of year 10
	y = genfromtxt(runPrefixList[i] + '_Thaw.csv', delimiter=',')
	for j in range(nruns):
		if(j<8):
			cVal = 'k'
		elif(j<16):
			cVal = 'r'
		elif(j<24):
			cVal = 'b'
		else:
			cVal = 'g'
		if(j%4 < 2):
			shapeVal = 's'
		else:
			shapeVal = '*'
		if(j%8 < 4):
			fillColor = 'none'
		else:
			fillColor = cVal
		if(j%2 == 0):
			sizeVal = 25
		else:
			sizeVal = 75
		# Write the csv file
		#rowData = [runPrefixList[i], j, y[j,:]]
		#print(rowData)
		#with open(fname, 'a') as csvFile:
		#	writer = csv.writer(csvFile)
		#	writer.writerow(rowData)

		axes[i%4,i/4].scatter(trange,y[j,:],color=cVal,facecolors=fillColor, marker=shapeVal,s=sizeVal)
		plt.hold(True)
	plt.hold(True)
	axes[i%4,i/4].set_title(runPrefixList[i])

plt.show() 
foldername = os.path.basename(os.getcwd())
plt.savefig(foldername + 'All_Thaw.eps', format = 'eps', dpi = 1000)

