#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
import math
from scipy import stats
import os

#runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','SedgeHi','WoodyShrubsRiparianHi','SedgeLo','FrostBoils']
runDate = '18Dec18'

nruns = 32

t1 = 9
t2 = 10
t1 = t1*365
t2 = t2*365
ndays = (t2-t1)
y = np.nan*np.ones([ndays,nruns],'d')
meany = np.nan*np.ones([ndays,len(runPrefixList)],'d')
min_bOM = np.nan*np.ones([len(runPrefixList)],'d')
max_bOM = np.nan*np.ones([len(runPrefixList)],'d')

bac = [[0.09,0.17],[0.07,0.12],[0.05,0.10],[0.10,0.20],[0.10,0.17],[0.08,0.16],[0.03,0.12],[0.01,0.02]]
bct = [[0.06,0.14],[0.06,0.16],[0.14,0.26],[0.02,0.12],[0.20,0.34],[0.10,0.20],[0.18,0.46],[0.02,0.04]]

for i in range(len(runPrefixList)):
	min_bOM[i] = bac[i][0] + bct[i][0]
	max_bOM[i] = bac[i][1] + bct[i][1]

range_bOM = max_bOM - min_bOM
y = np.nan*np.ones([nruns,len(runPrefixList)],'d')
q_range = np.nan*np.ones([len(runPrefixList)],'d')
q_med = np.nan*np.ones([len(runPrefixList)],'d')

for i in range(len(runPrefixList)):
	for j in range(nruns):
		directory = runPrefixList[i] + '_' + runDate + '.' + str(j+1)
                isDir = os.path.isdir(os.getcwd() + '/' + directory)
                if not isDir:
                        continue
                mat = np.loadtxt(runPrefixList[i] + '_' + runDate + '.' + str(j+1) + '/subsurface_outlet_flux.dat')
		t = mat[t1:t2,0]/86400/365  # time in days
		y_part = mat[t1:t2,1] # thing we're plotting
		y[j,i] = sum(y_part)
		if(j<8):
                        cVal = 'k'
#			x[j] = bct[i][0]# + bct[i][0]
                elif(j<16):
                        cVal = 'r'
#			x[j] = bct[i][1] #+ bct[i][1]
                elif(j<24):
                        cVal = 'b'
#			x[j] = bct[i][0]# + bct[i][0]
                else:
                        cVal = 'g'
#			x[j] = bct[i][1] #+ bct[i][1]
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
	q75,q25 = np.percentile(y[:,i],[75,25])
	q_range[i] = q75 - q25
	q_med[i] = np.percentile(y[:,i],50)
plt.scatter(range_bOM,q_range,color='r')
#plt.title('Decreasing flux with increasing OM thickness')
plt.ylabel('Range in total yearly flux [mol]')
plt.xlabel('Range in OM thickness [m]')
plt.show() 

foldername = os.path.basename(os.getcwd())
#plt.savefig(foldername + '/PlotsForTalk/TotalFluxVsBCT', format = 'eps', dpi = 1000)

