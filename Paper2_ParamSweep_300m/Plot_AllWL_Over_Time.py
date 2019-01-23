#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import math
from scipy import stats
import sys,os
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
# Time will be measured here in days, converting the month metrics to days
t1 = ((9*12) + 6) * 30 # starting month (March of year 9)
t2 = ((9*12) + 12) * 30 # ending month (Dec of year 9)
trange1 = range(t1,t2,30) # representing monthly timesteps
trange2 = trange1
t1 = (9*12) * 30
trange3 = range(t1,t2,1) # representing daily timesteps
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
#	y = genfromtxt(runPrefixList[i] + '_Thaw.csv', delimiter=',')
	#mean_y = np.mean(y, axis = 0)
	y2 = genfromtxt(runPrefixList[i] + '_WL.csv', delimiter=',')
	#mean_y2 = np.mean(y2, axis = 0)
#	y3 = genfromtxt(runPrefixList[i] + '_Flow.csv', delimiter = ',') # One year of daily flow observations
#	y3 = y3[:,0:360]
	#mean_y3 = np.mean(y3, axis = 0)
#	axes2 = axes[i/4,i%4].twinx()
	for j in range(nruns):
		plt.scatter(trange1,-y2[j,:])
	
plt.title('Water level variability for each domain')
plt.xlabel('Month of simulation')
plt.ylabel('Depth of AL or Water[m]')
#plt.legend(runPrefixList)
plt.show() 
foldername = os.path.basename(os.getcwd())
#plt.savefig(foldername + 'Thaw_Means.eps', format = 'eps', dpi = 1000)

