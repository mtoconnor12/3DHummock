#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
import math
from scipy import stats
import os

### THE FIRST RUNS ###

#runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','SedgeHi','WoodyShrubsRiparianHi','SedgeLo','FrostBoils']

runDate = '18Dec18'

nruns = 32

t1 = 9
t2 = 10
t1 = t1*365
t2 = t2*365
ndays = (t2-t1)
fig, axes = plt.subplots(4,2,sharex=True)
for i in range(len(runPrefixList)):
	y = np.nan*np.ones([nruns,1],'d')
	for j in range(nruns):
		directory = runPrefixList[i] + '_' + runDate + '.' + str(j+1)
                isDir = os.path.isdir(os.getcwd() + '/' + directory)
                if not isDir:
                        continue
                mat = np.loadtxt(runPrefixList[i] + '_' + runDate + '.' + str(j+1) + '/subsurface_outlet_flux.dat')
		matSubset = mat[t1:-1,:]
		matShape = matSubset.shape
		t = mat[t1:t2,0]/86400/365  # time in days
		y_part = mat[t1:t2,1] # thing we're plotting
		y[j] = sum(y_part)
		if(j<8):
			cVal = 'k'
		elif(j<16):
			cVal = 'r'
		elif(j<24):
			cVal = 'b'
		else:
			cVal = 'g'
		axes[i%4,i/4].scatter(j+1,y[j],color=cVal,facecolors=cVal)
		plt.hold(True)

os.chdir('../Paper2_ParamSweep_300m_22Jan19')

for i in range(len(runPrefixList)):
        y = np.nan*np.ones([nruns,1],'d')
        for j in range(nruns):
                directory = runPrefixList[i] + '_' + runDate + '.' + str(j+1)
                isDir = os.path.isdir(os.getcwd() + '/' + directory)
                if not isDir:
                        continue
                mat = np.loadtxt(runPrefixList[i] + '_' + runDate + '.' + str(j+1) + '/subsurface_outlet_flux.dat')
                matSubset = mat[t1:-1,:]
                matShape = matSubset.shape
                t = mat[t1:t2,0]/86400/365  # time in days
                y_part = mat[t1:t2,1] # thing we're plotting
                y[j] = sum(y_part)
                if(j<8):
                        cVal = 'k'
                elif(j<16):
                        cVal = 'r'
                elif(j<24):
                        cVal = 'b'
                else:
                        cVal = 'g'
                axes[i%4,i/4].scatter(j+1,y[j],color=cVal,facecolors='none')
                plt.hold(True)
        axes[i%4,i/4].set_title(runPrefixList[i])
	axes[i%4,i/4].set_yscale('log')
plt.show() 

foldername = os.path.basename(os.getcwd())
#plt.savefig(foldername + '_Subsurface_Outlet_Flux.eps', format = 'eps', dpi = 1000)

