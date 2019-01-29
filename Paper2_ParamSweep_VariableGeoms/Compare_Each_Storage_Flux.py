#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
import math
from scipy import stats
import os
from numpy import genfromtxt
from matplotlib import colors

runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runDate = '18Dec18'

nruns = 32

t1 = 9
t2 = 10
t1 = t1*365
t2 = t2*365
ndays = (t2-t1)
y = np.nan*np.ones([ndays,nruns],'d')
meany = np.nan*np.ones([ndays,len(runPrefixList)],'d')
#t = np.nan*np.ones([ndays,nruns],'d')

t1 = (9*360) + 90 # starting month (March of year 9)
t2 = (9*360) + 365 #ending month (Dec of year 9)
trange1 = range(t1,t2) # representing monthly timesteps
trange2 = trange1
t1a = (9*360) + 0
t2a = (9*360) + 365
trange3 = range(t1a,t2a) # representing daily timesteps

fig, axes = plt.subplots(2,2,sharex=True,sharey=True)

index_to_test = [6,14,20,28]
c = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray']

for i in range(len(runPrefixList)):
	y = np.nan*np.ones([ndays,nruns],'d')
	count = 0
	# Structure of y:
        # 1) There is a separate file for each classification type
        # 2) Rows increase with the number of runs
        # 3) Columns increase with months, starting from May of year 10
        # y = genfromtxt(runPrefixList[i] + '_Thaw_Daily.csv', delimiter=',')
        #mean_y = np.mean(y, axis = 0)
        y2 = genfromtxt(runPrefixList[i] + '_Storage_Daily.csv', delimiter=',')
        #mean_y2 = np.mean(y2, axis = 0)
        y3 = genfromtxt(runPrefixList[i] + '_Flow.csv', delimiter = ',') # One year of daily flow observations
        y3 = y3[:,0:365]
        #mean_y3 = np.mean(y3, axis = 0)
        y4 = genfromtxt(runPrefixList[i] + '_SurfaceFlow.csv', delimiter = ',')
        y4 = y4[:,0:365]
	for j in index_to_test:
		m = count/2
		n = count%2
		axes2 = axes[m,n].twinx()
                plt.hold(True)
		axes[m,n].plot(trange1,-y2[j,:], color = c[i])
		axes2.plot(trange3,y3[j,:],linewidth = 2, color = c[i])
                axes2.plot(trange3,y4[j,:],linestyle = '--', color = c[i])
                axes[m,n].set_xlim([3350,3600])
		axes[m,n].set_ylim([-100,0])
		axes2.set_yscale('log')
                axes2.set_ylim([1E-11,1E8])
                axes2.set_xlim([3350,3600])
		plt.hold(True)
		axes[m,n].set_title('Run # ' + str(j))
		count = count + 1

axes[1,1].legend(runPrefixList)
plt.show() 

foldername = os.path.basename(os.getcwd())
plt.savefig(foldername + '_Compare_Flux_Storage.eps', format = 'eps', dpi = 1000)


