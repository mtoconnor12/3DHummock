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

for i in range(len(runPrefixList)):
	# Structure of y: 
	# 1) There is a separate file for each classification type
	# 2) Rows increase with the number of runs
	# 3) Columns increase with months, starting from May of year 10
	y = genfromtxt(runPrefixList[i] + '_Thaw.csv', delimiter=',')
	mean_y = np.mean(y, axis = 0)
	print(mean_y.shape)
	plt.scatter(trange,-mean_y)#,color=cVal,facecolors=fillColor, marker=shapeVal,s=sizeVal)
	plt.hold(True)

plt.title('Average Active Layer Thickness of Each Group Over Time')
plt.xlabel('Month of simulation')
plt.ylabel('Active Layer Depth [m]')
plt.legend(runPrefixList)
plt.show() 
foldername = os.path.basename(os.getcwd())
plt.savefig(foldername + 'Thaw_Means.eps', format = 'eps', dpi = 1000)

