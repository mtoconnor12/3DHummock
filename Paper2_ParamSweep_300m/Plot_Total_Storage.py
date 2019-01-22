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
titleList = ['Tussock Tundra High','Tussock Tundra Low','Water Track','Woody Shrubs, Hillslope','Woody Shrubs, Riparian','Frost Boils','Sedge High','Sedge Low']
runDate = '18Dec18'

nruns = 32

t1 = 0
t2 = 10
t1 = t1*365
t2 = t2*365
trange = 365*np.arange((t1/365),(t2/365))
print(trange)
print(trange.size)
ndays = (t2-t1)
y_part = np.nan*np.ones([ndays,nruns],'d')
meany = np.nan*np.ones([ndays,len(runPrefixList)],'d')
#t = np.nan*np.ones([ndays,nruns],'d')
fig, axes = plt.subplots(4,2,sharex=True,sharey=True)

for i in range(len(runPrefixList)):
	y = np.nan*np.ones([trange.size-1,nruns],'d')
	for j in range(nruns):
		directory = runPrefixList[i] + '_' + runDate + '.' + str(j+1)
                isDir = os.path.isdir(os.getcwd() + '/' + directory)
                if not isDir:
                        continue
                mat = np.loadtxt(runPrefixList[i] + '_' + runDate + '.' + str(j+1) + '/subsurface_water_content.dat')
                #if i == 6 and j > 21:
                #        continue
		#matSubset = mat[t1:-1,:]
		#matShape = matSubset.shape
		t = mat[t1:t2,0]/86400/365  # time in days
		y_part = mat[trange,1] # thing we're plotting
		yChng = np.nan*np.ones([trange.size-1],'d')
		for k in range(trange.size-1):
			yChng[k] = (y_part[k+1] - y_part[k])#/y_part[k]
		y[:,j] =(yChng)/55000# conv from mol to m3
		y[:,j] = y[:,j]/300 # convert from m3 to m (average)
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
		axes[i%4,i/4].scatter(np.arange((t1/365)+1,t2/365),y[:,j],color=cVal,facecolors=fillColor, marker=shapeVal,s=sizeVal)
		plt.hold(True)
#	axes[i%4,i/4].scatter(range(1,8),y[0:7],color='k')
#        axes[i%4,i/4].scatter(range(9,16),y[8:15],color='r')
#        axes[i%4,i/4].scatter(range(17,24),y[16:23],color='b')
#        axes[i%4,i/4].scatter(range(25,32),y[24:31],color='g')
	plt.hold(True)
	#axes[i%4,i/4].set_ylim([9,11])
#	plt.legend(runPrefixList,loc='upper left')
	axes[i%4,i/4].set_title(titleList[i])
	if(i%4 == 3):
		axes[i%4,i/4].set_xlabel('Time [yrs]')
	axes[i%4,i/4].set_ylabel('m water')


plt.show() 

foldername = os.path.basename(os.getcwd())
#plt.savefig(foldername + '_Subsurface_Outlet_Flux.eps', format = 'eps', dpi = 1000)

