#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import sys,os
sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools', 'utils'))
import parse_xmf, parse_ats
import column_data, transect_data
import colors
import mesh
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import colorbar
from scipy import stats

# INPUTS:
nruns = 32
yr = 20
ind = (12*yr)+9 # time index from which we will extract thaw depths
xPos = 15 # the horizontal position from which we will extract thaw depths

runPrefixList = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','WoodyShrubsRiparianHi','FrostBoils','SedgeHi','SedgeLo']
runDate = '18Dec18'

bct_lo = [8,6,1,11,32,6,6,13,20,17]
bct_hi = [15,18,14,33,50,14,15,27,34,44]

wtd = np.nan*np.ones([nruns,len(runPrefixList)],'d')

col =  ['b','g','r','c','m','y','k','w','b','g']

for q in range(len(runPrefixList)):	
	for i in range(nruns):
        	directory = runPrefixList[q] + '_' + runDate + '.' + str(i+1)
	        print directory
	        isDir = os.path.isdir(os.getcwd() + '/' + directory)
		if not isDir:
			continue
		keys, times, dat = parse_ats.readATS(directory, "visdump_data.h5", timeunits='yr')
	        mos = np.round(times*12)
		if ind > mos[-1]:
			continue
		col_dat = transect_data.transect_data(['saturation_ice'], keys=np.s_[ind], directory=directory)
        	times_subset = times[ind]
	        nvar, nt, nx, nz = col_dat.shape
	
        	z_surf = col_dat[1,0,:,-1] + (col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2. # average of the uppermost and second-to-uppermost rows, shifted up to the top row
	        z_bott = col_dat[1,0,:,0] - (col_dat[1,0,:,1] - col_dat[1,0,:,0])/2. # average of the bottom and second-to-bottom rows, shifted up to the bottom row
	        where_unsat = np.where(col_dat[2,0,xPos,:] == 0)[0]
	        print(where_unsat)
		if len(where_unsat) == 0:
	                wtd[i,q] = 0.
	        elif where_unsat[0] == 0:
	                wtd[i,q] = z_surf[xPos] - z_bott[xPos]
	        else:
	                wtd[i,q] = z_surf[xPos] - (col_dat[1,:,xPos,where_unsat[0]] + col_dat[1,:,xPos,where_unsat[0]-1])/2
	plt.scatter(np.ones([8,1],'d')*bct_lo[q],-wtd[0:8,q],c=col[q],marker='s')
	plt.hold(True)
	plt.scatter(np.ones([8,1],'d')*bct_hi[q],-wtd[8:16,q],c=col[q],marker='s')
	plt.hold(True)
	plt.scatter(np.ones([8,1],'d')*bct_lo[q],-wtd[16:24,q],c=col[q])
	plt.hold(True)		
	plt.scatter(np.ones([8,1],'d')*bct_hi[q],-wtd[24:32,q],c=col[q])
	plt.hold(True)

plt.title('Active Layer Thickness vs. Acrotelm Thickness, Grouped by Catotelm Thickness')
plt.xlabel('Catotelm Thickness [m]')
plt.ylabel('Active Layer Thickness [m]')
plt.legend(runPrefixList)
plt.xlim([0,60])
plt.ylim([-0.3,-0.8])
plt.show()

meanThaw = np.nan*np.ones(len(runPrefixList),'d')
stdThaw = np.nan*np.ones(len(runPrefixList),'d')
for q in range(len(runPrefixList)):
	meanThaw[q] = stats.nanmean(wtd[:,q])
	stdThaw[q] = stats.nanstd(wtd[:,q])

print(meanThaw)
print(stdThaw)
