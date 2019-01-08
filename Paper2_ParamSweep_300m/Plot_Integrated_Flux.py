#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
import math
from scipy import stats
import os

runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runDate = '18Dec18'

nruns = 32

t1 = 9
t2 = 10
t1 = t1*365
t2 = t2*365
ndays = (t2-t1)
y_part = np.nan*np.ones([ndays,nruns],'d')
meany = np.nan*np.ones([ndays,len(runPrefixList)],'d')
#t = np.nan*np.ones([ndays,nruns],'d')
fig, axes = plt.subplots(4,2,sharex=True)

for i in range(len(runPrefixList)):
	y = np.nan*np.ones([nruns,1],'d')
	for j in range(nruns):
		directory = runPrefixList[i] + '_' + runDate + '.' + str(j+1)
                isDir = os.path.isdir(os.getcwd() + '/' + directory)
                if not isDir:
                        continue
                mat = np.loadtxt(runPrefixList[i] + '_' + runDate + '.' + str(j+1) + '/subsurface_outlet_flux.dat')
                if i == 6 and j > 21:
                        continue
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
		if(j%4 < 2):
			shapeVal = 's'
		else:
			shapeVal = '*'
		if(j%8 < 4):
			fillColor = 'none'
		else:
			fillColor = cVal
		if(j%2 == 0):
			sizeVal = 50
		else:
			sizeVal = 150
		axes[i%4,i/4].scatter(j+1,y[j],color=cVal,facecolors=fillColor, marker=shapeVal,s=sizeVal)
		plt.hold(True)
#	axes[i%4,i/4].scatter(range(1,8),y[0:7],color='k')
#        axes[i%4,i/4].scatter(range(9,16),y[8:15],color='r')
#        axes[i%4,i/4].scatter(range(17,24),y[16:23],color='b')
#        axes[i%4,i/4].scatter(range(25,32),y[24:31],color='g')
	plt.hold(True)
#	axes[i%4,i/4].set_xlim([9.35,10])
#	plt.legend(runPrefixList,loc='upper left')
	axes[i%4,i/4].set_title(runPrefixList[i])
#	axes.xlabel('Time [yrs]')
#	plt.ylabel('Total water content [m^3]')


plt.show() 

foldername = os.path.basename(os.getcwd())
#plt.savefig(foldername + '_Subsurface_Outlet_Flux.eps', format = 'eps', dpi = 1000)

