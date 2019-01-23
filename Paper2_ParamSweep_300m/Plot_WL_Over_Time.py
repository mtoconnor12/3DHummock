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

runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','SedgeHi','WoodyShrubsRiparianHi','SedgeLo','FrostBoils']
#runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runDate = '18Dec18'

bac = [[0.09,0.17],[0.07,0.12],[0.05,0.10],[0.10,0.20],[0.10,0.17],[0.08,0.16],[0.03,0.12],[0.01,0.02]]
bct = [[0.06,0.14],[0.06,0.16],[0.14,0.26],[0.02,0.12],[0.20,0.34],[0.10,0.20],[0.18,0.46],[0.02,0.04]]

nruns = 32
t1 = (9*12) + 6 # starting month (March of year 9)
t2 = (9*12) + 12 # ending month (Dec of year 9)
trange = range(t1,t2)
xPos = 29 # position on the hillslope where measurement is taken
# My visdumps spit out every 30 days; however, years are 365 days, meaning months are actually 365/12 = 30.416 days long.  Thus, we need to do 2 things:
# 1) Every 6th year, we need to add one to the visdump index to assure we're looking at the right times.
# 2) We can only look at visdumps every 6th year to truly compare apples to apples

#fig, axes = plt.subplots(2,4,sharex=True,sharey=True)

for i in range(len(runPrefixList)):
	# Structure of y: 
	# 1) There is a separate file for each classification type
	# 2) Rows increase with the number of runs
	# 3) Columns increase with months, starting from May of year 10
	x = np.nan*np.ones([nruns],'d') # total organic thickness
	y = genfromtxt(runPrefixList[i] + '_Thaw.csv', delimiter=',')
	for k in range(6):
		for j in range(nruns):
			if(j<8):
                	        cVal = 'k'
	                        x[j] = bac[i][0] + bct[i][0]
        	        elif(j<16):
	                        cVal = 'r'
        	                x[j] = bac[i][0] + bct[i][1]
	                elif(j<24):
        	                cVal = 'b'
                	        x[j] = bac[i][1] + bct[i][0]
	                else:
        	                cVal = 'g'
                	        x[j] = bac[i][1] + bct[i][1]
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
		#plt.scatter(trange,-y[j,:],color=cVal,facecolors=fillColor, marker=shapeVal,s=sizeVal)
			plt.scatter(x[j],-y[j,k],color=cVal,facecolors=fillColor, marker=shapeVal,s=sizeVal)
			plt.hold(True)
	#axes[i/4,i%4].set_title(runPrefixList[i])

plt.title('The range of water levels fluctuates the least when the orgnaic columns are thickest')
plt.xlabel('Organic Thickness')
plt.ylabel('Water Depth')
plt.show() 
foldername = os.path.basename(os.getcwd())
plt.savefig(foldername + 'All_Thaw.eps', format = 'eps', dpi = 1000)

