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

runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runDate = '18Dec18'

nruns = 32
#t1 = (9*12) + 0 # starting month (March of year 9)
#t2 = (9*12) + 12 # ending month (Dec of year 9)

t1 = 0
t2 = 275
interval = 1

trange = range(t1,t2,interval)
xPos = 0 # position on the hillslope where measurement is taken
# My visdumps spit out every 30 days; however, years are 365 days, meaning months are actually 365/12 = 30.416 days long.  Thus, we need to do 2 things:
# 1) Every 6th year, we need to add one to the visdump index to assure we're looking at the right times.
# 2) We can only look at visdumps every 6th year to truly compare apples to apples

fig, axes = plt.subplots(4,2,sharex=True)

#fname = 'ThawData_Yr10_All.csv'
#with open(fname, 'wb') as csvFile:
#	writer = csv.writer(csvFile, delimiter=',')

for i in range(len(runPrefixList)):
	y = np.nan*np.ones([nruns,len(trange)],'d')
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
                                y[j,k] = 0.
                        elif where_unsat[0] == 0:
                                y[j,k] = z_surf[xPos] - z_bott[xPos]
                        else:
                                y[j,k] = z_surf[xPos] - (col_dat[1,k,xPos,where_unsat[0]] + col_dat[1,k,xPos,where_unsat[0]-1])/2
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
	np.savetxt(runPrefixList[i] + '_WL_Daily.csv',y,delimiter=',')
	print(runPrefixList[i] + '_WL.csv' + ' Written!')
	plt.hold(True)
	axes[i%4,i/4].set_title(runPrefixList[i])

plt.show() 
csvFile.close()
foldername = os.path.basename(os.getcwd())
plt.savefig(foldername + 'All_WL.eps', format = 'eps', dpi = 1000)

