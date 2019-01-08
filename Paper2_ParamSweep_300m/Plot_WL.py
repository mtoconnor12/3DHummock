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

runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runDate = '18Dec18'

nruns = 32
# thaw depths are taken at the end of september (10th month) of years specified
t1 = 1
t2 = 20
month = 11
trange = [None] * ((t2-t1)/6)
print(len(trange))
t1 = t1*12+month
t2 = t2*12+month
xPos = 15 # position on the hillslope where measurement is taken
# My visdumps spit out every 30 days; however, years are 365 days, meaning months are actually 365/12 = 30.416 days long.  Thus, we need to do 2 things:
# 1) Every 6th year, we need to add one to the visdump index to assure we're looking at the right times.
# 2) We can only look at visdumps every 6th year to truly compare apples to apples
c = -1
for i in range(t1,t2,12):
	ind = (i - month)/12 # ind is the year of each visdump
	if(ind%6 == 0): # if it is a year that is divisible by 6
		c = c + 1
		print(c)
		trange[c] = i + c # the index of the visdump we want is the month (i) plus the shift (c)

fig, axes = plt.subplots(4,2,sharex=True)

for i in range(1):#len(runPrefixList)):
	y = np.nan*np.ones([len(trange),nruns],'d')
	for j in range(nruns):
		directory = runPrefixList[i] + '_' + runDate + '.' + str(j+1)
                isDir = os.path.isdir(os.getcwd() + '/' + directory)
                if not isDir:
                        continue
		keys, times, dat = parse_ats.readATS(directory, "visdump_data.h5", timeunits='yr')
		col_dat = transect_data.transect_data(['saturation_gas'], keys=np.s_[trange], directory=directory)
		times_subset = times[trange]
		#col_dat structure:
		#col 1 = variable
		#col 2 = time
		#col 3 = x position
		#col 4 = z position
		z_surf = col_dat[1,0,:,-1] + (col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2. # average of the uppermost and second-to-uppermost rows, shifted up to the top row
                z_bott = col_dat[1,0,:,0] - (col_dat[1,0,:,1] - col_dat[1,0,:,0])/2. # average of the bottom and second-to-bottom rows, shifted up to the bottom row
       	        for k in range(len(trange)):
			where_unsat = np.where(col_dat[2,k,xPos,:] > 0)[-1]
	                #print(where_unsat)
        	        if len(where_unsat) == 0:
			        y[k,j] = 0.
	                elif where_unsat[0] == 0:
        	                y[k,j] = z_surf[xPos] - z_bott[xPos]
                	else:
                        	y[k,j] = z_surf[xPos] - (col_dat[1,k,xPos,where_unsat[0]] + col_dat[1,k,xPos,where_unsat[0]-1])/2
                #if i == 6 and j > 21:
                #        continue
		#t = mat[t1:t2,0]/86400/365  # time in years
		#y_part = mat[trange,1] # thing we're plotting
		#yChng = np.nan*np.ones([trange.size-1],'d')
		#for k in range(trange.size-1):
		#	yChng[k] = (y_part[k+1] - y_part[k])/y_part[k]
		#y[:,j] =(yChng)*1E6
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
		axes[i%4,i/4].scatter(trange,y[:,j],color=cVal,facecolors=fillColor, marker=shapeVal,s=sizeVal)
		plt.hold(True)
#	axes[i%4,i/4].scatter(range(1,8),y[0:7],color='k')
#        axes[i%4,i/4].scatter(range(9,16),y[8:15],color='r')
#        axes[i%4,i/4].scatter(range(17,24),y[16:23],color='b')
#        axes[i%4,i/4].scatter(range(25,32),y[24:31],color='g')
	plt.hold(True)
	#axes[i%4,i/4].set_ylim([9,11])
#	plt.legend(runPrefixList,loc='upper left')
	axes[i%4,i/4].set_title(runPrefixList[i])
#	axes.xlabel('Time [yrs]')
#	plt.ylabel('Total water content [m^3]')


plt.show() 

foldername = os.path.basename(os.getcwd())
#plt.savefig(foldername + '_Subsurface_Outlet_Flux.eps', format = 'eps', dpi = 1000)

