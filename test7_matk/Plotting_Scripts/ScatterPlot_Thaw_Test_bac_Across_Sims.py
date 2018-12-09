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



nruns = 18
c = 0
leg = [None]*nruns
m = [0.01,0.1]
bac = [0.01,0.1,0.22]
bct = [0.02,0.14,0.4]

for i in range(2):
	for j in range(3):
		for k in range(3):
			print m[i]
			leg[c] = ['m=' + str(m[i]) + ' bac=' + str(bac[j]) + ' bct=' + str(bct[k])]
			c = c + 1

		

leg_ordered = [None]*18

# Low-sloping domains: simulations 1-9
# Hi-sloping domains: simulations 10-18

ind = 12*9 + 9 # time index from which we will extract thaw depths
xPos = 15 # the horizontal position from which we will extract thaw depths

# ONLY plot the SHALLOW SLOPING thaws (slope does not matter)

wtd = np.nan*np.ones((np.size(bac),np.size(bct)),'d')
for i in range(1):
	for j in range(np.size(bct)):
		for k in range(np.size(bac)):
			directory = "../CenturySim_01Dec18_Debug."+str((j+1) + (k*3))
			print directory
			keys, times, dat = parse_ats.readATS(directory, "visdump_data.h5", timeunits='yr')
			col_dat = transect_data.transect_data(['saturation_ice'], keys=np.s_[ind], directory=directory)
			times_subset = times[ind]
			nvar, nt, nx, nz = col_dat.shape

			print(wtd.shape)
			z_surf = col_dat[1,0,:,-1] + (col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2. # average of the uppermost and second-to-uppermost rows, shifted up to the top row
			z_bott = col_dat[1,0,:,0] - (col_dat[1,0,:,1] - col_dat[1,0,:,0])/2. # average of the bottom and second-to-bottom rows, shifted up to the bottom row

			where_unsat = np.where(col_dat[2,0,xPos,:] == 0)[0]
			if len(where_unsat) == 0:
				wtd[j,k] = 0.
			elif where_unsat[0] == 0:
				wtd[j,k] = z_surf[xPos] - z_bott[xPos]
			else:
				wtd[j,k] = z_surf[xPos] - (col_dat[1,:,xPos,where_unsat[0]] + col_dat[1,:,xPos,where_unsat[0]-1])/2 
		plt.plot(bac,-wtd[j,:])
plt.legend(['Min Catotelm','Mean Catotelm','Max Catotelm'],loc='lower right')
plt.title('Active Layer Thickness vs. Acrotelm Thickness, Grouped by Catotelm Thickness')
plt.xlabel('Acrotelm Thickness [m]')
plt.ylabel('Active Layer Thickness [m]')
plt.show() 
